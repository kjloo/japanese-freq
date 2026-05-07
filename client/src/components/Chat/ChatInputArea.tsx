import React, { FunctionComponent } from "react";
import styles from "./ChatInputArea.module.css";

interface ChatInputAreaProps {
  input: string;
  setInput: (value: string) => void;
  handleSend: () => void;
  isLoading: boolean;
}

const ChatInputArea: FunctionComponent<ChatInputAreaProps> = ({
  input,
  setInput,
  handleSend,
  isLoading,
}) => {
  return (
    <div className={styles.chatInputArea}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        disabled={isLoading}
      />
      <button
        className={styles.sendButton}
        onClick={handleSend}
        disabled={!input.trim() || isLoading}
      >
        {isLoading ? "..." : "Send"}
      </button>
    </div>
  );
};

export default ChatInputArea;
