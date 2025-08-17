IMAGE_REPOSITORY  ?= juanitomint/api-2025
CURRENT_DIR = $(shell pwd)
GIT_LAST_TAG=$(shell git tag --sort=committerdate|tail -n 1)
GIT_COMMIT=$(shell git rev-parse --short HEAD)
GIT_TAG         ?=$(or ${CI_COMMIT_TAG},$(or ${GIT_LAST_TAG}, ${GIT_COMMIT} ) )
IMAGE_TAG         ?= ${GIT_TAG}
help:
	@grep -E '^[\/a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'	
.PHONY: docker-build

deps:  ## config virtual env and install dependencies using poetry
	pip install poetry
	poetry config virtualenvs.in-project true
	poetry config virtualenvs.create true
	poetry install

lint: ## Show code lints using black flake8 and isort
	poetry run flake8 ./
	poetry run black ./ --check
	poetry run isort ./ --check

.PHONY: fix
fix: ## Fix code lints using black flake8 and isort
	poetry run black ./ 
	poetry run flake8 ./
	poetry run isort ./ 

.PHONY: build
build: ## Build python package
	poetry build

.PHONY: publish
publish: ## Publish package to pypi
	poetry publish

.PHONY: cover
cover: ## runs tests
	poetry run coverage run -m unittest discover

.PHONY: cover/report
cover/report: ## Shows coverage Report
	poetry run coverage report

.PHONY: cover/xml
cover/xml: ## Creates coverage Report
	poetry run coverage xml

.PHONY: semantic-release-version
semantic-release-version: ## Run python-semantic-release to calculate version
	poetry run python -m semantic_release version

.PHONY: run
run:
	uvicorn example.main:app --reload --port=8000

.PHONY: clean
clean: ## Clean up local environment and caches
	rm -rf ./.venv
	rm -rf ./.pytest_cache
	rm -rf ./__pycache__
	rm -rf tests/__pycache__
	rm -rf api/__pycache__
.PHONY: printvars
printvars: ## Prints make variables
	$(foreach V, $(sort $(.VARIABLES)), \
	$(if $(filter-out environment% default automatic, $(origin $V)),$(warning $V=$($V) ($(value $V)))) \
	)
