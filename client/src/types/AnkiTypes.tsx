export type AnkiConfig = {
    _id: string;
    name: string;
    deck_id: number;
    deck_name: string;
    model_id: number;
    model_name: string;
    settings: Record<string, string>;
}
