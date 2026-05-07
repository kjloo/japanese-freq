-include .env
export

# Default goal displays the help menu
.DEFAULT_GOAL := help

# --- HELP MENU ---
.PHONY: help
help: ## 📋 Show this help menu
	@echo "========================================================================"
	@echo "                    🛠️  DEVELOPMENT COMMANDS"
	@echo "========================================================================"
	@grep -E '^[a-zA-Z_/.-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		sed -e 's/^.*Makefile://' | \
		sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo "========================================================================"

# --- PROJECT WIDE ---

.PHONY: setup
setup: server/setup client/setup ## 🏗️  Initial setup for both server and client

.PHONY: build
build: ## 🐳 Build docker containers
	docker compose build

.PHONY: dev
dev: build ## 🚀 Start full stack in dev mode (attached)
	open http://localhost:5000
	docker compose up japanese-freq

.PHONY: run
run: ## 🏃 Run full stack in background
	docker compose up -d
	open http://localhost:5000

.PHONY: stop
stop: ## 🛑 Stop all services
	docker compose down

.PHONY: format
format: server/format client/format ## 🎨 Format all code (Python & JS)

.PHONY: clean
clean: server/clean client/clean ## 🧹 Clean everything (Server, Client, & Docker)
	@echo "✨ All systems cleaned."

# --- SERVER ---

.PHONY: server/setup
server/setup: ## 🐍 Setup server directories and requirements
	mkdir -p server/input server/output
	if [ -d input ]; then rsync -a input/ server/input/; fi
	if [ -d output ]; then rsync -a output/ server/output/; fi
	rsync -a dictionaries/ server/dictionaries/
	pip install -r requirements.txt

.PHONY: sidecar/run
sidecar/run: ## 🤖 Start the MLX-LM sidecar server (Qwen 3.5 9B)
	@echo "Checking if mlx-lm is installed..."
	@pip show mlx-lm > /dev/null || pip install mlx-lm
	@echo "🚀 Starting Qwen3.5 9B on Metal GPU..."
	@((nohup mlx_lm server --model mlx-community/Qwen3.5-9B-MLX-4bit --host 0.0.0.0 > sidecar.log 2>&1 < /dev/null) &)

.PHONY: sidecar/tts
sidecar/tts: ## 🎙️ Start the Qwen 3 TTS sidecar server with voice cloning
	@echo "Checking if mlx-audio is installed..."
	@pip show mlx-audio > /dev/null || pip install mlx-audio
	@echo "🚀 Starting Qwen 3 TTS sidecar server..."
	@((nohup python server/tts_sidecar.py > tts_sidecar.log 2>&1 < /dev/null) &)

.PHONY: server/run
server/run: ## ⚡ Run server locally with Gunicorn
	docker compose up mongodb -d
	@echo "Waiting for MongoDB to be ready..."
	@until [ "$$(docker inspect --format='{{.State.Health.Status}}' mongodb)" = "healthy" ]; do \
		sleep 2; \
	done
	@echo "Checking for MLX Sidecar..."
	@if ! curl -s http://localhost:8080/v1/models > /dev/null; then \
		echo "Sidecar not detected. Launching..."; \
		$(MAKE) sidecar/run; \
		echo "Waiting for MLX to load..."; \
		while ! curl -s http://localhost:8080/v1/models > /dev/null; do \
			sleep 5; \
		done; \
	fi
	@echo "All systems green. Starting the server..."
	cd server && gunicorn -w 1 -k eventlet -b 0.0.0.0:5000 app.main:app

.PHONY: server/test
server/test: ## 🧪 Run server tests
	cd server && pytest -vv

.PHONY: server/lint
server/lint: ## 🔍 Lint and fix server code (Ruff)
	cd server && ruff check . --fix

.PHONY: server/format
server/format: ## ✒️  Format Python code (Black)
	cd server && black .

.PHONY: server/clean
server/clean: ## 🧹 Stop server, kill sidecar, and remove cache/logs
	@echo "Cleaning Server..."
	docker compose down
	@pkill -f "mlx_lm server" || true
	rm -f sidecar.log
	rm -rf .direnv
	rm -rf .venv
	rm -rf .pytest_cache
	find server -type d -name "__pycache__" -exec rm -rf {} +
	find server -type d -name ".pytest_cache" -exec rm -rf {} +

# --- CLIENT ---

.PHONY: client/setup
client/setup: ## 📦 Install client dependencies
	cd client && npm install

.PHONY: client/run
client/run: ## 🌐 Run client dev server
	cd client && npm run dev

.PHONY: client/lint
client/lint: ## 🔍 Lint and auto-fix client code
	@echo "Running ESLint with --fix..."
	cd client && npm run lint -- --fix

.PHONY: client/test
client/test: ## 🧪 Run client tests
	cd client && npm test

.PHONY: client/format
client/format: ## ✒️  Format client code (Auto-fix)
	@echo "Formatting client code..."
	cd client && npm run format

.PHONY: client/clean
client/clean: ## 🧹 Remove node_modules and build artifacts
	@echo "Cleaning Client..."
	rm -rf client/node_modules
	rm -rf client/dist
	rm -rf client/.next
