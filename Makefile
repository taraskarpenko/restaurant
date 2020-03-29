PROJECT=src
MAX_LINE_LENGTH=120
IMAGE_NAME=restaurant
IMAGE_TAG := $(shell git rev-parse --short HEAD)

venv-create:
	python3 -m venv .venv
	source $(PWD)/.venv/bin/activate &> /dev/null && \
		pip install -U pip  && \
		pip install -r requirements-common.txt && \
		pip install -r requirements-deply.txt

venv-dev-create:
	python3 -m venv .dev-venv && \
	source "$(PWD)/.dev-venv/bin/activate" && \
	pip install -U pip && \
	pip install -r requirements-common.txt && \
	pip install -r requirements-dev.txt

unit-test:
	.dev-venv/bin/pytest test/unit

test:
	make lint
	make unit-test

lint:
	.dev-venv/bin/mypy --ignore-missing-imports $(PROJECT)

clean:
	rm -r .dev-venv
	rm -r .venv

build_image:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile .

build_and_start_image:
	make build_image
	docker container run -p 5000:5000 $(IMAGE_NAME):$(IMAGE_TAG)