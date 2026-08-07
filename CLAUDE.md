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

## Configuration and Tool Selection

### Current API Setup
This project uses **OpenRouter with free tier configuration** for Claude API access:
- **Provider**: OpenRouter (free tier)
- **Model**: OpenRouter free
- **Restriction**: Direct use of Claude models is explicitly prevented

### Tool Selection Guidelines
When choosing tools and steps under this restriction:

1. **Model Restrictions**: Do NOT use Claude models directly. All Claude API calls must go through OpenRouter with free tier.

2. **Available Tools**: You can use the following Claude tools and capabilities:
   - `Agent` tool with any subagent type (`claude`, `claude-code-guide`, `Explore`, `general-purpose`, `Plan`, `statusline-setup`)
   - `Bash` tool for command-line operations
   - `Read`, `Write`, `Edit` tools for file operations
   - `TaskList`, `TaskGet`, `TaskUpdate` for task management
   - `Skill` tool for project-specific skills
   - `SendMessage`, `PushNotification`, `Monitor`, `ScheduleWakeup`, `CronCreate`, `CronList`, `CronDelete` for automation
   - `EnterPlanMode`, `ExitPlanMode`, `EnterWorktree`, `ExitWorktree` for workflow management

3. **Prohibited Tool Usage**:
   - Any direct calls to Anthropic API (use OpenRouter instead)
   - Direct model selection (e.g., `model: "claude-3-5-sonnet-20241022"`)
   - Any configuration that would bypass OpenRouter

4. **Implementation Approach**:
   - Always use the available tool wrapper (Agent, Bash, etc.)
   - Choose tools based on task requirements
   - Use parallel tool calls when appropriate
   - Follow the project's existing patterns for tool usage

5. **Validate Actions**:
   - Because of the restriction on models, updates/writes to files fails. Make sure when you do a file change to validate if there is a failure and read back the file to ensure the change was actually made.

### Development Workflow
- **Tool Selection**: Choose tools based on task complexity and requirements
- **Restriction Enforcement**: Ensure no direct Claude model usage
- **OpenRouter Integration**: All Claude API calls go through OpenRouter
- **Free Tier Management**: Monitor OpenRouter usage if using free tier

## Github Integration
- Refer to the github-helper skill
- Utilize the gh api cli client to access information from GitHub `https://github.com/kjloo/japanese-freq` repo
- Ensure that gh api is properly installed and setup on the user's machine when executing commands
