export type ProcessVideoSettings = {
    inputs: string[];
    word_check: boolean;
    freq_min: number;
    requires_definition: boolean;
    min_word_length: number;
    anki_config_id?: string;
};

export const defaultProcessVideoSettings = (): ProcessVideoSettings => ({
    inputs: [],
    word_check: true,
    freq_min: 1,
    requires_definition: false,
    min_word_length: 2,
});
