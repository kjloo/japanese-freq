import { useState, useEffect, FunctionComponent } from 'react';
import { io } from 'socket.io-client';
import AnkiCard from './AnkiCard/AnkiCard';
import WordCheckForm from './WordCheckForm';
import WelcomeCard from './WelcomeCard/WelcomeCard';
import ProcessSettings from './ProcessSettings';
import VideoPlayer from './VideoPlayer';

const socket = io('http://localhost:5000');

// Define an enum to manage the component's state
enum ViewState {
    Anki,
    Welcome,
    ProcessSettings,
    WordCheckForm,
    VideoPlayer
}

interface StartProps { }

const Start: FunctionComponent<StartProps> = () => {
    const [viewState, setViewState] = useState<ViewState>(ViewState.Welcome); // Single state variable to manage views
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [videoSource, setVideoSource] = useState<string | null>(null); // State to store the selected video source
    const [settings, setSettings] = useState<Record<string, any>>({});

    useEffect(() => {
        socket.on('progress', (data) => {
            setProgress(data.progress);
            if (data.progress >= 100) {
                setIsLoading(false);
            }
        });

        socket.on('word_check_complete', () => {
            // Hack
            if (viewState !== ViewState.VideoPlayer) {
                setViewState(ViewState.Welcome);
            }
        });

        return () => {
            socket.off('progress');
            socket.off('word_check_complete');
        };
    }, [viewState]);

    const startProcess = () => {
        setIsLoading(true);
        setProgress(0);
    };

    const handleStartClick = () => {
        setViewState(ViewState.ProcessSettings);
    };

    const handleAnkiClick = () => {
        setViewState(ViewState.Anki);
    }

    const handleInputSelectorSubmit = () => {
        setViewState(ViewState.WordCheckForm); // Reset to Welcome while processing
        startProcess(); // Start the process with the selected inputs
    };

    const handleInputSelectorCancel = () => {
        setViewState(ViewState.Welcome); // Reset to Welcome if canceled
    };

    const handleVideoPlayerClick = (source: string, settings: Record<string, any>) => {
        setViewState(ViewState.VideoPlayer);
        setSettings(settings);
        setVideoSource(source);
    };

    return (
        <div className="container">
            {viewState === ViewState.Anki ? (
                <AnkiCard />
            ) : viewState === ViewState.ProcessSettings ? (
                <ProcessSettings
                    onVideo={handleVideoPlayerClick} // Pass the handler to ProcessSettings
                    onProcess={handleInputSelectorSubmit}
                    onCancel={handleInputSelectorCancel}
                />
            ) : viewState === ViewState.WordCheckForm ? (
                <WordCheckForm />
            ) : viewState === ViewState.VideoPlayer && videoSource ? (
                <VideoPlayer source={videoSource} settings={settings} /> // Pass the selected video source to VideoPlayer
            ) : (
                <WelcomeCard
                    isLoading={isLoading}
                    progress={progress}
                    onStart={handleStartClick}
                    onAnki={handleAnkiClick}
                />
            )}
        </div>
    );
};

export default Start;
