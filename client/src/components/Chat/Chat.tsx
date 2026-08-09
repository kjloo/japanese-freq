import { useState, FunctionComponent, useRef, useEffect } from "react";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faMicrophone, faCircleNotch } from "@fortawesome/free-solid-svg-icons";
import styles from "./Chat.module.css";
import { TTSPlayer } from "./TTSPlayer";
import FuriganaMessage from "./FuriganaMessage";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  isAssistant: boolean;
  audio?: string; // base64 encoded MP3 audio
}

const Chat: FunctionComponent = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    return () => {
      // Cleanup on unmount
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
        echoCancellation: true,
        noiseSuppression: true,
      });

      streamRef.current = stream;
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: "audio/webm",
      });

      const audioChunks: Blob[] = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunks.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(audioChunks, {
          type: "audio/webm",
        });

        try {
          const response = await fetch("/api/speech/stt", {
            method: "POST",
            body: blob,
          });

          if (response.ok) {
            const data = await response.json();
            const transcribedText = data.text || "";
            setTranscription(transcribedText);

            // Process through assistant
            await processMessage(transcribedText);
          }
        } catch (error) {
          console.error("STT processing failed:", error);
        } finally {
          setIsRecording(false);
        }
      };

      mediaRecorder.start(3000); // Send chunks every 3 seconds
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = audioChunks;
      setIsRecording(true);
    } catch (error) {
      console.error("Could not access microphone:", error);
      alert("Could not access microphone. Please allow microphone access.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      }
    }
  };

  const processMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: text,
      isAssistant: false,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await axios.post("/api/chat/message", {
        text: text,
      });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.data.response || "No response received",
        isAssistant: true,
        audio: response.data.audio, // base64 audio from server
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: unknown) {
      let message = "An unexpected error occurred";

      if (axios.isAxiosError(error)) {
        message = error.response?.data?.error || error.message;
      } else if (error instanceof Error) {
        message = error.message;
      }

      const errorMessage: ChatMessage = {
        id: (Date.now() + 2).toString(),
        role: "assistant",
        content: `Error: ${message}`,
        isAssistant: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      isAssistant: false,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await axios.post("/api/chat/message", {
        text: input,
      });

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.data.response || "No response received",
        isAssistant: true,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: unknown) {
      let message = "An unexpected error occurred";

      if (axios.isAxiosError(error)) {
        message = error.response?.data?.error || error.message;
      } else if (error instanceof Error) {
        message = error.message;
      }

      const errorMessage: ChatMessage = {
        id: (Date.now() + 2).toString(),
        role: "assistant",
        content: `Error: ${message}`,
        isAssistant: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className={styles.chatArea}>
      <h1 className={styles.header}>📱 Chat with AI</h1>

      {/* Chat Messages Area - Above Input */}
      <div className={styles.chatMessages}>
        {messages.length === 0 && (
          <div className={styles.emptyState}>
            <p>Start a conversation!</p>
          </div>
        )}
        {messages.map((message) => (
          <div
            key={message.id}
            className={`${styles.message} ${
              message.isAssistant ? styles.assistant : styles.user
            }`}
          >
            <div className={styles.messageContent}>
              <FuriganaMessage text={message.content} />
              {message.isAssistant && message.audio && (
                <TTSPlayer audio={message.audio} />
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className={`${styles.message} ${styles.assistant}`}>
            <div className={styles.messageContent}>
              <FontAwesomeIcon icon={faCircleNotch} spin />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Recording Indicator - Visible while recording */}
      {isRecording && (
        <div className={styles.recordingIndicator}>
          <span className={styles.recordingDot}></span>
          <span>Recording...</span>
        </div>
      )}

      {/* Input Area with Microphone Button - Bottom */}
      <div className={styles.chatInputArea}>
        {/* Single Microphone Toggle Button */}
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`${styles.micButton} ${isRecording ? styles.recording : ""}`}
          aria-label={isRecording ? "Stop recording" : "Start recording"}
          disabled={isLoading}
        >
          <FontAwesomeIcon icon={faMicrophone} />
        </button>

        {/* Text Input */}
        <input
          className={styles.chatInput}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={isLoading}
        />

        {/* Send Button */}
        <button
          className={styles.sendButton}
          onClick={handleSendMessage}
          disabled={!input.trim() || isLoading}
        >
          {isLoading ? "..." : "Send"}
        </button>
      </div>

      {/* Transcription Display - Shows what user said */}
      {transcription && !isRecording && (
        <div className={styles.transcriptionDisplay}>
          <strong>You said:</strong> {transcription}
        </div>
      )}
    </div>
  );
};

export default Chat;
