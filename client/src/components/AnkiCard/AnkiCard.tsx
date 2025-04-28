import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';

interface AnkiCardProps {
    onCancel: () => void;
}

const AnkiCard: FunctionComponent<AnkiCardProps> = ({ onCancel }) => {
    const [models, setModels] = useState(new Map<string, number>());
    const [selectedModel, setSelectedModel] = useState<number>(0);
    const [modelSelected, setModelSelected] = useState(false);
    const [fields, setFields] = useState<string[]>([]);

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

    const handleDeckChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedDeckName = event.target.value;
        const modelId = models.get(selectedDeckName) || 0;
        setSelectedModel(modelId);
    };

    const handleModelSelect = async () => {
        setModelSelected(true);
        try {
            const response = await axios.get(`/api/anki/models/${selectedModel}/fields`);
            setFields(response.data.fields);
        } catch (error) {
            console.error('Error fetching Anki model fields:', error);
        }
    }

    return (
        <div className="card">
            <h1 className="title">Anki Settings</h1>
            {!modelSelected ? (<>
                <p className="text">Choose an Anki Deck</p>
                <select className="deck-select" onChange={handleDeckChange} value={selectedModel}>
                    {Array.from(models.entries()).map(([model, id], index) => (
                        <option key={index} value={model}>
                            {model}
                        </option>
                    ))}
                </select>
                <button onClick={handleModelSelect}>
                    Select Model
                </button>
            </>
            ) : (
                <div>
                    <h2>Selected Model: {Array.from(models.keys())[selectedModel]}</h2>
                    <p>Fields:</p>
                    <ul>
                        {fields.map((field, index) => (
                            <li key={index}>{field}</li>
                        ))}
                    </ul>
                </div>
            )}
            <button onClick={onCancel}>Cancel</button>
        </div >
    );
};

export default AnkiCard;
