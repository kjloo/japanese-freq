import { useState } from 'react';
import axios from 'axios';

interface StartProps { }

const Start: React.FunctionComponent<StartProps> = () => {
    // State variables to manage loading and completion state
    const [loading, setLoading] = useState(false);
    const [complete, setComplete] = useState(false);

    // Function to handle the button click
    const handleStartClick = async () => {
        setLoading(true); // Start loading
        setComplete(false); // Reset complete state

        try {
            // Make the POST request to /api/process
            await axios.post('/api/process');

            // On success, update the state to show completion screen
            setComplete(true);
        } catch (error) {
            // Handle error (you could show an error message here)
            console.error("Error during POST request", error);
        } finally {
            setLoading(false); // End loading regardless of success or error
        }
    };

    return (
        <div className="container">
            <div className="card">
                <h1 className="title">Welcome</h1>
                <p className="text">Get started by clicking the button below</p>

                {!loading && !complete && (
                    <button className="start-button" onClick={handleStartClick}>Start</button>
                )}

                {loading && (
                    <div className="loading">
                        <p>Loading...</p>
                        {/* You can replace the text with an actual loading spinner */}
                        <div className="spinner"></div>
                    </div>
                )}

                {complete && (
                    <div className="complete">
                        <p>Process Complete!</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Start;
