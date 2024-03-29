CONTAINER_NAME_AUELECT=bill-fetcher-auelect
CONTAINER_NAME_REMIX=bill-fetcher-remix
CONTAINER_NAME_SBI=bill-fetcher-sbi
CONTAINER_NAME_TOKYOWATER=bill-fetcher-tokyowater
CONTAINER_NAME_NICIGAS=bill-fetcher-nicigas
CONTAINER_NAME_MONEY_FORWARD=bill-fetcher-money-forward

.PHONY: build start stop clean
build:
	docker build -t $(CONTAINER_NAME_AUELECT) -f build/Dockerfile-auelect .
	docker build -t $(CONTAINER_NAME_REMIX) -f build/Dockerfile-remix .
	docker build -t $(CONTAINER_NAME_SBI) -f build/Dockerfile-sbi .
	docker build -t $(CONTAINER_NAME_TOKYOWATER) -f build/Dockerfile-tokyowater .
	docker build -t $(CONTAINER_NAME_NICIGAS) -f build/Dockerfile-nicigas .
	docker build -t $(CONTAINER_NAME_MONEY_FORWARD) -f build/Dockerfile-money-forward .

start:
	docker compose -f deployment/compose.yml up -d

stop:
	docker compose -f deployment/compose.yml down

debug:
	docker compose -f deployment/compose.yml up

clean:
	docker image rm $(CONTAINER_NAME_AUELECT)
	docker image rm $(CONTAINER_NAME_REMIX)
	docker image rm $(CONTAINER_NAME_SBI)
	docker image rm $(CONTAINER_NAME_TOKYOWATER)
	docker image rm $(CONTAINER_NAME_NICIGAS)
	docker image rm $(CONTAINER_NAME_MONEY_FORWARD)
