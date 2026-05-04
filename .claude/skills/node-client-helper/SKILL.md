# Node-Client Helper Skill

## Client Structure Overview
This skill helps navigate and understand the React client components of the Japanese frequency analyzer. Key elements include:

### 1. Core Architecture
- Built with React 18 + TypeScript
- Uses React Router for client-side navigation  
- Lazy-loaded components for efficient loading
- Managed via Vite for fast development builds

### 2. Key Components
- **WelcomeCard**: Main landing page component (`client/src/components/WelcomeCard/WelcomeCard.tsx`)
- **MineMenu**: User menu/personalization hub (`client/src/components/MineMenu/MineMenu.tsx`)
- **Chat**: Real-time chat interface (`client/src/components/Chat/Chat.tsx`)
- **VideoPlayer**: Handles media playback (`client/src/components/VideoPlayer/VideoPlayer.tsx`)
- **ProcessSettings**: Configuration interface (`client/src/components/ProcessSettings/ProcessSettings.tsx`)

### 3. Routing Setup
- Centralized routing in `App.tsx` (`client/src/App.tsx`)
- Uses React Router's `Routes` + `Route` API
- Lazy loading via `lazy(() => import(...))` pattern with `Suspense` fallback

### 4. Common Patterns
- CSS Modules: e.g. `WelcomeCard.module.css`, `Chat.module.css`, `ProcessSettings.module.css`
- TypeScript strict mode with ESLint rules for React
- Socket.IO client for real-time updates
- Axios for REST API calls
- Type-safe component props with TypeScript interfaces

### 5. Development Stack
- **Core**: React 18.2, ReactDOM 18.2, React Router 6.9  
- **Build**: Vite 6.2, TypeScript 4.9
- **Styling**: CSS Modules, global `index.css`
- **Tooling**: ESLint 9.x, Prettier, `npm-run-all`
- **Runtime**: `type: "module"` ES modules

### 6. Project Conventions
- Component directories contain `.tsx` + matching `.module.css` file
- Routes defined in App.tsx only — no nested routers
- `Suspense` boundary around lazy-loaded routes
- Type declarations in `client/src/types/` directory

### 7. Testing Requirements
- **When modifying any `.ts`/`.tsx` file in `client/src/`, always verify changes by running client tests**
- Run tests with: `make client/test` or `cd client && npm test`
- Tests are written with Vitest + Testing Library
- Test files are co-located in `client/src/components/__tests__/` or alongside components as `*.test.tsx`

