import React, { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import { createChat, getChat, listChats, sendMessage } from "./api.js";

const emptyChat = {
  chatId: "",
  title: "",
  createdAt: "",
  messages: []
};

export default function App() {
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(emptyChat);
  const [messageInput, setMessageInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const sortedChats = useMemo(() => {
    return [...chats].sort((a, b) => (b.createdAt || "").localeCompare(a.createdAt || ""));
  }, [chats]);

  useEffect(() => {
    loadChats();
  }, []);

  async function loadChats() {
    try {
      setError("");
      const data = await listChats();
      setChats(data.chats || []);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleCreateChat() {
    const title = window.prompt("Titulo del chat:") || "Nuevo chat";
    try {
      setError("");
      const data = await createChat(title);
      setChats((prev) => [data, ...prev]);
      await handleSelectChat(data.chatId);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleSelectChat(chatId) {
    try {
      setError("");
      const data = await getChat(chatId);
      setActiveChat({
        chatId: data.chat?.chatId || chatId,
        title: data.chat?.title || "Chat",
        createdAt: data.chat?.createdAt || "",
        messages: data.messages || []
      });
      setIsSidebarOpen(false);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleSendMessage(event) {
    event.preventDefault();
    if (!activeChat.chatId || !messageInput.trim()) {
      return;
    }

    const userMessage = {
      role: "user",
      content: messageInput,
      createdAt: new Date().toISOString()
    };

    setMessageInput("");
    setLoading(true);
    setActiveChat((prev) => ({
      ...prev,
      messages: [...prev.messages, userMessage]
    }));

    try {
      const data = await sendMessage(activeChat.chatId, userMessage.content);
      const assistantMessage = {
        role: "assistant",
        content: data.answer,
        createdAt: data.createdAt
      };

      setActiveChat((prev) => ({
        ...prev,
        messages: [...prev.messages, assistantMessage]
      }));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <aside className={`sidebar ${isSidebarOpen ? "open" : ""}`}>
        <div className="sidebar-header">
          <h1>Agente IA</h1>
          <button type="button" className="primary" onClick={handleCreateChat}>
            Nuevo chat
          </button>
        </div>
        <div className="chat-list">
          {sortedChats.map((chat) => (
            <button
              key={chat.chatId}
              type="button"
              className={`chat-item ${chat.chatId === activeChat.chatId ? "active" : ""}`}
              onClick={() => handleSelectChat(chat.chatId)}
            >
              <span className="chat-title">{chat.title}</span>
              <span className="chat-date">{new Date(chat.createdAt).toLocaleDateString()}</span>
            </button>
          ))}
          {!sortedChats.length && (
            <p className="empty">Crea tu primer chat para empezar.</p>
          )}
        </div>
      </aside>

      <main className="chat-area">
        <header className="chat-header">
          <button
            type="button"
            className="ghost"
            onClick={() => setIsSidebarOpen((prev) => !prev)}
          >
            Menu
          </button>
          <div>
            <h2>{activeChat.title || "Selecciona un chat"}</h2>
            <p>Memoria activa con DynamoDB y Groq</p>
          </div>
        </header>

        <section className="chat-messages">
          {activeChat.messages.map((message, index) => (
            <div key={`${message.role}-${index}`} className={`message ${message.role}`}>
              <div className="bubble">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            </div>
          ))}
          {!activeChat.messages.length && (
            <div className="message assistant">
              <div className="bubble">
                <ReactMarkdown>
                  {"Hola! Crea un chat y envia tu primer prompt para comenzar."}
                </ReactMarkdown>
              </div>
            </div>
          )}
        </section>

        <form className="chat-input" onSubmit={handleSendMessage}>
          <input
            type="text"
            placeholder="Escribe tu prompt..."
            value={messageInput}
            onChange={(event) => setMessageInput(event.target.value)}
            disabled={!activeChat.chatId || loading}
          />
          <button type="submit" className="primary" disabled={loading || !messageInput.trim()}>
            {loading ? "Enviando..." : "Enviar"}
          </button>
        </form>

        {error && <div className="error">{error}</div>}
      </main>
    </div>
  );
}
