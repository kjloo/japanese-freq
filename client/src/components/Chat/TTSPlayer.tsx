import { useEffect } from "react";

interface TTSPlayerProps {
  /**
   * Japanese text that should be synthesized and played.
   * If provided, the component will call the TTS API.
   */
  text?: string;
  /**
   * Pre-fetched base64 encoded audio to play directly.
   * If provided, the component will play this audio without calling the API.
   */
  audio?: string;
}

/**
 * Fetches synthesized speech from the backend and plays it.
 * The component is side‑effect only – it renders null.
 */
export const TTSPlayer: React.FC<TTSPlayerProps> = ({ text, audio }) => {
  useEffect(() => {
    const play = async () => {
      try {
        let audioBlob: Blob;

        if (audio) {
          // Play pre-fetched base64 audio
          const binaryString = atob(audio);
          const len = binaryString.length;
          const bytes = new Uint8Array(len);
          for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
          }
          audioBlob = new Blob([bytes], { type: "audio/mp3" });
        } else if (text) {
          // Fetch audio from TTS API
          const response = await fetch("/api/speech/tts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, language: "Japanese" }),
          });
          if (!response.ok) {
            console.error("TTS request failed");
            return;
          }
          audioBlob = await response.blob();
        } else {
          // Neither text nor audio provided
          return;
        }

        const audioUrl = URL.createObjectURL(audioBlob);
        const audioElement = new Audio(audioUrl);
        // Play the audio; swallow any playback errors.
        audioElement.play().catch((e) => console.error("Audio play error", e));
        // Clean up the object URL once playback finishes.
        audioElement.onended = () => URL.revokeObjectURL(audioUrl);
      } catch (err) {
        console.error("Error in TTSPlayer", err);
      }
    };
    play();
    // No cleanup needed – the audio element handles its own lifecycle.
  }, [text, audio]);

  // The component does not render any DOM.
  return null;
};
