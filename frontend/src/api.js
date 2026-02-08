const API_BASE = import.meta.env.VITE_API_BASE || "";

export async function createChat(title) {
  const response = await fetch(`${API_BASE}/chats`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title })
  });
  if (!response.ok) {
    throw new Error("No se pudo crear el chat");
  }
  return response.json();
}

export async function listChats() {
  const response = await fetch(`${API_BASE}/chats`);
  if (!response.ok) {
    throw new Error("No se pudo listar los chats");
  }
  return response.json();
}

export async function getChat(chatId) {
  const response = await fetch(`${API_BASE}/chats/${chatId}`);
  if (!response.ok) {
    throw new Error("No se pudo obtener el chat");
  }
  return response.json();
}

export async function sendMessage(chatId, prompt) {
  const response = await fetch(`${API_BASE}/chats/${chatId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt })
  });
  if (!response.ok) {
    throw new Error("No se pudo enviar el mensaje");
  }
  return response.json();
}
