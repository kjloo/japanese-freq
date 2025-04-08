import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';

interface ProcessSettingsProps {
    onVideo: () => void;
    onProcess: () => void;
    onCancel: () => void;
}

const ProcessSettings: FunctionComponent<ProcessSettingsProps> = ({ onVideo, onProcess, onCancel }) => {
    const [inputs, setInputs] = useState<string[]>([]);
    const [selectedInputs, setSelectedInputs] = useState<string[]>([]);
    const [wordCheck, setWordCheck] = useState<boolean>(true);
    const [freqMin, setFreqMin] = useState<number>(2);
    const [requiresDefinition, setRequiresDefinition] = useState<boolean>(true);
    const [minWordLength, setMinWordLength] = useState<number>(1);

    useEffect(() => {
        // Fetch inputs from the API
        const fetchInputs = async () => {
            try {
                const response = await axios.get('/api/io/inputs');
                setInputs(response.data.inputs);
            } catch (error) {
                console.error('Error fetching inputs:', error);
            }
        };

        fetchInputs();
    }, []);

    const handleCheckboxChange = (input: string) => {
        setSelectedInputs((prev) =>
            prev.includes(input)
                ? prev.filter((item) => item !== input) // Remove if already selected
                : [...prev, input] // Add if not selected
        );
    };

    const handleVideoPlayerClick = async () => {
        try {
            onVideo();
            // const response = await axios.post('/api/frequency/video', { inputs: selectedInputs });
            // if (response.status !== 200) {
            //     throw new Error('Failed to start video');
            // }
        } catch (error) {
            console.error('Error starting video:', error);
        }
    };


    const handleProcess = async () => {
        try {
            onProcess();
            const response = await axios.post('/api/frequency/process', { inputs: selectedInputs, word_check: wordCheck, freq_min: freqMin, requires_definition: requiresDefinition, min_word_length: minWordLength });
            if (response.status !== 200) {
                throw new Error('Failed to start process');
            }
        } catch (error) {
            console.error('Error starting process:', error);
        }
    };

    return (
        <div className="card">
            <h2 className="title">Process Settings</h2>
            <div className="settings">
                <div>
                    <label>
                        Word Check:
                        <input
                            type="checkbox"
                            checked={wordCheck}
                            onChange={(e) => setWordCheck(e.target.checked)}
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Frequency Minimum:
                        <input
                            type="number"
                            value={freqMin}
                            onChange={(e) => setFreqMin(Number(e.target.value))}
                            min="1"
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Minimum Word Length:
                        <input
                            type="number"
                            value={minWordLength}
                            onChange={(e) => setMinWordLength(Number(e.target.value))}
                            min="1"
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Requires Definition:
                        <input
                            type="checkbox"
                            checked={requiresDefinition}
                            onChange={(e) => setRequiresDefinition(e.target.checked)}
                        />
                    </label>
                </div>
                <h3 className="title">Select Inputs</h3>
                <ul className="inputs-list">
                    {inputs.map((input) => (
                        <li key={input}>
                            <label>
                                <input
                                    type="checkbox"
                                    value={input}
                                    checked={selectedInputs.includes(input)}
                                    onChange={() => handleCheckboxChange(input)}
                                />
                                {input}
                            </label>
                        </li>
                    ))}
                </ul>
                <button onClick={handleVideoPlayerClick}>Video</button>
                <button onClick={handleProcess}>Process</button>
                <button onClick={onCancel}>Cancel</button>
            </div>
        </div>
    );
};

export default ProcessSettings;