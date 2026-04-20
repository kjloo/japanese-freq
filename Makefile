-include .env
export

# Default goal displays the help menu
.DEFAULT_GOAL := help

# --- CONFIGURATION ---
OS := $(shell uname)

# --- HELP MENU ---
.PHONY: help
help: ## 📋 Show this help menu
	@echo "========================================================================"
	@echo "                    🛠️  DEVELOPMENT COMMANDS"
	@echo "========================================================================"
	@grep -E '^[a-zA-Z_/.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
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

# --- SERVER ---

.PHONY: server/setup
server/setup: ## 🐍 Setup directories and install requirements
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
	# The '/dev/null' redirections are key to preventing the freeze
	@((nohup mlx_lm server --model mlx-community/Qwen3.5-9B-MLX-4bit --host 0.0.0.0 > sidecar.log 2>&1 < /dev/null) &)

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
		echo "Waiting for MLX to load (this can take a minute)..."; \
		while ! curl -s http://localhost:8080/v1/models > /dev/null; do \
			echo "Still loading model..."; \
			sleep 5; \
		done; \
	fi
	@echo "All systems green. Starting the server..."
	cd server && gunicorn -w 1 -k eventlet -b 0.0.0.0:5000 app.main:app

.PHONY: server/test
server/test: ## 🧪 Run server tests
	cd server && pytest -vv

.PHONY: server/lint
server/lint: ## 🔍 Lint server code
	cd server && ruff check . --fix

.PHONY: server/format
server/format: ## ✒️  Format Python code with Black
	cd server && black .

.PHONY: server/clean
server/clean: ## 🧹 Stop services and remove logs/cache
	@echo "Stopping Docker services..."
	docker compose down
	@echo "Killing MLX Sidecar process..."
	@pkill -f "mlx_lm server" || echo "Sidecar was not running."
	@echo "Removing log files..."
	rm -f sidecar.log
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✨ Workspace is clean."

# --- CLIENT ---

.PHONY: client/setup
client/setup: ## 📦 Install client dependencies
	cd client && npm install

.PHONY: client/run
client/run: ## 🌐 Run client dev server
	cd client && npm run dev

.PHONY: client/lint
client/lint: ## 🔍 Lint client code (auto-fix)
	cd client && npm run lint -- --fix

.PHONY: client/format
client/format: ## ✒️  Format client code
	cd client && npm run format
