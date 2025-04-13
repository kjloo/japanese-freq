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

.PHONY: server-run
server-run:
	cp -r input app/input
	cp -r output app/output
	cp -r dictionaries app/dictionaries
	cp .ignorelist.json app/.ignorelist.json
	cd app; gunicorn -w 1 -k eventlet -b 0.0.0.0:5000 main:app

.PHONY: client-run
client-run:
	npm run dev
