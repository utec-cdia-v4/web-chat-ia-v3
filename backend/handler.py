import json
import os
import time
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Attr, Key

from groq_client import chat_completion

CHAT_TABLE = os.getenv("CHAT_TABLE", "")

dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(CHAT_TABLE)


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
        },
        "body": json.dumps(body),
    }


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _sort_messages(messages):
    return sorted(messages, key=lambda x: x.get("sk", ""))


def create_chat(event, context):
    try:
        payload = json.loads(event.get("body") or "{}")
        title = (payload.get("title") or "Nuevo chat").strip()
        chat_id = payload.get("chatId") or f"chat-{int(time.time() * 1000)}"
        created_at = _now_iso()

        table.put_item(
            Item={
                "pk": f"CHAT#{chat_id}",
                "sk": "META",
                "chatId": chat_id,
                "title": title,
                "createdAt": created_at,
            }
        )

        return _response(201, {"chatId": chat_id, "title": title, "createdAt": created_at})
    except Exception as exc:
        return _response(500, {"error": "create_chat_failed", "detail": str(exc)})


def list_chats(event, context):
    try:
        result = table.scan(
            FilterExpression=Attr("sk").eq("META")
        )
        items = result.get("Items", [])
        chats = sorted(items, key=lambda x: x.get("createdAt", ""), reverse=True)
        return _response(200, {"chats": chats})
    except Exception as exc:
        return _response(500, {"error": "list_chats_failed", "detail": str(exc)})


def get_chat(event, context):
    try:
        chat_id = event.get("pathParameters", {}).get("chatId")
        if not chat_id:
            return _response(400, {"error": "chatId_required"})

        response = table.query(
            KeyConditionExpression=Key("pk").eq(f"CHAT#{chat_id}")
        )
        items = response.get("Items", [])
        meta = next((item for item in items if item.get("sk") == "META"), None)
        messages = [item for item in items if item.get("sk", "").startswith("MSG#")]
        messages = _sort_messages(messages)

        return _response(200, {"chat": meta, "messages": messages})
    except Exception as exc:
        return _response(500, {"error": "get_chat_failed", "detail": str(exc)})


def send_message(event, context):
    try:
        chat_id = event.get("pathParameters", {}).get("chatId")
        if not chat_id:
            return _response(400, {"error": "chatId_required"})

        payload = json.loads(event.get("body") or "{}")
        prompt = (payload.get("prompt") or "").strip()
        if not prompt:
            return _response(400, {"error": "prompt_required"})

        history_response = table.query(
            KeyConditionExpression=Key("pk").eq(f"CHAT#{chat_id}")
        )
        history_items = history_response.get("Items", [])
        history_messages = [item for item in history_items if item.get("sk", "").startswith("MSG#")]
        history_messages = _sort_messages(history_messages)

        groq_messages = []
        for message in history_messages:
            groq_messages.append({"role": message.get("role"), "content": message.get("content")})

        groq_messages.append({"role": "user", "content": prompt})

        completion = chat_completion(groq_messages)
        answer = completion.get("content", "")

        timestamp = _now_iso()
        user_sk = f"MSG#{timestamp}#000#user"
        assistant_sk = f"MSG#{timestamp}#001#assistant"

        table.put_item(
            Item={
                "pk": f"CHAT#{chat_id}",
                "sk": user_sk,
                "role": "user",
                "content": prompt,
                "createdAt": timestamp,
            }
        )
        table.put_item(
            Item={
                "pk": f"CHAT#{chat_id}",
                "sk": assistant_sk,
                "role": "assistant",
                "content": answer,
                "createdAt": timestamp,
            }
        )

        return _response(200, {"prompt": prompt, "answer": answer, "createdAt": timestamp})
    except Exception as exc:
        return _response(500, {"error": "send_message_failed", "detail": str(exc)})
