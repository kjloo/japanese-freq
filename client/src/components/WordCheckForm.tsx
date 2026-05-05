import {
  useState,
  useEffect,
  FunctionComponent,
  useCallback,
  useRef,
} from "react";
import { io, Socket } from "socket.io-client";

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
  const socketRef = useRef<Socket | null>(null);

  useEffect(() => {
    const socket = io("http://localhost:5000");
    socketRef.current = socket;

    socket.on("word_check", (data: WordData) => {
      setWordData(data);
    });

    return () => {
      socket.off("word_check");
      socket.disconnect();
    };
  }, []);

  const handleResponse = useCallback(
    (answer: boolean) => {
      if (wordData && socketRef.current) {
        socketRef.current.emit("word_response", {
          word: wordData.word,
          answer,
        });
        setWordData(null);
      }
    },
    [wordData],
  );

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      if (event.key === "y") {
        handleResponse(true);
      } else if (event.key === "n") {
        handleResponse(false);
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [handleResponse]);

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
