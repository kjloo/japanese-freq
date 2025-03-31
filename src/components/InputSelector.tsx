import { useState, useEffect, FunctionComponent } from 'react';
import axios from 'axios';

interface InputSelectorProps {
    onSubmit: (selectedInputs: string[]) => void; // Callback to handle selected inputs
    onCancel: () => void; // Callback to cancel input selection
}

const InputSelector: FunctionComponent<InputSelectorProps> = ({ onSubmit, onCancel }) => {
    const [inputs, setInputs] = useState<string[]>([]);
    const [selectedInputs, setSelectedInputs] = useState<string[]>([]);

    useEffect(() => {
        // Fetch inputs from the API
        const fetchInputs = async () => {
            try {
                const response = await axios.get('/api/io/inputs');
                setInputs(response.data["inputs"]);
            } catch (error) {
                console.error('Error fetching inputs:', error);
            }
        };

        fetchInputs();
    }, []);

    const handleCheckboxChange = (input: string) => {
        setSelectedInputs((prev) =>
            prev.includes(input)
                ? prev.filter((item) => item !== input) // Remove if already selected
                : [...prev, input] // Add if not selected
        );
    };

    const handleSubmit = () => {
        onSubmit(selectedInputs); // Pass selected inputs to the parent component
    };

    return (
        <div className="card">
            <h2 className="title">Select Inputs</h2>
            <ul>
                {inputs.map((input) => (
                    <li key={input}>
                        <label>
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
            <button onClick={handleSubmit}>Submit</button>
            <button onClick={onCancel}>Cancel</button>
        </div>
    );
};

export default InputSelector;