import { useEffect } from "react";

interface TTSPlayerProps {
  /**
   * Japanese text that should be synthesized and played.
   */
  text: string;
}

/**
 * Fetches synthesized speech from the backend and plays it.
 * The component is side‑effect only – it renders null.
 */
export const TTSPlayer: React.FC<TTSPlayerProps> = ({ text }) => {
  useEffect(() => {
    const play = async () => {
      try {
        const response = await fetch("/api/speech/tts", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, language: "Japanese" }),
        });
        if (!response.ok) {
          console.error("TTS request failed");
          return;
        }
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        // Play the audio; swallow any playback errors.
        audio.play().catch((e) => console.error("Audio play error", e));
        // Clean up the object URL once playback finishes.
        audio.onended = () => URL.revokeObjectURL(audioUrl);
      } catch (err) {
        console.error("Error in TTSPlayer", err);
      }
    };
    play();
    // No cleanup needed – the audio element handles its own lifecycle.
  }, [text]);

  // The component does not render any DOM.
  return null;
};
