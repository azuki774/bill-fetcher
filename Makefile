CONTAINER_NAME_SBI=bill-fetcher-sbi
CONTAINER_NAME_MONEY_FORWARD=bill-fetcher-money-forward

.PHONY: build start stop clean
build:
	docker build -t $(CONTAINER_NAME_SBI) -f build/sbi/Dockerfile .
	docker build -t $(CONTAINER_NAME_MONEY_FORWARD) -f build/money-forward/Dockerfile .

start:
	docker compose -f deployment/compose.yml up -d

stop:
	docker compose -f deployment/compose.yml down

debug:
	docker compose -f deployment/compose.yml up

clean:
	docker image rm $(CONTAINER_NAME_SBI)
	docker image rm $(CONTAINER_NAME_MONEY_FORWARD)
