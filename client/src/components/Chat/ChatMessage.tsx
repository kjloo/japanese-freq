import React, { FunctionComponent } from "react";
import styles from "./ChatMessage.module.css";

interface ChatMessageProps {
  id: string;
  role: "user" | "assistant";
  content: string;
}

const ChatMessage: FunctionComponent<ChatMessageProps> = ({
  role,
  content,
}) => {
  return (
    <div
      className={`${styles.message} ${role === "user" ? styles.user : styles.assistant}`}
    >
      <div className={styles.messageContent}>
        <p>{content}</p>
      </div>
    </div>
  );
};

export default ChatMessage;
