import { useRef, useState, useEffect, FunctionComponent } from 'react';

interface VideoPlayerProps {
    source: string;
}

const VideoPlayer: FunctionComponent<VideoPlayerProps> = ({ source }) => {
    const videoRef = useRef<HTMLVideoElement>(null); // Reference to the video element
    const [progress, setProgress] = useState(0); // State to track video progress
    const [isPlaying, setIsPlaying] = useState(false); // State to track if the video is playing
    const [videoUrl, setVideoUrl] = useState<string | null>(null); // State to store the video URL

    useEffect(() => {
        // Construct the video URL from the API endpoint
        const apiUrl = `http://localhost:5000/api/video/stream/${source}`;
        setVideoUrl(apiUrl);
    }, [source]);

    const handlePlayPause = () => {
        if (videoRef.current) {
            if (isPlaying) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const handleProgress = () => {
        if (videoRef.current) {
            const currentTime = videoRef.current.currentTime;
            const duration = videoRef.current.duration;
            setProgress((currentTime / duration) * 100);
        }
    };

    const handleSeek = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (videoRef.current) {
            const newTime = (Number(event.target.value) / 100) * videoRef.current.duration;
            videoRef.current.currentTime = newTime;
            setProgress(Number(event.target.value));
        }
    };

    return (
        <div className="video-player">
            {videoUrl ? (
                <video
                    ref={videoRef}
                    src={videoUrl}
                    className="video-element"
                    onTimeUpdate={handleProgress}
                    controls
                />
            ) : (
                <p>Loading video...</p>
            )}
            <div className="video-controls">
                <button onClick={handlePlayPause} className="play-pause-button">
                    {isPlaying ? "Pause" : "Play"}
                </button>
                <input
                    type="range"
                    min="0"
                    max="100"
                    value={progress}
                    onChange={handleSeek}
                    className="progress-bar"
                />
                <span className="progress-text">{Math.round(progress)}%</span>
            </div>
        </div>
    );
};

export default VideoPlayer;
