import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import WordCheckForm from './WordCheckForm';
import WelcomeCard from './WelcomeCard'; // Import the new WelcomeCard component

const socket = io('http://localhost:5000');

interface StartProps { }

const Start: FunctionComponent<StartProps> = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [showWordCheckForm, setShowWordCheckForm] = useState(false);

    useEffect(() => {
        socket.on('progress', (data) => {
            setProgress(data.progress);
            if (data.progress >= 100) {
                setIsLoading(false);
            }
        });

        return () => {
            socket.off('progress');
        };
    }, []);

    const startProcess = async () => {
        setIsLoading(true);
        setProgress(0);
        setShowWordCheckForm(true);

        try {
            const response = await axios.post('/api/frequency/process', {});
            if (response.status !== 200) {
                throw new Error('Failed to start process');
            }
        } catch (error) {
            console.error('Error starting process:', error);
            setIsLoading(false);
        }
    };

    return (
        <div className="container">
            {showWordCheckForm ? (
                <WordCheckForm />
            ) : (
                <WelcomeCard
                    isLoading={isLoading}
                    progress={progress}
                    onStart={startProcess}
                />
            )}
        </div>
    );
};

export default Start;
