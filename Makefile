.PHONY: setup
setup:
	npm install

.PHONY: build
build:
	docker compose build

.PHONY: dev
dev: build
	open http://localhost:5000
	docker compose up japanese-freq

.PHONY: run
run:
	docker compose up -d
	open http://localhost:5000

.PHONY: stop
stop:
	docker compose down

.PHONY: server-setup
server-setup:
	cp -r input server/input
	cp -r output server/output
	cp -r dictionaries server/dictionaries

.PHONY: server-run
server-run: server-setup
	docker compose up mongodb -d
	@echo "Waiting for MongoDB to be ready..."
	@until [ "$$(docker inspect --format='{{.State.Health.Status}}' mongodb)" = "healthy" ]; do \
		echo "MongoDB not healthy yet..."; \
		sleep 2; \
	done
	@echo "MongoDB is ready. Starting the server..."
	cd server; gunicorn -w 1 -k eventlet -b 0.0.0.0:5000 app.main:app

.PHONY: server-test
server-test: server-setup
	cd server; pytest -vv

.PHONY: client-run
client-run:
	cd client; npm run dev

.PHONY: client-lint
client-lint:
	cd client; npm run lint

.PHONY: client-format
client-format:
	cd client; npm run format
