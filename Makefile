install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run
build:
	./build.sh

check:
	uv run flake8 .

flask-start:
	uv run flask --app page_analyzer.app --debug run --port 8000

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app