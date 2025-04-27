import { FunctionComponent } from 'react';

interface AnkiCardProps {
}

const AnkiCard: FunctionComponent<AnkiCardProps> = ({ }) => {
    return (
        <div className="card">
            <h1 className="title">Anki Settings</h1>
            <p className="text">Choose an Anki Deck</p>
        </div>
    );
};

export default AnkiCard;
