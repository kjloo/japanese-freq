import { FunctionComponent } from 'react';
import styles from './WelcomeCard.module.css';

interface WelcomeCardProps {
    isLoading: boolean;
    progress: number;
    onStart: () => void;
    onAnki: () => void;
}

const WelcomeCard: FunctionComponent<WelcomeCardProps> = ({ isLoading, progress, onStart, onAnki }) => {
    return (
        <div className="card">
            <button className={styles.ankiButton} onClick={onAnki} >⚙️</button>
            <h1 className="title">Welcome</h1>
            <p className="text">Get started by clicking the button below</p>
            <button className="start-button" onClick={onStart} disabled={isLoading}>
                {isLoading ? 'Processing...' : 'Start'}
            </button>

            {isLoading && (
                <div className={styles.progressBar}>
                    <div
                        className={styles.progressBarFill}
                        style={{ width: `${progress}%` }}
                    ></div>
                </div>
            )}
            {progress === 100 && <p>Process complete!</p>}
        </div>
    );
};

export default WelcomeCard;