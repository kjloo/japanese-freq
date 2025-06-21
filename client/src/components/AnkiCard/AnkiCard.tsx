import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';
import styles from './AnkiCard.module.css';

interface AnkiCardProps {
    onCancel: () => void;
}

const AnkiCard: FunctionComponent<AnkiCardProps> = ({ onCancel }) => {
    const [models, setModels] = useState(new Map<string, number>());
    const [selectedModel, setSelectedModel] = useState<number>(0);
    const [modelSelected, setModelSelected] = useState(false);
    const [modelFields, setModelFields] = useState<string[]>([]);
    const [settingsFields, setSettingsFields] = useState<string[]>([]);
    const [configFieldsSelected, setConfigFieldsSelected] = useState<{ [key: string]: string }>({});

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
        return <select className={styles.configSelect} onChange={(e) => handleFieldChange(e.target.name, e.target.value)} name={modelFields[0]}>
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
            const ankiResp = await axios.get(`/api/anki/models/${selectedModel}/fields`);
            setModelFields(ankiResp.data.fields);
            const appSettings = await axios.get(`/api/anki/config`);
            setSettingsFields(appSettings.data.fields);
        } catch (error) {
            console.error('Error fetching Anki model fields:', error);
        }
    }

    const handleFieldChange = (field: string, value: string) => {
        setConfigFieldsSelected(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleConfigSubmit = async () => {
        try {
            await axios.post('/api/anki/config', {
                modelId: selectedModel,
                config: configFieldsSelected
            });
            console.log('Configuration saved successfully');
            onCancel();
        } catch (error) {
            console.error('Error saving Anki configuration:', error);
        }
    };

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
                <div className={styles.configContainer}>
                    <h2 className='subtitle'>Field Configuration</h2>
                    {settingsFields.map((field, index) => (
                        <div className={styles.configRow} key={index}>
                            <label className={styles.configLabel}>
                                {field}
                            </label>
                            {modelFieldsDropDown()}
                        </div>
                    ))}
                </div>
                <button onClick={handleConfigSubmit}>
                    Submit
                </button>
            </>)}
            <button onClick={onCancel}>Cancel</button>
        </div >
    );
};

export default AnkiCard;
