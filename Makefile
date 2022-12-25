CONTAINER_NAME_REMIX=bill-fetcher-remix
CONTAINER_NAME_SBI=bill-fetcher-sbi

.PHONY: build start
build:
	docker build -t $(CONTAINER_NAME_REMIX) -f build/Dockerfile-remix .
	docker build -t $(CONTAINER_NAME_SBI) -f build/Dockerfile-sbi .

start:
	docker compose -f deployment/compose.yml up -d
