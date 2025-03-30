import { useState, useEffect, FunctionComponent } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:5000');

interface WordData {
    word: string;
    definition: string;
}

interface WordCheckFormProps { }

const WordCheckForm: FunctionComponent<WordCheckFormProps> = () => {
    const [wordData, setWordData] = useState<WordData | null>(null);

    useEffect(() => {
        // Listen for the "word_check" event from the server
        socket.on('word_check', (data: WordData) => {
            setWordData(data);
        });

        return () => {
            socket.off('word_check');
        };
    }, []);

    const handleResponse = (answer: boolean) => {
        if (wordData) {
            // Emit the response back to the server
            socket.emit('response', { word: wordData.word, answer });
            // Clear the current word data after submitting the response
            setWordData(null);
        }
    };

    return (
        <div>
            {wordData ? (
                <div>
                    <h2>Word Check</h2>
                    <p><strong>Word:</strong> {wordData.word}</p>
                    <p><strong>Definition:</strong> {wordData.definition}</p>
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