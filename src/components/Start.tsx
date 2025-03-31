import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import WordCheckForm from './WordCheckForm';
import WelcomeCard from './WelcomeCard';
import InputSelector from './InputSelector'; // Import the InputSelector component

const socket = io('http://localhost:5000');

// Define an enum to manage the component's state
enum ViewState {
    Welcome,
    InputSelector,
    WordCheckForm,
}

interface StartProps { }

const Start: FunctionComponent<StartProps> = () => {
    const [viewState, setViewState] = useState<ViewState>(ViewState.Welcome); // Single state variable to manage views
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        socket.on('progress', (data) => {
            setProgress(data.progress);
            if (data.progress >= 100) {
                setIsLoading(false);
            }
        });

        socket.on('word_check_complete', () => {
            setViewState(ViewState.Welcome)
        });

        return () => {
            socket.off('progress');
            socket.off('work_check_complete');
        };
    }, []);

    const startProcess = async (selectedInputs: string[]) => {
        setIsLoading(true);
        setProgress(0);

        try {
            const response = await axios.post('/api/frequency/process', { inputs: selectedInputs });
            if (response.status !== 200) {
                throw new Error('Failed to start process');
            }
        } catch (error) {
            console.error('Error starting process:', error);
            setIsLoading(false);
        }
    };

    const handleStartClick = () => {
        setViewState(ViewState.InputSelector); // Show the InputSelector when the Start button is clicked
    };

    const handleInputSelectorSubmit = (selectedInputs: string[]) => {
        setViewState(ViewState.WordCheckForm); // Reset to Welcome while processing
        startProcess(selectedInputs); // Start the process with the selected inputs
    };

    const handleInputSelectorCancel = () => {
        setViewState(ViewState.Welcome); // Reset to Welcome if canceled
    };

    return (
        <div className="container">
            {viewState === ViewState.InputSelector ? (
                <InputSelector
                    onSubmit={handleInputSelectorSubmit}
                    onCancel={handleInputSelectorCancel}
                />
            ) : viewState === ViewState.WordCheckForm ? (
                <WordCheckForm />
            ) : (
                <WelcomeCard
                    isLoading={isLoading}
                    progress={progress}
                    onStart={handleStartClick}
                />
            )}
        </div>
    );
};

export default Start;
