POETRY = poetry
CONTAINER_NAME=test-task
ifeq ($(OS),Windows_NT)
    PYTHON = docker exec -it $(CONTAINER_NAME) python
else
    PYTHON := docker exec -it $(CONTAINER_NAME) $(shell command -v python3 || command -v python)
endif

.PHONY: help
help:
	@echo "Usage: make [target] [path=<path>]"
	@echo ""
	@echo "Targets:"
	@echo "  deps          Install dependencies"
	@echo "  update        Update dependencies"
	@echo "  fetch-api     Make a request to the API"
	@echo "  convert       Convert xml to json"
	@echo "  analyze       CLI tool for log analysis"
	@echo "  add-task      Add task via task manager"
	@echo "  update-task   Update task status via task manager"
	@echo "  delete-task   Delete task via task manager"
	@echo "  list          Show list of all tasks via task manager"
	@echo "  build         Build Docker image"
	@echo "  run           Start the application in Docker"
	@echo "  stop          Down the container"

	@echo "  lint      Run isort and Ruff on a specific path"
	@echo "  clean     Remove __pycache__ files"

.PHONY: deps
deps:
	${POETRY} install --no-root

.PHONY: update
update:
	${POETRY} update

.PHONY: fetch-api
fetch-api:
	${PYTHON} -m api_fetcher.fetch_data

.PHONY: convert
input ?= file_processing/input_data.xml
output ?= file_processing/output_data.json
convert:
	${PYTHON} -m file_processing.converter --input-dir "$(input)" --output-dir "$(output)"

.PHONY: analyze
analyze:
	${PYTHON} -m cli_log_analyzer.log_analyzer access.log

.PHONY: add-task
add-task:
	@if [ -z "$(title)" ] || [ -z "$(description)" ] || [ -z "$(due_date)" ]; then \
		echo "Error: Missing required arguments. Usage: make add_task title='My Task' description='Some text' due_date='20-05-2025'"; \
		exit 1; \
	else \
		python -m task_manager.manager add "$(title)" "$(description)" "$(due_date)"; \
	fi

.PHONY: update-task
update-task:
	@if [ -z "$(status)" ]; then \
		echo "Error: Missing required argument 'status'. Usage: make update-task status='completed' [task-id=7 | title='New title']"; \
		exit 1; \
	elif [ -z "$(task_id)" ] && [ -z "$(title)" ]; then \
		echo "Error: Either 'task_id' or 'title' must be provided."; \
		exit 1; \
	else \
		${PYTHON} -m task_manager.manager update "$(status)" $(if $(task_id),--task-id "$(task_id)") $(if $(title),--title "$(title)"); \
	fi

.PHONY: delete-task
delete-task:
	@if [ -z "$(task_id)" ] && [ -z "$(title)" ]; then \
		echo "Error: Either 'task_id' or 'title' must be provided. Usage: make delete-task [task-id=7 | title='New title']"; \
		exit 1; \
	else \
		${PYTHON} -m task_manager.manager delete $(if $(task_id),--task-id "$(task_id)") $(if $(title),--title "$(title)"); \
	fi

.PHONY: list
list:
	${PYTHON} -m task_manager.manager list

.PHONY: build
build:
	docker build -t $(CONTAINER_NAME) .

.PHONY: run
run:
	docker run -dit --name $(CONTAINER_NAME) $(CONTAINER_NAME) bash

.PHONY: stop
stop:
	docker stop $(CONTAINER_NAME) && docker rm $(CONTAINER_NAME)
