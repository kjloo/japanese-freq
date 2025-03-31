import { useState, useEffect, FunctionComponent } from 'react';
import { io } from 'socket.io-client';
import WordCheckForm from './WordCheckForm';
import WelcomeCard from './WelcomeCard';
import ProcessSettings from './ProcessSettings'; // Import the InputSelector component

const socket = io('http://localhost:5000');

// Define an enum to manage the component's state
enum ViewState {
    Welcome,
    ProcessSettings,
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

    const startProcess = () => {
        setIsLoading(true);
        setProgress(0);
    };

    const handleStartClick = () => {
        setViewState(ViewState.ProcessSettings); // Show the InputSelector when the Start button is clicked
    };

    const handleInputSelectorSubmit = () => {
        setViewState(ViewState.WordCheckForm); // Reset to Welcome while processing
        startProcess(); // Start the process with the selected inputs
    };

    const handleInputSelectorCancel = () => {
        setViewState(ViewState.Welcome); // Reset to Welcome if canceled
    };

    return (
        <div className="container">
            {viewState === ViewState.ProcessSettings ? (
                <ProcessSettings
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
