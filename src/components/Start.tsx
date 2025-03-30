import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';

const socket = io('http://localhost:5000');

interface StartProps { }

const Start: FunctionComponent<StartProps> = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        // Listen for progress updates from the server
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

        try {
            const response = await axios.post('/api/process', {});
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
            <div className="card">
                <h1 className="title">Welcome</h1>
                <p className="text">Get started by clicking the button below</p>
                <button className="start-button" onClick={startProcess} disabled={isLoading}>
                    {isLoading ? 'Processing...' : 'Start'}
                </button>

                {isLoading && (
                    <div className="progress-bar">
                        <div
                            className="progress-bar-fill"
                            style={{ width: `${progress}%` }}
                        ></div>
                    </div>
                )}
                {progress === 100 && <p>Process complete!</p>}
            </div>
        </div>
    );
};

export default Start;
