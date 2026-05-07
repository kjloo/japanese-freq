import React, { FunctionComponent, useState, useRef, useEffect } from "react";
import styles from "./AudioRecorder.module.css";

interface AudioRecorderProps {
  isRecording: boolean;
  setIsRecording: (recording: boolean) => void;
}

const AudioRecorder: FunctionComponent<AudioRecorderProps> = ({
  isRecording,
  setIsRecording,
}) => {
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

      mediaRecorder.start(1500);
      recorderRef.current = mediaRecorder;
    } catch (error) {
      console.error("Could not start recording:", error);
      alert("Could not access microphone");
      setIsRecording(false);
    }
  };

  const stopRecording = async () => {
    if (
      recorderRef.current &&
      recorderRecoderRef.current.state === "recording"
    ) {
      recorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className={styles.audioRecorder}>
      {isRecording ? (
        <div className={styles.recordingIndicator}>
          <span className={styles.recordingDot}>🔴</span>
          <span className={styles.recordingText}>Recording...</span>
          <button onClick={stopRecording} className={styles.stopButton}>
            ⏹ Stop
          </button>
        </div>
      ) : (
        <button
          onClick={startRecording}
          className={`${styles.recordButton} ${!isRecording && styles.active}`}
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

export default AudioRecorder;
