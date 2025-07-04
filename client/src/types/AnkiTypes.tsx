export type AnkiConfig = {
    _id: number;
    name: string;
    deck_id: number;
    deck_name: string;
    model_name: string;
    settings: Record<string, string>;
}
