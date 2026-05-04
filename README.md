# Japanese Word Frequency

A Python project that utilizes MeCab to analyze an SRT file and return the frequency of words.

---

## Overview

This project is designed to be **largely zero-config** using:

- `direnv` for automatic environment management  
- `pyenv` for Python version control  
- `make` for command orchestration  
- `docker` for containerized execution  
- `pre-commit` for automatic code quality enforcement  

Once set up, most environment steps happen automatically when you enter the project directory, and code formatting/linting runs automatically on every commit.

---

## System Setup

### macOS Dependencies

```sh
brew install direnv mecab mecab-ipadic git-lfs pyenv pre-commit
```

---

## One-Time Setup

### 1. Configure Shell for `direnv`

Add to your shell config (`~/.zshrc` or `~/.bash_profile`):

```sh
eval "$(direnv hook zsh)"
```

Restart your shell after this.

---

### 2. Initialize Project

```sh
git lfs install
git lfs pull
direnv allow
```

---

### 3. Install Git Hooks (pre-commit)

After cloning the repo:

```sh
pre-commit install
```

This installs git hooks that automatically run:

- Client formatting (Prettier)
- Client linting (ESLint auto-fix)
- Server formatting (Black)
- Server linting (Ruff auto-fix)

---

## What Happens Automatically

When you `cd` into the project, `.envrc` will:

### Python Environment
- Install `pyenv` (if missing)
- Install Python **3.13.13** (if missing)
- Create and activate a project-local virtual environment

### Dependencies
- Automatically install/update `requirements.txt` when it changes

### VS Code Integration
- Auto-configure `.vscode/settings.json` with:
  - Correct Python interpreter
  - Test configuration
  - Import paths

### Environment Variables
- Set `VIRTUAL_ENV` automatically

---

## Code Quality (Pre-commit)

On every commit, the following runs automatically:

### Client (TypeScript)
- Prettier formatting
- ESLint with auto-fix

### Server (Python)
- Black formatting
- Ruff linting with auto-fix

If fixes are applied, files will be updated automatically and you may need to re-stage them before committing.

---

## Configuration

### Environment File

```sh
cp .env.example .env
```

### Ignore List

```sh
cp .ignorelist.example .ignorelist.json
```

---

## Input Files

Place your media files here:

```sh
mkdir -p input/anime
```

- Add `.mp4` and matching `.srt` files

---

## Development Commands

Use `make help` to see all available commands.

---

## Quick Start

### Initial Setup

```sh
make setup
```

This will:

- Prepare server directories  
- Sync input/output files  
- Copy dictionaries  
- Install Python dependencies  
- Install client dependencies  
- Install pre-commit hooks  

---

## Running the App

### Run Full Stack (Docker - Background)

```sh
make run
```

- Starts all services in the background  
- Opens: http://localhost:5000  

---

### Run Full Stack (Dev Mode - Attached Logs)

```sh
make dev
```

---

### Stop Services

```sh
make stop
```

---

## Local Development

### Run Server (Local Python)

```sh
make server/run
```

- Starts MongoDB via Docker  
- Waits for it to become healthy  
- Runs Gunicorn server locally  

---

### Run Client

```sh
make client/run
```

---

## Testing

### Run Server Tests

```sh
make server/test
```

---

## Formatting

### Format All Code

```sh
make format
```

### Individually

```sh
make server/format
make client/format
```

---

## Linting (Manual)

```sh
make client/lint
make server/lint
make quality
```

---

## Docker Commands

### Build Containers

```sh
make build
```

### Run Containers

```sh
make run
```

---

## Server Architecture

The server is a **Flask-based Python application** with the following structure:

- **Entry Point**: `server/app/main.py` initializes the Flask app and registers blueprints
- **Blueprints** (in `server/app/routes/`):
  - `admin_routes` - Administrative endpoints
  - `anki_routes` - Anki deck integration  
  - `debug_routes` - Debugging endpoints
  - `frequency_routes` - Word frequency analysis
  - `io_routes` - Real-time communication (SocketIO)
  - `llm_routes` - LLM chat integration
  - `word_routes` - Word lookup/management
  - `video_routes` - Video processing endpoints

- **Form Processing** (`server/app/form/`):
  - `base_form.py` - Abstract base class for form validation
  - `anki/` - Anki card and settings forms
  - `frequency/` - Frequency analysis forms
  - `llm/` - LLM chat forms

- **Services** (`server/app/service/`): Business logic layer
- **Repositories** (`server/app/repository/`): Data access layer
- **Mappers** (`server/app/mapper/`): Data transformation
- **Models** (`server/app/model/`): Data models
- **Utilities** (`server/app/util/`): Helper functions

- **Key Features**:
  - **SocketIO** for real-time updates
  - **MongoDB** for data persistence
  - **Custom JSON encoder** for specialized serialization
  - **MeCab integration** for Japanese text analysis

---

## Client Architecture

The client is a **React/TypeScript application** built with:

- **Framework**: React with TypeScript
- **Build Tool**: Vite for fast development and production builds
- **Package Management**: npm with `package-lock.json`
- **Linting**: ESLint with React plugins
- **Formatting**: Prettier

- **Key Directories**:
  - `client/src/` - Source code
  - `client/public/` - Static assets
  - `client/node_modules/` - Dependencies (auto-generated)

- **Configuration Files**:
  - `vite.config.ts` - Vite configuration
  - `tsconfig*.json` - TypeScript configurations
  - `eslint.config.js` - ESLint rules

---

## Integration Points

- **Shared Data**: Dictionaries in `dictionaries/`, media in `input/` and `output/`
- **API Communication**: Client ↔ Server via REST API and SocketIO
- **Build System**: Unified `Makefile` orchestrates both stacks

---

## Notes

- No need to manually activate a virtual environment (`direnv` handles it)
- No need to manually install Python (`pyenv` handles it)
- Dependencies auto-update when `requirements.txt` changes
- VS Code setup is automatic
- Code formatting and linting are enforced automatically via pre-commit

---

## Project Structure (Simplified)

```
.
├── client/          # React/TypeScript frontend
├── server/          # Flask/Python backend
├── input/           # Media files (SRT/MP4)
├── output/          # Analysis results
├── dictionaries/    # Language data for MeCab
├── .envrc           # direnv configuration
├── .pre-commit-config.yaml
├── Makefile         # Unified command interface
```

---

## Troubleshooting

### direnv not loading

```sh
direnv allow
```

### pre-commit not running

```sh
pre-commit install
pre-commit run --all-files
```

### Python version issues

```sh
pyenv install 3.13.13
```

### Rebuild environment

```sh
rm -rf .direnv
direnv allow
```
