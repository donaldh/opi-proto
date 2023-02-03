PODMAN ?= podman
NAME=netopeer2
VERSION=latest

image:	## Build netopeer2 image
	$(PODMAN) build -t $(NAME):$(VERSION) -f Containerfile .

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
