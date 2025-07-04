import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';
import commonStyles from '../CommonConfigs.module.css';
import type { AnkiConfig } from '../../types/AnkiTypes'; // Assuming you have a type definition for AnkiConfig

interface AnkiCardProps {
    onCancel: () => void;
}

const AnkiCard: FunctionComponent<AnkiCardProps> = ({ onCancel }) => {
    const [configs, setConfigs] = useState<AnkiConfig[]>([]);
    const [selectedConfig, setSelectedConfig] = useState<string | null>(null);
    const [decks, setDecks] = useState(new Map<string, number>());
    const [configName, setConfigName] = useState<string>('');
    const [selectedDeck, setSelectedDeck] = useState<string>('');
    const [selectedDeckId, setSelectedDeckId] = useState<number>(0);
    const [models, setModels] = useState(new Map<string, number>());
    const [selectedModel, setSelectedModel] = useState<string>('');
    const [selectedModelId, setSelectedModelId] = useState<number>(0);
    const [modelSelected, setModelSelected] = useState(false);
    const [modelFields, setModelFields] = useState<string[]>([]);
    const [settingsFields, setSettingsFields] = useState<string[]>([]);
    const [configFieldsSelected, setConfigFieldsSelected] = useState<Record<string, string>>({});

    useEffect(() => {
        // Fetch Anki decks from the API
        const fetchDecks = async () => {
            try {
                const decksResponse = await axios.get('/api/anki/decks');
                const deckMap: [string, number][] = Object.entries(decksResponse.data.decks);
                setDecks(new Map(deckMap));
                const [deckFirstKey, deckFirstValue] = deckMap[0];
                setSelectedDeck(deckFirstKey);
                setSelectedDeckId(deckFirstValue);

                const modelsResponse = await axios.get('/api/anki/models');
                const modelMap: [string, number][] = Object.entries(modelsResponse.data.models);
                setModels(new Map(modelMap));
                const [modelFirstKey, modelFirstValue] = modelMap[0];
                setSelectedModel(modelFirstKey);
                setSelectedModelId(modelFirstValue);
            } catch (error) {
                console.error('Error fetching Anki models:', error);
            }
        };
        const fetchConfigs = async () => {
            try {
                const response = await axios.get('/api/anki/configs');
                setConfigs(response.data.configs);
                setSelectedConfig(response.data.configs.length > 0 ? response.data.configs[0]._id : '');
            } catch (error) {
                console.error('Error fetching configs:', error);
            }
        };
        fetchDecks();
        fetchConfigs();
    }, []);

    useEffect(() => {
        const fetchModelFieldsAndSettings = async () => {
            if (modelSelected && selectedModelId) {
                try {
                    const ankiResp = await axios.get(`/api/anki/models/${selectedModelId}/fields`);
                    setModelFields(ankiResp.data.fields);
                    const appSettings = await axios.get(`/api/anki/configs/fields`);
                    setSettingsFields(appSettings.data.fields);
                } catch (error) {
                    console.error('Error fetching Anki model fields:', error);
                }
            }
        };
        fetchModelFieldsAndSettings();
    }, [modelSelected, selectedModelId]);

    const settingsFieldsDropDown = (field: string) => {
        return (
            <select
                className={commonStyles.configSelect}
                onChange={(e) => handleFieldChange(field, e.target.value)}
                value={configFieldsSelected[field] || ""}
                name={settingsFields[0]}
            >
                <option value="">Select...</option>
                {settingsFields.map((optionField, index) => (
                    <option key={index} value={optionField}>
                        {optionField}
                    </option>
                ))}
            </select>
        );
    }

    const handleDeckChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedDeckName = event.target.value;
        const deckId = decks.get(selectedDeckName) || 0;
        setSelectedDeck(selectedDeckName);
        setSelectedDeckId(deckId);
    };

    const handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const selectedModelName = event.target.value;
        const modelId = models.get(selectedModelName) || 0;
        setSelectedModel(selectedModelName);
        setSelectedModelId(modelId);
    };

    const handleModelSelect = async () => {
        setModelSelected(true);
    }

    const handleFieldChange = (field: string, value: string) => {
        setConfigFieldsSelected(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleConfigSubmit = async () => {
        try {
            const configJson = {
                deck_id: selectedDeckId,
                name: configName,
                deck_name: selectedDeck,
                model_name: selectedModel,
                settings: configFieldsSelected
            };
            await axios.post('/api/anki/configs', configJson);
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
                <div className={commonStyles.configContainer}>
                    <div className={commonStyles.configRow}>
                        <label className={commonStyles.configLabel}>Configuration Name</label>
                        {selectedConfig === '' ? (
                            <input
                                type="text"
                                className={commonStyles.configInput}
                                value={configName}
                                onChange={(e) => setConfigName(e.target.value)}
                                placeholder="Enter configuration name"
                            />
                        ) : (
                            <select className={commonStyles.configInput} onChange={(e) => setSelectedConfig(e.target.value)} value={selectedConfig || ''}>
                                {configs.map((config) => (
                                    <option key={config._id} value={config._id}>
                                        {config.name}
                                    </option>
                                ))}
                                <option value="">Create New Configuration</option>
                            </select>
                        )}
                    </div>
                    <h2 className="subtitle">Choose an Anki Deck</h2>
                    <div className={commonStyles.configRow}>
                        <label className={commonStyles.configLabel}>Deck</label>
                        <select className={commonStyles.configSelect} onChange={handleDeckChange} value={selectedDeck}>
                            {Array.from(decks.entries()).map(([deck], index) => (
                                <option key={index} value={deck}>
                                    {deck}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className={commonStyles.configRow}>
                        <label className={commonStyles.configLabel}>Model</label>
                        <select className={commonStyles.configSelect} onChange={handleModelChange} value={selectedModel}>
                            {Array.from(models.entries()).map(([model], index) => (
                                <option key={index} value={model}>
                                    {model}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
                <button onClick={handleModelSelect}>
                    Select Model
                </button>
            </>) : (<>
                <div className={commonStyles.configContainer}>
                    <h2 className='subtitle'>Field Configuration</h2>
                    <div className={commonStyles.configScrollable}>
                        {modelFields.map((field, index) => (
                            <div className={commonStyles.configRow} key={index}>
                                <label className={commonStyles.configLabel}>
                                    {field}
                                </label>
                                {settingsFieldsDropDown(field)}
                            </div>
                        ))}
                    </div>
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
