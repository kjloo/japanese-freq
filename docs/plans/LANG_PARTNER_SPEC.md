# LANG_PARTNER_SPEC.md

## Project Overview
A LLM-powered Japanese language learning companion that combines speech processing, interactive learning modes, and bilingual conversation. Builds upon existing `japanese-freq` architecture with new LLM integration.

---

## Assistant Persona & Constraints

### Role
Casual Japanese friend (JLPT N3 level).

### Persona & Constraints

**Language**: Japanese only. Absolutely no English.

**Furigana**: Every Kanji must be followed by its reading in parentheses (e.g., 公園(こうえん)).

**Tone**: Casual/Friendly (tameguchi). Accept mixed formal/informal if it's natural.

**Natural Flow (Strict)**:
- 1-2 sentences maximum. Keep it extremely short.

**Share, don't ask**:
- Most responses should be just your own reaction, opinion, or a related story.
- Question Ban: If responding to a question do not ask a question back.
- Do not ask a question unless it's the only way to keep the conversation from dying.
- Never ask a question just to be "polite."
- It is okay to ask followup questions or to ask the user a question if the conversation is not going anywhere.

### Initialization
- Randomly select a Common Japanese Name, a Location, and a Situation.
- Briefly describe the scene and start the talk in Japanese.

### Response Logic
1. **Analyze**: Check for STT typos.
2. **Evaluate**: Is the Japanese natural?
3. **Formulate**:
   - If Natural → Use Output A.
   - If Unnatural → Use Output B and Stop.

### Output Format

**[Output A - Natural]**
✅ [Name]: [Short, reactive statement with Kanji(reading)]

**[Output B - Unnatural]**
🛑 [Name]: (一時停止(いちじていし))

解説(かいせつ): [Short breakdown]

修正(しゅうせい): [Corrected version]
📝 [Corrected User Sentence with Kanji(reading)]
⚠️ 次(つぎ)に進(すす)むために、上(うえ)の文章(ぶんしょう)を声(こえ)に出(だ)して繰(く)り返(かえ)してね！

**Note**: Since this is a more complete chat with voice capabilities, remove parts of the prompt that don't quite fit (e.g., purely voice‑only instructions if not applicable to text chat).

## Implementation Approach

1. **Define a spec file** `LANG_PARTNER_SPEC.md` describing the above constraints in a structured YAML/JSON block that the assistant code will read.
2. **Implement two assistant classes** in `server/app/assistant/` (e.g., `conversation_assistant.py` and `script_assistant.py`). Each class:
   - Loads the spec.
   - Generates an initialization scene (random name, location, situation) using existing utility `random.choice` over predefined lists.
   - Provides a `process(input_text)` method that:
     * Performs simple STT typo correction (basic regex replacements).
     * Checks Japanese naturalness via a lightweight heuristic (presence of hiragana/katakana, no stray ASCII).
     * If natural → format with Output A, prepend ✅, include furigana via a helper `add_furigana()` that uses a small built‑in dictionary (or fallback to `pykakasi` if available).
     * If unnatural → format with Output B, prepend 🛑, add brief explanation and corrected sentence.
3. **Integrate into server routes** (`/api/conversation` and `/api/script`) in `server/app/main.py`.
4. **Expose client‑side TypeScript wrappers** in `client/src/api/partner.ts` that call the new endpoints.
5. **Add unit tests** under `server/app/tests/assistant_test.py` covering natural and unnatural paths.
6. **Update documentation** (`README.md` and a new `LANG_PARTNER_SPEC.md` in the repo root) describing the spec format.

## Critical Files
- `server/app/assistant/conversation_assistant.py`
- `server/app/assistant/script_assistant.py`
- `server/app/main.py` (new routes)
- `client/src/api/partner.ts`
- `LANG_PARTNER_SPEC.md` (spec definition)
- `server/app/tests/assistant_test.py`

## Verification
- Run `make test` – all new tests must pass.
- Manually call the API via `curl` or the client UI and verify:
  * Responses are Japanese only, contain furigana, and are ≤2 sentences.
  * Unnatural input yields the 🛑 block with correction.
- Lint with existing pre‑commit hooks (flake8, eslint) – no new violations.

## Next Steps
1. Review the spec draft with the team.
2. Approve plan to proceed with implementation.

## 1. Core LLM Integration Requirements

### 1.1 Models & APIs
- **Primary STT/TTS**: Qwen 3.5 Speech-to-Text & Text-to-Speech
  - Fallback: Any free/open model supported by OpenRouter (e.g., Whisper for STT, Bark/F5-TTS for TTS)
  - Preference: Use Python MLX module server when efficient enough; support seamless switching to OpenRouter via same interface as existing LLM chat brain
  - Model: Qwen 3.5 (or compatible Japanese-optimized model)

### 1.2 Speech Pipeline
- Input: Microphone/audio file → STT → Japanese text
- Output: Japanese text → LLM → TTS → Audio playback
- Low-latency target: <800ms end-to-end for conversational flow
- Offline-capable option via MLX server when available

### 1.3 Configuration
- Environment variables mirroring existing patterns (see `.envrc`):
  - `OPENROUTER_API_KEY`
  - `MLX_SERVER_URL` (optional)
  - `DEFAULT_JLPT_LEVEL=N4`
  - `VOCDB_PATH` (MongoDB connection string)
- Config loading via existing `app.module.config_module` pattern

---

## 2. Agent Modes Specification

### 2.1 Conversational Mode (Casual Practice)
**Purpose**: Natural, friend-like conversation with gentle correction.

**Behavior**:
- LLM adopts a **personality & name** (e.g., "Haru", a 20-year-old university student from Osaka) for the session.
- Uses known vocabulary (from MongoDB) + JLPT level (N5-N3) to gauge complexity.
- **Scenario setup**: LLM initiates a casual scenario (e.g., "Let's grab coffee after class", "Walking home together") based on user interests.
- **Correction flow**:
  1. User speaks → STT → text analysis
  2. If phrase is unnatural / non-idiomatic → LLM **pauses**
  3. LLM presents 1–2 natural alternatives with brief explanation (in Japanese)
  4. User repeats corrected phrase → conversation continues
- **Rules**:
  - LLM should NOT over-ask questions (avoid interview vibe).
  - Use filler words, ellipses, emojis sparingly to feel human.
  - Balance correction with flow: max 1–2 corrections per minute unless user requests more.

**Data used**:
- `db.user_vocab.find({ user_id, known: true })` for known words (maps to current `word_list` for global ignore list)
- `db.user_profile.findOne({ user_id }).jlpt_level` for complexity gauging
- `db.user_profile.findOne({ user_id }).interests` for scenario selection
- Word definitions from existing `Dictionary.short_lookup()` via JMDict

**Example**:
> LLM (Haru): Ah, I'm so tired today… stayed up late watching anime.
> User: I also very like that anime.
> LLM: *gently* Actually, we'd say 「私もそのアニメが大好きです」— "I really like that anime too." Want to try saying it?
> User: 私もそのアニメが大好きです。
> LLM: Perfect! So true~ ✨ Anyway, what did you think of the last episode?

---

### 2.2 Learn Mode (Vocabulary Acquisition)
**Purpose**: Introduce one new word per session in a natural context.

**Flow**:
1. Query MongoDB for unknown words at or below user JLPT level:
   ```javascript
   db.user_vocab.find({
     user_id: user_id,
     jlpt_level: { $lte: user_jlpt_level },
     known: false
   }).limit(10).sort({ frequency: -1 })
   ```
   **Current Integration**: Word frequency ranks from `frequency_service` output will populate initial `user_vocab` collection.

2. LLM picks **one word** (prefer nouns/verbs over obscure kanji).
3. Ask: "Do you know the word _[target]_?" (User: yes/no/skip via quick button or speech)
4. If **no**:
   - Give brief English meaning + hiragana/kanji (from JMDict lookup via existing `Dictionary.short_lookup()`)
   - Generate a **mini dialogue (4–6 lines)** where the word appears 2–3× naturally.
   - Ask user to repeat sentences containing the word.
   - After practice, mark `known: true` or `review_later` in DB.
5. If **yes/skip** → choose another word (max 3 attempts).

**Constraints**:
- Word must fit user's **interest domain** (e.g., music, food, tech) when possible.
- Avoid words already encountered in last 7 days (track via review log).
- Leverage existing `word_service` ignore list to exclude already-known words.

**Data Integration**:
- Word definitions sourced from existing `Dictionary.short_lookup()` (JMDict)
- Word frequency sourced from `frequency_service.py` analysis
- User progress tracked in new `user_vocab` collection

---

### 2.3 Situational Practice Mode
**Purpose**: Drill common real-world scenarios with repetition.

**Structure**:
- Pre-defined **scenario templates** (JSON) with slots for customization.
- Each scenario contains:
  - Role-play setup (e.g., "You're checking into a hotel")
  - 5–7 key phrases to master
  - 2–3 variation paths (e.g., "with reservation" / "without reservation")

**Scenarios to implement (initial set)**:
1. Hotel check-in / checkout
2. Ordering at a restaurant / dietary requests
3. Scheduling a hair appointment (phone)
4. Asking for directions / train tickets
5. Convenience store: returns / heating food

**Session flow**:
1. LLM explains scenario + goals (in English + Japanese).
2. LLM models a phrase → TTS playback → User repeats.
3. LLM evaluates via STT → **accuracy score** (pronunciation + naturalness).
4. If low score → slow model + re-practice (max 3×).
5. After all phrases → **free role-play**: user improvises within scenario; LLM reacts.

**Future extensibility**:
- Community scenario marketplace (load from `scenarios/` directory).
- Difficulty tags (N5 → N1).

---

### 2.4 English → Japanese Mode (Translation & Nuance)
**Purpose**: Improve translation intuition and natural phrasing.

**Flow**:
1. LLM presents an **English phrase** (from a curated list tied to user level).
2. User attempts Japanese translation (voice or text).
3. LLM compares to reference using **semantic similarity** (e.g., sentence-transformers) + grammar check.
4. Feedback:
   - If **natural & correct** → praise + slight extension ("Exactly! You could also say…").
   - If **unnatural** → highlight awkward part + offer natural alternative + 1 sentence of grammar note.
   - If **wrong** → ask clarifying question to guide self-correction before giving answer.
5. Add phrase to user's **active review queue** (Anki-style) if new.

**Example**:
> LLM: How would you say: "I can't believe it's already Friday"?
> User: 金曜日であることが信じられない。
> LLM: Close! More naturally we'd say: 「もう金曜日なんて信じられない！」— "I can't believe it's already Friday!" The 「なんて」adds casual disbelief. Try it?

---

## 3. Data Model Additions

Collections to create/extend in MongoDB:

### 3.1 `users`
```json
{
  "_id": ObjectId,
  "user_id": "string",
  "name": "string",
  "jlpt_level": "N5|N4|N3|N2|N1",
  "interests": ["food", "music", "travel"],
  "created_at": ISODate,
  "current_mode": "conversation|learn|situational|en2ja"
}
```

### 3.2 `word_list` (Current Implementation)
**Storage Model**: Single MongoDB document storing user's known/ignored words.

```json
{
  "_id": ObjectId,
  "words": ["日本語", "複雑", "単語", ...]
}
```

**Implementation Details** (`server/app/model/word/word_list.py`, `server/app/repository/word/word_repository.py`):
- Stores a flat list of word strings in `words` array
- CRUD operations via `WordRepository`:
  - `add_words(words: list[str])` - Adds words with automatic deduplication using set union
  - `get_words()` - Retrieves current word list
  - `remove_word(word: str)` - Removes individual word
- Singleton pattern: `word_repository` instance accessible throughout app
- Synced from Anki via `word_service.update_from_anki(deck_id, field_name)` 
- Exported to file via `.ignorelist.json` for backup/offline use

**Definition Lookup**: 
- Definitions retrieved on-demand from **JMDict** dictionary via `app/model/dictionary.py`
- `Dictionary.short_lookup(word: str)` returns `ShortDef` object with:
  - `definition` - Primary meaning
  - `kanji` - Kanji form 
  - `hiragana` - Hiragana reading
  - `romaji` - Romanization

**Future Enhancement**:
Evolve to structured `words` collection with rich metadata:
```json
{
  "_id": ObjectId,
  "word": "string",
  "reading": "string",
  "meaning_en": "string",
  "jlpt_level": "N5|N4|N3|N2|N1",
  "pos": "noun|verb|adj|adv|etc",
  "frequency_rank": int,
  "topics": ["food", "business", ...]
}
```
This would enable pre-computed frequency ranking and topic categorization.

### 3.3 `user_vocab` (Removed)
> The `word_list` collection already serves as the user's known‑words list. No separate `user_vocab` collection is required.


### 3.4 `scenarios` (Proposed)
```json
{
  "_id": ObjectId,
  "slug": "hotel-checkin",
  "title_en": "Hotel Check-in",
  "title_ja": "ホテルのチェックイン",
  "level": "N4",
  "phrases": [
    {
      "en": "I have a reservation under Tanaka.",
      "ja": "田中で予約しています。",
      "tags": ["check-in", "reservation"]
    }
  ],
  "setup_script": "You arrive at the hotel with your suitcase...",
  "variations": [
    {
      "condition": "no_reservation",
      "extra_phrases": ["Do you have any rooms available?"]
    }
  ]
}
```

### 3.5 `conversation_log` (Proposed)
```json
{
  "user_id": "string",
  "mode": "string",
  "started_at": ISODate,
  "ended_at": ISODate,
  "turns": [
    {
      "role": "user|assistant",
      "input_text": "string",
      "output_text": "string",
      "audio_urls": ["stt.mp3", "tts.mp3"],
      "corrections": [
        {
          "original": "...",
          "suggested": "...",
          "accepted": true
        }
      ],
      "timestamp": ISODate
    }
  ]
}
```

### 3.6 Word Frequency Processing Pipeline (Current Implementation)

**Location**: `server/app/service/frequency_service.py`

**Pipeline Overview**:
The system extracts and ranks words from Japanese content (subtitles, videos) through multi-stage filtering:

```
Source Content (SRT/MP4) 
  ↓
Parse Content → Tokenize (MeCab) → Filter Ignore List 
  ↓
POS Filter (remove particles, punctuation, auxiliaries)
  ↓
Length Filter (min_word_length)
  ↓
Definition Lookup (JMDict)
  ↓
Frequency Aggregation + Sorting
  ↓
User Confirmation (Optional)
  ↓
JSON Output (by frequency)
```

**Processing Details** (`_process_input`, `_analyze_content`):

1. **Content Parsing**: 
   - SRT files parsed to extract sentences (`JapaneseContent` objects)
   - Video files decomposed to subtitle stream

2. **Tokenization**: 
   - MeCab morphological analyzer via `subtitle_service.get_base_words(sentence)`
   - Returns base form (lemma) of each token

3. **Filtering Stages** (applied in order):
   ```python
   # Stage 1: Ignore list
   if word in ignore_list:
       skip
   
   # Stage 2: Minimum length
   if len(word) < min_word_length:
       skip
   
   # Stage 3: POS filtering (handled upstream in get_base_words)
   # Removes: 助詞 (particles), 補助記号 (punctuation), 助動詞 (auxiliaries)
   ```

4. **Definition Lookup** (per unique word):
   - `dictionary.short_lookup(word)` queries JMDict
   - Returns `ShortDef` or `None`
   - Cached in frequency map to avoid redundant lookups

5. **Frequency Aggregation**:
   ```python
   word_freq[word] = {
       "frequency": count,      # occurrence count
       "definition": ShortDef,  # definition object or False if not found
       "content": [content_obj, ...]  # source sentences
   }
   ```

6. **Output Filtering & Sorting**:
   - Filter by: `frequency >= freq_min`, optionally `requires_definition` 
   - Sort by frequency (descending)
   - Return as ordered dict

7. **User Confirmation** (Optional):
   - `word_service.ask_user(content_dict)` via SocketIO
   - User confirms known words
   - Confirmed words added to ignore_list
   - Unknown words remain in output

**Configuration Parameters** (`ProcessSettings`):
- `freq_min` - Minimum frequency threshold (default: 1)
- `min_word_length` - Minimum character length (default: 1)
- `requires_definition` - Filter to words with definitions (default: false)
- `word_check` - Enable user confirmation dialog (default: true)
- `inputs` - List of source content files to process

---

## 4. API Endpoints (to be added)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/chat/start` | Start a session with mode, persona, JLPT |
| `WS`   | `/api/chat/stream` | Real-time audio/text streaming (STT ↔ LLM ↔ TTS) |
| `POST` | `/api/chat/correction/accept` | Log accepted correction; update vocab |
| `GET`  | `/api/learn/next-word` | Get next unknown word for current user |
| `POST` | `/api/learn/word-feedback` | Feedback on word difficulty / known status |
| `GET`  | `/api/scenarios/list` | List available scenarios (filter by level) |
| `POST` | `/api/scenarios/start` | Start a scenario session |
| `POST` | `/api/en2ja/translate` | Submit user translation; get feedback |
| `GET`  | `/api/profile` | Get user JLPT, interests, stats |
| `PATCH`| `/api/profile` | Update JLPT, interests, persona prefs |

WebSocket message shape (STT ↔ LLM ↔ TTS):
```json
{
  "type": "audio_chunk|text|control",
  "payload": { ... },
  "session_id": "string",
  "timestamp": 1234567890
}
```

---

## 5. Implementation Plan

### Phase 1: Foundations (1–2 weeks)
- [ ] Define `Scenario` and `ConversationLog` models if needed (new collections, no migrations)
  - Migrate word list data from global `word_list` collection to per-user `user_vocab`
  - Initialize `user_vocab` entries from current `frequency_service` analysis outputs
- [ ] Extend `config_module` for STT/TTS/LLM provider selection
- [ ] Create wrapper services:
  - `stt_service.py` (Qwen/Whisper + fallback)
  - `tts_service.py` (Qwen/Bark/F5 + fallback)
  - `llm_service.py` (OpenRouter/MLX; mirrors existing chat brain pattern)
- [ ] Implement audio I/O utilities (microphone, playback, format conversion)
- [ ] **Integration Point**: Wire new services to existing `Dictionary` and `word_repository` for definition/word lookups

### Phase 2: Core Modes (2–3 weeks)
- [ ] Conversational mode engine:
  - Persona system
  - Correction detector (rule-based + LLM scoring)
  - Flow controller (pause/resume on correction)
- [ ] Learn mode engine:
  - Unknown word selector
  - Mini-dialogue generator
  - Review logger
- [ ] API routes for modes (`/api/chat/*`, `/api/learn/*`, `/api/scenarios/*`)

### Phase 3: Situational Practice (1–2 weeks)
- [ ] Scenario loader from `scenarios/` directory
- [ ] Phrase trainer (play → record → score → repeat)
- [ ] Free role-play handler (guided improv within scenario)

### Phase 4: English→Japanese Mode (1 week)
- [ ] Phrase bank by JLPT level + topic
- [ ] Translation evaluator (similarity + grammar checker)
- [ ] Feedback generator with grammar notes
- [ ] Review queue integration

### Phase 5: Polish & Integration (1–2 weeks)
- [ ] Frontend (React) UI for mode selection, persona picker, controls
- [ ] Real-time audio UI (mic → waveform → playback)
- [ ] Settings panel (JLPT, interests, provider selection)
- [ ] Persist session state (resume after disconnect)
- [ ] Tests for core services + API routes

### Phase 6: Deployment & Docs (1 week)
- [ ] Update `Makefile` with new commands (e.g., `make run-llm-partner`)
- [ ] `.envrc` additions for new providers
- [ ] README sections & usage examples
- [ ] CI checks for new modules

---

## 6. Success Metrics

- Latency: 80% of conversational turns < 800ms end-to-end.
- Accuracy: ≥85% naturalness approval on corrections (user-rated).
- Engagement: ≥3 modes used per session on average.
- Learning: ≥5 new words learned per user per week (Learn mode).
- Uptime: 99% for core chat sessions.

---

## 7. Notes on Extensibility

- All modes share a **common context loader** (`load_user_context(user_id)`):
  - Known vocab
  - JLPT level
  - Interests
  - Recent history
- New scenarios are **data-driven** (JSON); no code change needed.
- New LLM/STT/TTS providers can be added via adapter pattern (implement `BaseSTT`, `BaseLLM`, etc.).
- Future AI features (voice cloning, emotion detection) can plug into the same streaming pipeline.

---

*This spec aligns with existing `japanese-freq` architecture and builds on established patterns in `app.module.*`, `app.routes.llm_routes`, and MongoDB usage.*

---

## Appendix A: Integration with Existing Word Processing Architecture

### A.1 Current Word Processing Components
The existing system extracts word frequency data from Japanese media sources through these key components:

| Component | Location | Purpose |
|-----------|----------|---------|
| `FrequencyService` | `server/app/service/frequency_service.py` | Core word extraction & frequency ranking pipeline |
| `SubtitleService` | `server/app/service/subtitle_service.py` | MeCab tokenization, base form extraction |
| `Dictionary` | `server/app/model/dictionary.py` | JMDict definition lookup (kanji, hiragana, meaning) |
| `WordRepository` | `server/app/repository/word/word_repository.py` | MongoDB CRUD for ignore list |
| `WordService` | `server/app/service/word_service.py` | High-level word list management, Anki sync |

### A.2 Data Flow: From Media to LLM Modes

```
1. CONTENT INGESTION (Existing)
   Video/SRT files → File Manager
   
2. WORD EXTRACTION (Existing)
   Subtitle Service (MeCab tokenization)
   ↓
   Frequency Service (multi-stage filtering)
   - Ignore list filter
   - POS filtering
   - Length filtering
   - Definition lookup (JMDict)
   ↓
   Frequency-ranked word dictionary with definitions
   
3. USER CONFIRMATION (Existing)
   Word Service (ask_user via SocketIO)
   ↓
   Update ignore_list in MongoDB
   
4. NEW: POPULATE USER_VOCAB COLLECTION
   Existing frequency data → User Vocab Service
   - Create per-user entries from frequency output
   - Map frequency rank to priority for learning
   - Initialize "known" status from ignore_list
   
5. NEW: SUPPORT LEARNING MODES
   User Vocab + Dictionary lookups
   ↓
   Learn Mode Service queries unknown words
   ↓
   LLM generates contextual dialogues
   ↓
   Track user progress in user_vocab (repetitions, ease_factor)
```

### A.3 Service Integration Points

**For Learn Mode Word Selection**:
- Query `user_vocab` (not yet implemented) filtered by `known: false`
- Fallback to existing `word_service.get_ignore_list()` for global known words
- Merge with frequency rankings from `frequency_service` outputs

**For Word Definitions**:
- Continue using existing `Dictionary.short_lookup(word)` 
- Returns `ShortDef` with kanji, hiragana, meaning
- No DB schema change needed; JMDict is external reference

**For Anki Integration**:
- Existing `word_service.update_from_anki()` syncs known words
- These become initial "known" entries in `user_vocab`
- No changes to Anki gateway needed

**For Word Frequency Ranking**:
- Existing `frequency_service._analyze_content()` produces ranked dict
- Use frequency count as learning priority (higher frequency words first)
- Store frequency data in `user_vocab.frequency_rank` field (new)

### A.4 MongoDB Note
> MongoDB is schemaless, so no migrations are needed. The existing `WordList` model (`server/app/model/word/word_list.py`) already stores the user's known words. If additional fields are needed later, they can be added to the model class without downtime. No separate `user_vocab` collection is required.
### A.5 Code Patterns to Reuse

**Existing Service Pattern** (for new STT/TTS/LLM services):
```python
# From app.service.llm - existing pattern
class LLMService:
    def __init__(self, config):
        self.client = OpenRouter(config)  # or MLX client
    
    def chat(self, messages: list[dict]) -> str:
        return self.client.complete(messages)
```

**Existing Repository Pattern** (for user_vocab):
```python
# Modeled after WordRepository
class UserVocabRepository:
    def find_unknown_words(self, user_id: str, limit: int = 10):
        return UserVocab.objects(user_id=user_id, known=False).limit(limit)
    
    def update_mastery(self, word_id: ObjectId, repetitions: int, ease: float):
        # SM-2 algorithm integration
        pass
```

**Existing Socket Pattern** (for real-time streaming):
```python
# From frequency_service - existing pattern  
socketio.emit("progress", progress.to_json())
socketio.on_event("word_response", handle_response)
```
Use same pattern for audio chunk streaming in STT/TTS pipeline.

---
