BUILD_HTTP_PROXY = ${http_proxy}
BUILD_HTTPS_PROXY = ${https_proxy}
BUILD_NO_PROXY = localhost,127.0.0.1

REGISTRY = registry-jpe2.r-local.net/YAW-docker-regi

all:

.PHONY: all \
	image \
	push-image \
	run

image: BASE_VERSION=7-1.5.0-7.9.2009




image: CONDA_FILE_NAME=Miniconda3-py37_4.9.2-Linux-x86_64.sh
image: REQUIREMENTS=requirements.txt
image: DOCKERFILE=docker/Dockerfile
image: VERSION=0.0.dev

push-image: VERSION=0.0.dev
run: VERSION=0.0.dev

image:
	$(eval DOCKER_TAG = $(REGISTRY)/YAW-dashboards:$(VERSION))
	docker build . \
		-f $(DOCKERFILE) \
		--build-arg http_proxy=$(BUILD_HTTP_PROXY) \
		--build-arg https_proxy=$(BUILD_HTTPS_PROXY) \
		--build-arg no_proxy=$(BUILD_NO_PROXY) \
		--build-arg BASE_VERSION=$(BASE_VERSION) \
		--build-arg CONDA_FILE_NAME=$(CONDA_FILE_NAME) \
		--build-arg REQUIREMENTS=$(REQUIREMENTS) \
		-t $(DOCKER_TAG)
	docker image ls $(DOCKER_TAG)

push-image:
	$(eval DOCKER_TAG = $(REGISTRY)/YAW-dashboards:$(VERSION))
	docker push $(DOCKER_TAG)

run:
	$(eval DOCKER_TAG = $(REGISTRY)/YAW-dashboards:$(VERSION))
	docker run -it --rm -p 7000:7000 $(DOCKER_TAG) bash