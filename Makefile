PROJECT="restaurant_service"
MAX_LINE_LENGTH=118
IMAGE_NAME="restaurant_service"
IMAGE_TAG := $(shell git rev-parse --short HEAD)

venv-create:
	python3 -m venv .venv
	source $(PWD)/.venv/bin/activate &> /dev/null && \
		pip install -U pip  && \
		pip install -r requirements.txt

venv-dev-create:
	python3 -m venv .dev-venv && \
	source "$(PWD)/.dev-venv/bin/activate" && \
	pip install -U pip && \
	pip install -r requirements.txt && \
	pip install -r requirements-dev.txt