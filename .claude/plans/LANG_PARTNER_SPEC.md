# LANG_PARTNER_SPEC.md

## Project Overview
A LLM-powered Japanese language learning companion that combines speech processing, interactive learning modes, and bilingual conversation. Builds upon existing `japanese-freq` architecture with new LLM integration.

---

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
  3. LLM presents 1–2 natural alternatives with brief explanation (in English + Japanese)
  4. User repeats corrected phrase → conversation continues
- **Rules**:
  - LLM should NOT over-ask questions (avoid interview vibe).
  - Use filler words, ellipses, emojis sparingly to feel human.
  - Balance correction with flow: max 1–2 corrections per minute unless user requests more.

**Data used**:
- `db.vocab.find({ user_id, known: true })` for known words
- `db.user_profile.findOne({ user_id }).jlpt_level`
- `db.user_profile.findOne({ user_id }).interests`

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
   db.words.find({
     jlpt_level: { $lte: user_jlpt_level },
     known: false,
     user_id: user_id
   }).limit(10).sort({ frequency: -1 })
   ```
2. LLM picks **one word** (prefer nouns/verbs over obscure kanji).
3. Ask: "Do you know the word _[target]_?" (User: yes/no/skip via quick button or speech)
4. If **no**:
   - Give brief English meaning + hiragana/kanji.
   - Generate a **mini dialogue (4–6 lines)** where the word appears 2–3× naturally.
   - Ask user to repeat sentences containing the word.
   - After practice, mark `known: true` or `review_later` in DB.
5. If **yes/skip** → choose another word (max 3 attempts).

**Constraints**:
- Word must fit user's **interest domain** (e.g., music, food, tech) when possible.
- Avoid words already encountered in last 7 days (track via `db.review_log`).

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

### 3.2 `words`
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

### 3.3 `user_vocab`
```json
{
  "user_id": "string",
  "word_id": ObjectId,
  "known": boolean,
  "last_seen": ISODate,
  "next_review": ISODate,
  "ease_factor": float,
  "repetitions": int
}
```

### 3.4 `scenarios`
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

### 3.5 `conversation_log`
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
- [ ] Add new MongoDB collections & indexes (`user_vocab`, `scenarios`, `conversation_log`)
- [ ] Extend `config_module` for STT/TTS/LLM provider selection
- [ ] Create wrapper services:
  - `stt_service.py` (Qwen/Whisper + fallback)
  - `tts_service.py` (Qwen/Bark/F5 + fallback)
  - `llm_service.py` (OpenRouter/MLX; mirrors existing chat brain pattern)
- [ ] Implement audio I/O utilities (microphone, playback, format conversion)

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
