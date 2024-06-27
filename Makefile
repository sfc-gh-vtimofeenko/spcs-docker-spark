SPARK_MASTER_IMAGE=spark-master
SPARK_WORKER_IMAGE=spark-worker
SAMPLE_CLIENT=sample-client
include .env


.PHONY: help build_local run all login build build_spark_master build_spark_worker build_sample_client push push_spark_master push_spark_worker push_sample_client

help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build_local: ## Build Docker images for local environment
	docker compose build

run: ## Run local Docker images - make sure to set environment variables properly
	docker compose up

all: login build push

login:  ## Login to Snowflake Docker repo. Uses snowcli.
	snow spcs image-registry token --format=JSON | docker login ${REPOSITORY_URL} -u 0sessiontoken --password-stdin

build: build_spark_master build_spark_worker build_sample_client

build_spark_master: ## Builds spark master container
	cd spark-master && docker build --platform linux/amd64 -t $(SPARK_MASTER_IMAGE) . && cd ..

build_spark_worker: ## Builds spark worker container
	cd spark-worker && docker build --platform linux/amd64 -t $(SPARK_WORKER_IMAGE) . && cd ..

build_sample_client: ## Builds a client container
	cd sample-client && docker build --platform linux/amd64 -t $(SAMPLE_CLIENT) . && cd ..

push: push_spark_master push_spark_worker push_sample_client

push_spark_master:
	docker tag $(SPARK_MASTER_IMAGE) ${REPOSITORY_URL}/$(SPARK_MASTER_IMAGE)
	docker push ${REPOSITORY_URL}/$(SPARK_MASTER_IMAGE)

push_spark_worker:
	docker tag $(SPARK_WORKER_IMAGE) ${REPOSITORY_URL}/$(SPARK_WORKER_IMAGE)
	docker push ${REPOSITORY_URL}/$(SPARK_WORKER_IMAGE)

push_sample_client:
	docker tag $(SAMPLE_CLIENT) ${REPOSITORY_URL}/$(SAMPLE_CLIENT)
	docker push ${REPOSITORY_URL}/$(SAMPLE_CLIENT)

