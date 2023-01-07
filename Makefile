CONTAINER_NAME_REMIX=bill-fetcher-remix
CONTAINER_NAME_SBI=bill-fetcher-sbi
CONTAINER_NAME_TOKYOWATER=bill-fetcher-tokyowater

.PHONY: build start
build:
	docker build -t $(CONTAINER_NAME_REMIX) -f build/Dockerfile-remix .
	docker build -t $(CONTAINER_NAME_SBI) -f build/Dockerfile-sbi .
	docker build -t $(CONTAINER_NAME_TOKYOWATER) -f build/Dockerfile-tokyowater .

start:
	docker compose -f deployment/compose.yml up -d
