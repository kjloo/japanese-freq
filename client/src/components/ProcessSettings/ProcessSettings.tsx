import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';
import commonStyles from '../CommonConfigs.module.css';

export type ProcessVideoSettings = {
    inputs: string[];
    word_check: boolean;
    freq_min: number;
    requires_definition: boolean;
    min_word_length: number;
};

type AnkiConfig = {
    name: string;
}

export const defaultProcessVideoSettings = (): ProcessVideoSettings => ({
    inputs: [],
    word_check: true,
    freq_min: 1,
    requires_definition: false,
    min_word_length: 2,
});

interface ProcessSettingsProps {
    onVideo: (video: string, settings: ProcessVideoSettings) => void;
    onProcess: () => void;
    onCancel: () => void;
}

const ProcessSettings: FunctionComponent<ProcessSettingsProps> = ({ onVideo, onProcess, onCancel }) => {
    const [inputs, setInputs] = useState<string[]>([]);
    const [selectedInputs, setSelectedInputs] = useState<string[]>([]);
    const [configs, setConfigs] = useState<AnkiConfig[]>([]);
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
        const fetchConfigs = async () => {
            try {
                const response = await axios.get('/api/anki/configs');
                setConfigs(response.data.configs);
            } catch (error) {
                console.error('Error fetching configs:', error);
            }
        }

        fetchInputs();
        fetchConfigs();
    }, []);

    const handleCheckboxChange = (input: string) => {
        setSelectedInputs((prev) =>
            prev.includes(input)
                ? prev.filter((item) => item !== input) // Remove if already selected
                : [...prev, input] // Add if not selected
        );
    };

    const handlePlayVideo = () => {
        if (selectedInputs.length > 0) {
            const video = selectedInputs[0]; // Use the first element in selectedInputs
            onVideo(video, {
                inputs: selectedInputs,
                word_check: wordCheck,
                freq_min: freqMin,
                requires_definition: requiresDefinition,
                min_word_length: minWordLength,
            });
        } else {
            console.error('No video selected. Please select an input.');
        }
    };

    const handleProcess = async () => {
        try {
            onProcess();
            const response = await axios.post('/api/frequency/process', {
                inputs: selectedInputs,
                word_check: wordCheck,
                freq_min: freqMin,
                requires_definition: requiresDefinition,
                min_word_length: minWordLength,
            });
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
                    <label className={commonStyles.configLabel}>
                        Word Check:
                        <input
                            type="checkbox"
                            checked={wordCheck}
                            onChange={(e) => setWordCheck(e.target.checked)}
                        />
                    </label>
                </div>
                <div>
                    <label className={commonStyles.configLabel}>
                        Frequency Minimum:
                        <input className={commonStyles.configInput}
                            type="number"
                            value={freqMin}
                            onChange={(e) => setFreqMin(Number(e.target.value))}
                            min="1"
                        />
                    </label>
                </div>
                <div>
                    <label className={commonStyles.configLabel}>
                        Minimum Word Length:
                        <input className={commonStyles.configInput}
                            type="number"
                            value={minWordLength}
                            onChange={(e) => setMinWordLength(Number(e.target.value))}
                            min="1"
                        />
                    </label>
                </div>
                <div>
                    <label className={commonStyles.configLabel}>
                        Requires Definition:
                        <input
                            type="checkbox"
                            checked={requiresDefinition}
                            onChange={(e) => setRequiresDefinition(e.target.checked)}
                        />
                    </label>
                </div>
                <div>
                    <label className={commonStyles.configLabel}>
                        Anki Config:
                        <select className={commonStyles.configInput} onChange={(e) => setSelectedInputs([e.target.value])}>
                            <option value="">Select Config</option>
                            {configs.map((config) => (
                                <option key={config.name} value={config.name}>
                                    {config.name}
                                </option>
                            ))}
                        </select>
                    </label>
                </div>
                <h3 className="title">Select Inputs</h3>
                <ul className={commonStyles.configInputsList}>
                    {inputs.map((input) => (
                        <li key={input}>
                            <label className={commonStyles.configLabel}>
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
                <button onClick={handlePlayVideo}>Play Video</button>
                <button onClick={handleProcess}>Process</button>
                <button onClick={onCancel}>Cancel</button>
            </div>
        </div>
    );
};

export default ProcessSettings;
