# CLAUDE.md

## Project Overview
A hybrid Python/Node.js Japanese word frequency analyzer built with:
- **Server**: Python Flask/FastAPI backend with MeCab integration
- **Client**: React/Vite frontend with type-safe TypeScript

## Core Components
- **Server Stack**:
  - `server/app/main.py` - Central application entry point
  - `server/app/form/` - Form processors including Anki integration
  - `server/app/mapper/` - Data transformation utilities
  - `server/app/service/` - Business logic services

- **Client Stack**:
  - React components in `client/src`
  - Vite-powered development server
  - TypeScript type definitions

## Integration Architecture
- Shared dictionary storage in `dictionaries/`
- Media handling via `input/` (SRT/MP4) and `output/` directories
- Unified Makefile for cross-stack commands

## Key Configuration
- `.envrc` - Shell environment management
- `.pre-commit-config.yaml` - Automated code quality hooks
- `Makefile` - Centralized build/test/command interface