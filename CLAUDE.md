# CLAUDE.md

## Project Overview
A hybrid Python/Node.js Japanese word frequency analyzer built with:
- **Server**: Python Flask/FastAPI backend with MeCab integration
- **Client**: React/Vite frontend with type-safe TypeScript

## How to use Claude
- Always create a plan when in plan mode. Use tools to read files and content. Use tools to ask questions to the user. When planning in complete, use tools to ask user for input on whether to execute the plan and switch to edit mode or continue working on the plan.
- When user chooses to execute plan and enter edit mode, use read and write tools to edit files.
- Make sure the validate changes.
- Plan files go into docs/plans and spec files go into docs/spec. Plans should be use to plan several stages of work. Spec should be use to document code as markdown.

## Core Components
- **Server Stack**:
  - refer to the python-server-helper skill
  - `server/app/main.py` - Central application entry point
  - `server/app/form/` - Form processors including Anki integration
  - `server/app/mapper/` - Data transformation utilities
  - `server/app/service/` - Business logic services

- **Client Stack**:
  - refer to the node-client-helper skill
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

## Github Integration
- Refer to the github-helper skill
- Utilize the gh api cli client to access information from GitHub `https://github.com/kjloo/japanese-freq` repo
- Ensure that gh api is properly installed and setup on the user's machine when executing commands
