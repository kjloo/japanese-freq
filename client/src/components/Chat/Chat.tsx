import { useState, FunctionComponent, useRef, useEffect } from "react";
import axios from "axios";
import { TTSPlayer } from "./TTSPlayer";
import styles from "./Chat.module.css";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface ChatProps {
  // Add audio state props
  isRecording?: boolean;
  setIsRecording?: (recording: boolean) => void;
}

const AudioInputRecorder: FunctionComponent = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcription, setTranscription] = useState<string>("");
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);

  useEffect(() => {
    return () => {
      if (recorderRef.current?.state !== "inactive") {
        recorderRef.current?.stop();
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      setIsRecording(true);
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
        echoCancellation: true,
      });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm; codecs="opus"',
      });

      const audioChunks: Blob[] = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunks.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        if (audioChunks.length === 0) return;

        const blob = new Blob(audioChunks, {
          type: 'audio/webm; codecs="opus"',
        });
        setAudioBlob(blob);

        // Send to STT endpoint
        try {
          const response = await fetch("/api/speech/stt", {
            method: "POST",
            body: blob,
            headers: {
              "Content-Type": 'audio/webm; codecs="opus"',
            },
          });

          if (response.ok) {
            const data = await response.json();
            setTranscription(data.text || "");
          } else {
            console.error("STT request failed");
            setTranscription("Transcription error");
          }
        } catch (error) {
          console.error("Transcription failed:", error);
          setTranscription("Transcription failed");
        }
      };

      mediaRecorder.start(1500); // 1.5s chunks for better reliability
      recorderRef.current = mediaRecorder;
    } catch (error) {
      console.error("Could not start recording:", error);
      alert("Could not access microphone");
      setIsRecording(false);
    }
  };

  const stopRecording = async () => {
    if (recorderRef.current && recorderRef.current.state === "recording") {
      recorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className={styles.audioRecorder}>
      {isRecording ? (
        <div className={styles.recordingIndicator}>
          <span>🔴 Recording...</span>
          <button onClick={stopRecording} className={styles.stopButton}>
            ⏹ Stop
          </button>
        </div>
      ) : (
        <button
          onClick={startRecording}
          className={[styles.recordButton, !isRecording && styles.active]}
          aria-label="Start recording"
        >
          🎤 Start Recording
        </button>
      )}

      {audioBlob && (
        <div className={styles.transcriptionDisplay}>
          <strong>Transcription:</strong> {transcription}
        </div>
      )}
    </div>
  );
};

const Chat: FunctionComponent<ChatProps> = ({
  isRecording: externalIsRecording,
  setIsRecording: externalSetIsRecording,
  // ...other props
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [speakText, setSpeakText] = useState<string | null>(null);

  // Reset speakText after playback so subsequent identical texts will retrigger.
  useEffect(() => {
    if (speakText) {
      // Clear after a short tick; the TTSPlayer component will handle playback.
      const timer = setTimeout(() => setSpeakText(null), 0);
      return () => clearTimeout(timer);
    }
  }, [speakText]);
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

      // If the LLM response includes a "speak" field, render the TTSPlayer component
      if (response.data.speak) {
        // Render a hidden component that triggers playback via side‑effects.
        setMessages((prev) => [
          ...prev,
          { ...assistantMessage, content: assistantMessage.content },
        ]);
        // After the message is added, render TTSPlayer below the message list.
        // We'll use a temporary state to hold the current speak text.
        setSpeakText(response.data.speak);
      }
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

      {/* Add audio recording controls */}
      <AudioInputRecorder
        isRecording={externalIsRecording}
        setIsRecording={externalSetIsRecording}
      />

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
          <div className={`${styles.message} ${styles.assistant}`}>
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
        {speakText && <TTSPlayer text={speakText} />}
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
