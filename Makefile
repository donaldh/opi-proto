PODMAN ?= podman
NAME=opi-netconf
VERSION=latest
CNAME ?= opi
V ?= 0

images:	## Build OPI images
	cd netopeer2 && make image
	cd opi-netconf && make image

run:	## Run the OPI container
	$(PODMAN) run -d --privileged --network host -e V=${V} -e PUBKEY="$(PUBKEY)" \
		-v $(PWD)/python:/python:z --name $(CNAME) --rm $(NAME):$(VERSION)

stop:	## Kill the OPI container
	$(PODMAN) kill $(CNAME)

help:	## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help
.DEFAULT_GOAL := help
