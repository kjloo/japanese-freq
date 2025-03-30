.PHONY: setup
setup:
	npm install

.PHONY: build
build:
	docker compose build

.PHONY: run
run:
	docker compose up -d
	open http://localhost:5000

.PHONY: stop
stop:
	docker compose down
