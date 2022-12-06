CONTAINER_NAME_REMIX=bill-fetcher-remix

.PHONY: build start
build:
	docker build -t $(CONTAINER_NAME_REMIX) -f build/Dockerfile-remix .

start:
	docker compose -f deployment/compose.yml up -d
