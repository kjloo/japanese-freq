import { FunctionComponent } from 'react';

interface WelcomeCardProps {
    isLoading: boolean;
    progress: number;
    onStart: () => void;
}

const WelcomeCard: FunctionComponent<WelcomeCardProps> = ({ isLoading, progress, onStart }) => {
    return (
        <div className="card">
            <h1 className="title">Welcome</h1>
            <p className="text">Get started by clicking the button below</p>
            <button className="start-button" onClick={onStart} disabled={isLoading}>
                {isLoading ? 'Processing...' : 'Start'}
            </button>

            {isLoading && (
                <div className="progress-bar">
                    <div
                        className="progress-bar-fill"
                        style={{ width: `${progress}%` }}
                    ></div>
                </div>
            )}
            {progress === 100 && <p>Process complete!</p>}
        </div>
    );
};

export default WelcomeCard;