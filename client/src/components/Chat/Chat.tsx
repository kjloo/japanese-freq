import { useState, FunctionComponent, useRef, useEffect } from "react";
import axios from "axios";
import styles from "./Chat.module.css"; // Ensure you import as 'styles' for CSS modules

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const Chat: FunctionComponent = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await axios.post("/api/llm/generate", {
        prompt: input,
        system_prompt: "You are a helpful assistant.",
        max_tokens: 1000,
      });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.data.response || "No response received",
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: unknown) {
      let message = "An unexpected error occurred";

      if (axios.isAxiosError(error)) {
        // Now TypeScript knows 'error' is an AxiosError
        message = error.response?.data?.error || error.message;
      } else if (error instanceof Error) {
        // Handles standard JavaScript errors
        message = error.message;
      }

      const errorMessage: ChatMessage = {
        id: (Date.now() + 2).toString(),
        role: "assistant",
        content: `Error: ${message}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className={styles.chatArea}>
      <h1 className={styles.header}>Chat with AI</h1>

      <div className={styles.chatMessages}>
        {messages.length === 0 && (
          <div className={styles.emptyState}>
            <p>Start a conversation!</p>
          </div>
        )}
        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${message.role === "user" ? styles.user : styles.assistant}`}
          >
            <div className={styles.messageContent}>
              <p>{message.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className={`${styles.message} styles.assistant`}>
            <div className={styles.messageContent}>
              <div className={styles.loadingDots}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.chatInputArea}>
        <input
          className={styles.chatInput}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          disabled={isLoading}
        />
        <button
          className={styles.sendButton}
          onClick={handleSendMessage}
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default Chat;
