VERSION = $(shell python3 -c "import sys; sys.path.insert(0, \"$(pwd)\"); import app; print(app.__version__)")
DEFAULT_PATH = $(if $(path), $(path), $(dir $(abspath $(lastword $(MAKEFILE_LIST))))app)

.SILENT: help
help:
	echo "INVENTORY CHECKER APPLICATION\n v$(VERSION)\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: exec
exec: build run ## Build, tag, and execute the container. This will launch the docker container as a daemon

.PHONY: build
build: ## Build and tag the container. This does not start the application.
	docker build -t inventory-check:$(VERSION) -f Dockerfile .

.PHONY: run
run: clean ## This will launch the docker container as a daemon
	docker run --restart=unless-stopped --name inventory-check --log-opt max-size=20m --log-opt max-file=5 -v $(DEFAULT_PATH)/config.ini:/home/app/config.ini -i -d inventory-check:$(VERSION)

.SILENT: lint
.PHONY: lint
lint: ## Run code linting against the source code.
	black ./

.SILENT: clean
.PHONY: clean
clean: ## Clean unneeded docker images and files
	docker rm -f inventory-check || true

.SILENT: tests
.PHONY: tests
tests: ## Execute all test files
	python3 -m pytest -v tests