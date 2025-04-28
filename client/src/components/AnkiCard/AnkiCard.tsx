import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';

interface AnkiCardProps {
    onCancel: () => void;
}

const AnkiCard: FunctionComponent<AnkiCardProps> = ({ onCancel }) => {
    const [models, setModels] = useState(new Map<string, number>());
    const [selectedModel, setSelectedModel] = useState<number>(0);
    const [modelSelected, setModelSelected] = useState(false);
    const [modelFields, setModelFields] = useState<string[]>([]);
    const [settingsFields, setSettingsFields] = useState<string[]>([]);

    useEffect(() => {
        // Fetch Anki decks from the API
        const fetchDecks = async () => {
            try {
                const response = await axios.get('/api/anki/models');
                setModels(new Map(Object.entries(response.data.models)));
            } catch (error) {
                console.error('Error fetching Anki models:', error);
            }
        };

        fetchDecks();
    }, []);

    const modelFieldsDropDown = () => {
        return <select>
            {modelFields.map((field, index) => (
                <option key={index} value={field}>
                    {field}
                </option>
            ))}
        </select>;
    }

    const handleDeckChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedDeckName = event.target.value;
        const modelId = models.get(selectedDeckName) || 0;
        setSelectedModel(modelId);
    };

    const handleModelSelect = async () => {
        setModelSelected(true);
        try {
            const response1 = await axios.get(`/api/anki/models/${selectedModel}/fields`);
            setModelFields(response1.data.fields);
            const response2 = await axios.get(`/api/anki/config`);
            setSettingsFields(response2.data.fields);
        } catch (error) {
            console.error('Error fetching Anki model fields:', error);
        }
    }

    return (
        <div className="card">
            <h1 className="title">Anki Settings</h1>
            {!modelSelected ? (<>
                <div>
                    <p className="text">Choose an Anki Deck</p>
                    <select className="deck-select" onChange={handleDeckChange} value={selectedModel}>
                        {Array.from(models.entries()).map(([model, id], index) => (
                            <option key={index} value={model}>
                                {model}
                            </option>
                        ))}
                    </select>
                </div>
                <button onClick={handleModelSelect}>
                    Select Model
                </button>
            </>) : (<>
                <div>
                    <p>Field Configuration</p>
                    {settingsFields.map((field, index) => (
                        <div>
                            <label>
                                {field}
                            </label>
                            {modelFieldsDropDown()}
                        </div>
                    ))}
                </div>
                <button onClick={() => setModelSelected(false)}>
                    Submit
                </button>
            </>)}
            <button onClick={onCancel}>Cancel</button>
        </div >
    );
};

export default AnkiCard;
