import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';

interface AnkiCardProps {
}

const AnkiCard: FunctionComponent<AnkiCardProps> = ({ }) => {
    const [decks, setDecks] = useState(new Map<string, number>());

    useEffect(() => {
        // Fetch Anki decks from the API
        const fetchDecks = async () => {
            try {
                const response = await axios.get('/api/anki/decks');
                setDecks(new Map(Object.entries(response.data.decks)));
            } catch (error) {
                console.error('Error fetching Anki decks:', error);
            }
        };

        fetchDecks();
    }, []);


    return (
        <div className="card">
            <h1 className="title">Anki Settings</h1>
            <p className="text">Choose an Anki Deck</p>
            <select className="deck-select">
                {Array.from(decks.entries()).map(([deck, id]) => (
                    <option key={id} value={deck}>
                        {deck}
                    </option>
                ))}
            </select>
        </div>
    );
};

export default AnkiCard;
