# Word List Dictionary Implementation Summary

## Overview
The word list/dictionary system manages Japanese words across multiple sources (Anki decks, file-based ignore lists, and content extraction) using MongoDB for persistence. The architecture follows a layered pattern: Models → Repository → Service → API Routes.

---

## 1. Data Storage & Database Models

### Primary Model: `WordList`
**File**: [server/app/model/word/word_list.py](server/app/model/word/word_list.py)

```python
class WordList(Document):
    words = ListField()
    meta = {"collection": "word_list"}
```

- **Storage**: MongoDB collection named `word_list`
- **Schema**: Simple document with a single `ListField` containing word strings
- **Purpose**: Stores the ignore list (words users already know)
- **Framework**: MongoEngine for ORM

### Dictionary Model: `Dictionary`
**File**: [server/app/model/dictionary.py](server/app/model/dictionary.py)

- **Purpose**: Loads and manages Japanese-to-English dictionary definitions
- **Source**: JMDict dictionary (ZIP format: `jmdict_english.zip`)
- **Data Structure**: Kanji → List of definitions, Hiragana → List of definitions
- **Lookup Methods**:
  - `lookup(word)` - Returns full definitions
  - `short_lookup(word)` - Returns simplified definition with kanji, hiragana, and romaji

### Word Frequency Model: `WordFreq`
**File**: [server/app/model/frequency/word_freq.py](server/app/model/frequency/word_freq.py)

```python
class WordFreq:
    freq: int          # Occurrence count
    defition: str      # Definition
    content: list[str] # Associated content

class WordFreqDict:
    word_freq_dict: dict[str, WordFreq]
```

- **Purpose**: Tracks word frequency during content analysis
- **Used in**: Word processing pipeline for filtering and ranking words

### Anki Card Values Model
**File**: [server/app/model/anki/anki_values.py](server/app/model/anki/anki_values.py)

- **Fields**: audio, conjugation, definition, hiragana, kanji, part_of_speech, pitch_accent, romaji, sentence, sentence_audio, translation
- **Purpose**: Holds data for creating Anki cards from processed words

---

## 2. Repository Pattern for Data Access

### WordRepository
**File**: [server/app/repository/word/word_repository.py](server/app/repository/word/word_repository.py)

Manages CRUD operations on the `WordList` collection:

```python
class WordRepository:
    def add_words(self, words: list[str]) -> WordList
        # Adds unique words, prevents duplicates using set union
    
    def get_words(self) -> list[str]
        # Retrieves all words from the single WordList document
    
    def remove_word(self, word: str) -> WordList
        # Removes a word from the list
```

**Key Pattern**: Uses `.first()` to access the single shared `WordList` document in MongoDB.

**Singleton Instance**: `word_repository` global instance for application-wide use

---

## 3. Word Service - Business Logic

**File**: [server/app/service/word_service.py](server/app/service/word_service.py)

### Main Functions:

#### `get_ignore_list() -> set[str]`
- Returns the in-memory ignore list (words to exclude from processing)
- Loaded from database or file on app startup

#### `update_from_anki(deck_id: int, field_name: str) -> list[str]`
- Fetches cards from an Anki deck
- Extracts field values (e.g., "Kanji" field)
- Adds them to the ignore list and database
- Uses `AnkiService` to communicate with Anki

#### `update_from_file() -> list[str]`
- Syncs the in-memory ignore list to the database
- Returns all words currently in the database

#### `export_to_file() -> list[str]`
- Writes the ignore list to a JSON file (`.ignorelist.json`)
- Enables offline backup and git tracking

#### `ask_user(content: dict) -> dict`
- Interactive SocketIO-based user prompt
- User indicates if they know each word
- Known words are added to ignore list
- Unknown words remain in the content dictionary

### Initialization Process:
1. Load `WordList` from MongoDB (if exists)
2. Fallback to `.ignorelist.json` file if no database record
3. Store result in global `ignore_list` set for fast lookups

---

## 4. Dictionary Module - Configuration & Initialization

**File**: [server/app/module/dictionary_module.py](server/app/module/dictionary_module.py)

```python
wakati = _get_tagger()          # MeCab tagger for word segmentation
dictionary = Dictionary(...)    # JMDict loader
ignore_list_file = ".ignorelist.json"
ignore_list: set[str] = _load_ignore_list()

IGNORE_POS = ["助動詞", "補助記号", "助詞"]  # Parts of speech to exclude
```

### Initialization Steps:
1. Checks if dictionary directory exists
2. Extracts from ZIP if needed
3. Initializes MeCab tagger with UniDic
4. Loads ignore list from database or file

---

## 5. Word Processing & Extraction

### Subtitle Service
**File**: [server/app/service/subtitle_service.py](server/app/service/subtitle_service.py)

#### `get_base_words(sentence: str) -> Generator[str]`
- Tokenizes Japanese sentences using MeCab/wakati
- Filters using:
  - Ignore list membership
  - Part-of-speech (skips particles, auxiliary verbs, punctuation)
- Yields base form words

#### `style_subtitles(subtitles: list[str]) -> list[str]`
- Wraps new words in `<span class='new-word'>` for HTML display
- Used for subtitle highlighting

---

## 6. Frequency Service - Word List Generation

**File**: [server/app/service/frequency_service.py](server/app/service/frequency_service.py)

### Main Functions:

#### `process_words(process_settings: ProcessSettings)`
- Iterates through selected input files
- Calls `_process_input()` for each file
- Writes results to JSON output files
- Emits progress updates via SocketIO

#### `process_video(process_settings: ProcessSettings) -> dict`
- Similar to `process_words()` but for single video input
- Returns word frequency dictionary directly (no file write)

#### `_process_input() -> dict`
Coordinates the word extraction pipeline:
1. Retrieves current ignore list
2. Parses file content
3. Analyzes content → word frequency dictionary
4. Optionally prompts user via `ask_user()`
5. Returns filtered/sorted word dictionary

#### `_analyze_content(content, ignore_list, freq_min, requires_definition, min_word_length) -> dict`
**Core word analysis algorithm**:
- Iterates through all sentences in content
- Extracts words via `subtitle_service.get_base_words()`
- Builds frequency map with:
  - Word occurrence count
  - Definition (via `dictionary.short_lookup()`)
  - Associated content/sentences
- Filters by:
  - `freq_min`: Minimum occurrence count
  - `requires_definition`: Must have a dictionary entry
  - `min_word_length`: Minimum character length
- Returns sorted dictionary (descending by frequency)

---

## 7. API Routes for Word Lists

**File**: [server/app/routes/word_routes.py](server/app/routes/word_routes.py)

### Endpoints:

#### `POST /api/word/ignore-list/sync`
**Purpose**: Synchronize ignore list from Anki to database

**Request**:
```json
{
  "deck_id": 123,
  "field_name": "Kanji"
}
```

**Process**:
1. Fetches cards from specified Anki deck
2. Extracts field values via `word_service.update_from_anki()`
3. Syncs to database via `word_service.update_from_file()`
4. Returns updated ignore list

**Response**:
```json
{
  "ignore_list": ["word1", "word2", ...]
}
```

#### `POST /api/word/ignore-list/export`
**Purpose**: Export ignore list to JSON file

**Response**:
```json
{
  "ignore_list": ["word1", "word2", ...]
}
```

**Side Effect**: Creates/overwrites `.ignorelist.json`

---

## 8. Gateway Pattern - Anki Integration

**File**: [server/app/gateway/anki/anki_gateway.py](server/app/gateway/anki/anki_gateway.py)

- **Purpose**: HTTP bridge to AnkiConnect (Anki's REST API)
- **Methods**: `post(action, params)` sends requests to Anki server
- **URL**: Configured via `anki_server_url` from gateway module

### Anki Service Integration
**File**: [server/app/service/anki/anki_service.py](server/app/service/anki/anki_service.py)

Key functions for word list:
- `get_cards_in_deck(deck_id, field_name)` - Extracts field values from deck
- `get_deck_names()` - Lists available decks
- `get_model_names()` - Lists card templates
- `get_model_fields(model_id)` - Lists fields in a model

---

## 9. Frequency Processing Form

**File**: [server/app/form/frequency/process_settings.py](server/app/form/frequency/process_settings.py)

```python
class ProcessSettings:
    inputs: list[str]              # Files to process
    word_check: bool               # Enable user prompts
    freq_min: int                  # Minimum occurrence threshold
    requires_definition: bool      # Filter to defined words only
    min_word_length: int           # Minimum word character length
```

**Validation**: Ensures all parameters are valid before processing

---

## 10. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    API ROUTES (word_routes)                 │
│  POST /api/word/ignore-list/sync                            │
│  POST /api/word/ignore-list/export                          │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                   WORD SERVICE (word_service)               │
│  - get_ignore_list()                                        │
│  - update_from_anki(deck_id, field_name)                    │
│  - update_from_file()                                       │
│  - export_to_file()                                         │
│  - ask_user(content)                                        │
└────────────┬─────────────────────────┬──────────────────────┘
             │                         │
             ▼                         ▼
   ┌─────────────────┐      ┌─────────────────┐
   │ AnkiService     │      │ WordRepository  │
   │ (via gateway)   │      │ (MongoDB)       │
   └─────────────────┘      └────────┬────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │ WordList(Model) │
                            │ [MongoDB]       │
                            └─────────────────┘
```

## Frequency Processing Data Flow:

```
User Input (ProcessSettings)
         │
         ▼
frequency_routes.start_process()
         │
         ▼
frequency_service.process_words()
         │
         ├─> Get ignore_list from word_service
         ├─> Parse source content (SRT/MP4)
         │
         ▼
_analyze_content()
         │
         ├─> subtitle_service.get_base_words()
         │   ├─> MeCab tokenization
         │   ├─> Filter by ignore_list
         │   ├─> Filter by POS tags
         │   └─> Yield base words
         │
         ├─> dictionary.short_lookup(word)
         │   └─> Get definition, kanji, hiragana, romaji
         │
         └─> Build frequency map with filtering
         │
         ▼
Optional: word_service.ask_user() [SocketIO prompts]
         │
         ▼
io_service.write_to_json() [Output file]
```

---

## 11. Key Design Patterns

### 1. **Singleton Pattern**
- `word_repository` - Single instance shared across app
- `ignore_list` - Global in-memory set for fast lookups
- `dictionary` - Loaded once at startup

### 2. **Repository Pattern**
- `WordRepository` abstracts MongoDB operations
- Services depend on repository, not direct database calls

### 3. **Gateway Pattern**
- `anki_gateway` bridges to external Anki service
- Service layer calls gateway for Anki operations

### 4. **Factory Pattern (implicit)**
- `Dictionary` class loads and parses JMDict ZIP file
- `WordFreq` and `WordFreqDict` build frequency structures

### 5. **Strategy Pattern**
- Different content sources (SRT, MP4, plain text) parse differently
- Word filtering applies multiple strategies (ignore list, POS, length)

---

## 12. Database Schema

```
MongoDB: word_list collection
{
  _id: ObjectId,
  words: ["単語1", "単語2", "単語3", ...]
}
```

**Characteristics**:
- Single document (no multiple word lists)
- Uses MongoEngine ListField for array of strings
- Simple, flat schema suitable for ignore lists

---

## 13. File I/O

### Input Files
- **Location**: `input/` directory
- **Formats**: SRT subtitles, MP4 videos, plain text
- **Parsing**: Via content models (`TextContent`, `VideoContent`, `SourceContent`)

### Output Files
- **Location**: `output/` directory
- **Format**: JSON with word frequency data
- **Contains**: `{word: {frequency, definition, content}}`

### Ignore List File
- **Location**: `.ignorelist.json` (root directory)
- **Format**: JSON array of word strings
- **Purpose**: Persistent backup / git version control

---

## 14. Configuration & Dependencies

### MeCab/UniDic
- **Dictionary**: `dictionaries/unidic/` (UniDic 3.10)
- **Purpose**: Morphological analysis, POS tagging
- **Auto-extracted**: From `unidic-3.10.zip` if needed

### JMDict
- **Dictionary**: `jmdict_english.zip`
- **Purpose**: Word definitions
- **Format**: JSON arrays per term

### External Services
- **Anki**: AnkiConnect API (HTTP on configurable port)
- **MongoDB**: Database for persistent ignore list storage

---

## 15. Error Handling

### Database
- `.first()` returns `None` if no WordList exists → creates new
- Handles initialization gracefully

### Anki
- `ValueError` for invalid deck IDs
- `RequestException` for network failures
- Logged but doesn't crash processing

### File Operations
- Reads from `.ignorelist.json` if database unavailable
- Catches `FileNotFoundError` for missing files

---

## 16. Performance Considerations

### Memory
- **In-memory ignore list**: `set[str]` for O(1) lookups
- **Frequency analysis**: `defaultdict` for efficient aggregation
- **Dictionary**: Loaded once at startup

### Database
- **Single document query**: `WordList.objects.first()` - minimal overhead
- **Set union for dedup**: `set(existing) | set(new_words)`

### Processing
- **Threading**: `frequency_service.process_words()` runs in separate thread
- **SocketIO progress**: Emitted after each file completion

---

## Summary of Key Files

| Component | File Path |
|-----------|-----------|
| Word List Model | `server/app/model/word/word_list.py` |
| Word Repository | `server/app/repository/word/word_repository.py` |
| Word Service | `server/app/service/word_service.py` |
| Dictionary | `server/app/model/dictionary.py` |
| Dictionary Module | `server/app/module/dictionary_module.py` |
| Frequency Service | `server/app/service/frequency_service.py` |
| Subtitle Service | `server/app/service/subtitle_service.py` |
| Word Routes | `server/app/routes/word_routes.py` |
| Frequency Routes | `server/app/routes/frequency_routes.py` |
| Anki Service | `server/app/service/anki/anki_service.py` |
| Anki Gateway | `server/app/gateway/anki/anki_gateway.py` |
| Process Settings | `server/app/form/frequency/process_settings.py` |
| Database Module | `server/app/module/database_module.py` |
| Word Frequency Model | `server/app/model/frequency/word_freq.py` |
| Anki Values Model | `server/app/model/anki/anki_values.py` |
