.PHONY: setup
setup:
	npm install

.PHONY: build
build:
	docker compose build

.PHONY: dev
dev:
	docker compose build
	open http://localhost:5000
	docker compose up

.PHONY: run
run:
	docker compose up -d
	open http://localhost:5000

.PHONY: stop
stop:
	docker compose down
