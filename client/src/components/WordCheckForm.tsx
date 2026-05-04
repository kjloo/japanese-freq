import { useState, useEffect, FunctionComponent, useCallback } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

interface WordDefinition {
  definition: string;
  kanji: string;
  hiragana: string;
  romaji: string;
}

interface WordData {
  word: string;
  frequency: number;
  definition: WordDefinition;
}

const WordCheckForm: FunctionComponent = () => {
  const [wordData, setWordData] = useState<WordData | null>(null);

  useEffect(() => {
    socket.on("word_check", (data: WordData) => {
      setWordData(data);
    });
    return () => {
      socket.off("word_check");
    };
  }, []);

  useEffect(() => {
    // Add key press listeners
    const handleKeyPress = (event: KeyboardEvent) => {
      console.log("Key pressed:", event.key);
      if (event.key === "y") {
        handleResponse(true);
      } else if (event.key === "n") {
        handleResponse(false);
      }
    };

    window.addEventListener("keydown", handleKeyPress);

    return () => {
      window.removeEventListener("keydown", handleKeyPress);
    };
  }, [handleResponse]);

  const handleResponse = useCallback(
    (answer: boolean) => {
      if (wordData) {
        socket.emit("word_response", { word: wordData.word, answer });
        setWordData(null);
      }
    },
    [wordData],
  );

  return (
    <div>
      {wordData ? (
        <div className="card">
          <h2 className="title">Word Check</h2>
          <p>
            <strong>Frequency:</strong> {wordData.frequency}
          </p>
          <p>
            <strong>Word:</strong> {wordData.word}
          </p>
          <p>
            <strong>Definition:</strong> {wordData.definition.definition}
          </p>
          <p>
            <strong>Kanji:</strong> {wordData.definition.kanji}
          </p>
          <p>
            <strong>Hiragana:</strong> {wordData.definition.hiragana}
          </p>
          <p>
            <strong>Romaji:</strong> {wordData.definition.romaji}
          </p>
          <button onClick={() => handleResponse(true)}>Yes</button>
          <button onClick={() => handleResponse(false)}>No</button>
        </div>
      ) : (
        <p>Waiting for a word...</p>
      )}
    </div>
  );
};

export default WordCheckForm;
