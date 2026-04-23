import { useState, useEffect, FunctionComponent } from "react";
import axios from "axios";
import commonStyles from "../CommonConfigs.module.css";
import type { AnkiConfig } from "../../types/AnkiTypes"; // Assuming you have a type definition for AnkiConfig
import { ProcessVideoSettings } from "../../types/ProcessVideoSettings";

interface ProcessSettingsProps {
  onVideo: (video: string, settings: ProcessVideoSettings) => void;
  onProcess: () => void;
  onCancel: () => void;
}

const ProcessSettings: FunctionComponent<ProcessSettingsProps> = ({
  onVideo,
  onProcess,
  onCancel,
}) => {
  const [inputs, setInputs] = useState<string[]>([]);
  const [selectedInputs, setSelectedInputs] = useState<string[]>([]);
  const [configs, setConfigs] = useState<AnkiConfig[]>([]);
  const [selectedConfig, setSelectedConfig] = useState<string>("");
  const [wordCheck, setWordCheck] = useState<boolean>(true);
  const [freqMin, setFreqMin] = useState<number>(2);
  const [requiresDefinition, setRequiresDefinition] = useState<boolean>(true);
  const [minWordLength, setMinWordLength] = useState<number>(1);

  useEffect(() => {
    // Fetch inputs from the API
    const fetchInputs = async () => {
      try {
        const response = await axios.get("/api/io/inputs");
        setInputs(response.data.inputs);
      } catch (error) {
        console.error("Error fetching inputs:", error);
      }
    };
    const fetchConfigs = async () => {
      try {
        const response = await axios.get("/api/anki/configs");
        setConfigs(response.data.configs);
        setSelectedConfig(
          response.data.configs.length > 0 ? response.data.configs[0]._id : "",
        );
      } catch (error) {
        console.error("Error fetching configs:", error);
      }
    };

    fetchInputs();
    fetchConfigs();
  }, []);

  const handleCheckboxChange = (input: string) => {
    setSelectedInputs(
      (prev) =>
        prev.includes(input)
          ? prev.filter((item) => item !== input) // Remove if already selected
          : [...prev, input], // Add if not selected
    );
  };

  const handlePlayVideo = () => {
    if (selectedInputs.length > 0) {
      const video = selectedInputs[0]; // Use the first element in selectedInputs
      onVideo(video, {
        inputs: selectedInputs,
        word_check: wordCheck,
        freq_min: freqMin,
        requires_definition: requiresDefinition,
        min_word_length: minWordLength,
        anki_config_id: selectedConfig,
      });
    } else {
      console.error("No video selected. Please select an input.");
    }
  };

  const handleProcess = async () => {
    try {
      onProcess();
      const response = await axios.post("/api/frequency/process", {
        inputs: selectedInputs,
        word_check: wordCheck,
        freq_min: freqMin,
        requires_definition: requiresDefinition,
        min_word_length: minWordLength,
      });
      if (response.status !== 200) {
        throw new Error("Failed to start process");
      }
    } catch (error) {
      console.error("Error starting process:", error);
    }
  };

  return (
    <div className="card">
      <h2 className="title">Process Settings</h2>
      <div className={commonStyles.configContainer}>
        <div className={commonStyles.configRow}>
          <label className={commonStyles.configLabel}>Word Check:</label>
          <input
            type="checkbox"
            checked={wordCheck}
            onChange={(e) => setWordCheck(e.target.checked)}
          />
        </div>
        <div className={commonStyles.configRow}>
          <label className={commonStyles.configLabel}>Frequency Minimum:</label>
          <input
            className={commonStyles.configInput}
            type="number"
            value={freqMin}
            onChange={(e) => setFreqMin(Number(e.target.value))}
            min="1"
          />
        </div>
        <div className={commonStyles.configRow}>
          <label className={commonStyles.configLabel}>
            Minimum Word Length:
          </label>
          <input
            className={commonStyles.configInput}
            type="number"
            value={minWordLength}
            onChange={(e) => setMinWordLength(Number(e.target.value))}
            min="1"
          />
        </div>
        <div className={commonStyles.configRow}>
          <label className={commonStyles.configLabel}>
            Requires Definition:
          </label>
          <input
            type="checkbox"
            checked={requiresDefinition}
            onChange={(e) => setRequiresDefinition(e.target.checked)}
          />
        </div>
        <div className={commonStyles.configRow}>
          <label className={commonStyles.configLabel}>Anki Config:</label>
          <select
            className={commonStyles.configInput}
            value={selectedConfig}
            onChange={(e) => setSelectedConfig(e.target.value)}
          >
            {configs.map((config) => (
              <option key={config._id} value={config._id}>
                {config.name}
              </option>
            ))}
          </select>
        </div>
        <h3 className="title">Select Inputs</h3>
        <ul className={commonStyles.configInputsList}>
          {inputs.map((input) => (
            <li key={input}>
              <label className={commonStyles.configLabel}>
                <input
                  type="checkbox"
                  value={input}
                  checked={selectedInputs.includes(input)}
                  onChange={() => handleCheckboxChange(input)}
                />
                {input}
              </label>
            </li>
          ))}
        </ul>
        <div className={commonStyles.configRow}>
          <button onClick={handlePlayVideo}>Play Video</button>
          <button onClick={handleProcess}>Process</button>
          <button onClick={onCancel}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default ProcessSettings;
