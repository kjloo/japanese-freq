import { useRef, useState, useEffect, FunctionComponent } from 'react';
import axios from "axios";

interface VideoPlayerProps {
    source: string;
}

interface Subtitle {
    start: number;
    end: number;
    text: string;
}

const VideoPlayer: FunctionComponent<VideoPlayerProps> = ({ source }) => {
    const videoRef = useRef<HTMLVideoElement>(null); // Reference to the video element
    const [progress, setProgress] = useState(0); // State to track video progress
    const [isPlaying, setIsPlaying] = useState(false); // State to track if the video is playing
    const [videoUrl, setVideoUrl] = useState<string | null>(null); // State to store the video URL
    const [subtitleUrl, setSubtitleUrl] = useState<string | null>(null); // State to store the subtitle URL
    const [subtitles, setSubtitles] = useState<Subtitle[]>([]); // Parsed subtitles
    const [currentSubtitle, setCurrentSubtitle] = useState<string>(""); // Current subtitle text

    useEffect(() => {
        // Construct the video URL from the API endpoint
        const apiUrl = `http://localhost:5000/api/video/stream/${source}`;
        setVideoUrl(apiUrl);

        const subtitleApiUrl = `http://localhost:5000/api/video/subtitles/${source}`;
        setSubtitleUrl(subtitleApiUrl);
    }, [source]);

    useEffect(() => {
        // Fetch and parse subtitles
        if (subtitleUrl) {
            axios
                .get(subtitleUrl, { responseType: "text" }) // Specify response type as text
                .then((response) => {
                    const parsedSubtitles = parseVTT(response.data);
                    setSubtitles(parsedSubtitles);
                })
                .catch((error) => {
                    console.error("Error fetching subtitles:", error);
                });
        }
    }, [subtitleUrl]);

    const parseVTT = (data: string): Subtitle[] => {
        const lines = data.split("\n");
        const subtitles: Subtitle[] = [];
        let start = 0;
        let end = 0;
        let text = "";

        lines.forEach((line, index) => {
            const timeMatch = line.match(
                /((\d{2}:)?\d{2}:\d{2}[,.]\d{3}) --> ((\d{2}:)?\d{2}:\d{2}[,.]\d{3})/
            );
            if (timeMatch) {
                start = parseTime(timeMatch[1]); // Start timestamp
                end = parseTime(timeMatch[3]); // End timestamp
                text = lines[index + 1]; // Subtitle text is usually on the next line
                subtitles.push({ start, end, text });
            }
        });

        return subtitles;
    };

    const parseTime = (time: string): number => {
        const parts = time.split(":");
        let hours = "0";
        let minutes = "0";
        let seconds = "0.0";

        if (parts.length === 3) {
            // Format: HH:MM:SS.mmm
            [hours, minutes, seconds] = parts;
        } else if (parts.length === 2) {
            // Format: MM:SS.mmm (no hours)
            [minutes, seconds] = parts;
        }

        const [secs, millis] = seconds.split(".");
        return (
            parseInt(hours) * 3600 +
            parseInt(minutes) * 60 +
            parseInt(secs) +
            parseFloat(`0.${millis}`)
        );
    };

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

            // Update the current subtitle
            const current = subtitles.find(
                (subtitle) =>
                    currentTime >= subtitle.start && currentTime <= subtitle.end
            );
            setCurrentSubtitle(current ? current.text : "");
        }
    };

    const handleSeek = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (videoRef.current) {
            const newTime = (Number(event.target.value) / 100) * videoRef.current.duration;
            videoRef.current.currentTime = newTime;
            setProgress(Number(event.target.value));
        }
    };

    const styleSubtitle = (subtitle: string): JSX.Element => {
        const knownWords = ["example", "highlight", "video"]; // Replace with your known words
        const words = subtitle.split(" ");

        return (
            <>
                {words.map((word, index) => {
                    const isKnown = knownWords.includes(word.toLowerCase());
                    return (
                        <span
                            key={index}
                            style={{
                                color: isKnown ? "#0b6fb3" : "inherit", // Highlight known words in red
                                fontWeight: isKnown ? "bold" : "normal", // Make known words bold
                            }}
                        >
                            {word}
                            {index < words.length - 1 && " "} {/* Add space between words */}
                        </span>
                    );
                })}
            </>
        );
    };

    return (
        <div className="video-player">
            <div className="video-container">
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
                <div className="subtitle-container">{styleSubtitle(currentSubtitle)}</div>
            </div>
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
