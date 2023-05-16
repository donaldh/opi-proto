PODMAN ?= podman
NAME=opi-netconf
VERSION=latest
OC_REPO ?= https://github.com/openconfig/public.git
CNAME ?= opi
V ?= 0

image:	## Build OPI image
	$(PODMAN) build -t $(NAME):$(VERSION) --build-arg OC_REPO=${OC_REPO} .

run:	## Run the OPI container
	$(PODMAN) run -d --network host -e V=${V} -e PUBKEY="$(PUBKEY)" --name $(CNAME) --rm $(NAME):$(VERSION)

stop:	## Kill the OPI container
	$(PODMAN) kill $(CNAME)

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
