.DEFAULT_GOAL := help

.PHONY: run-all-compose

run-all-compose:  ## Run all services with docker compose
	docker-compose -f docker/docker-compose-auth.yml up

fmt:	## Run code formatting
	black .

help: ## Print this help message
	@grep -E '^[a-zA-Z_-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
