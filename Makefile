SHELL := $(shell which bash)
SELF  := $(patsubst %/,%,$(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

I         ?= $(SELF)/inventory/example.yml
INVENTORY ?= $(I)

T    ?=
TAGS ?= $(T)

S         ?=
SKIP_TAGS ?= $(S)

V       ?= vv
VERBOSE ?= $(V)

export

# Make sure we source ANSIBLE_ settings from ansible.cfg exclusively.
unexport $(filter ANSIBLE_%,$(.VARIABLES))

.PHONY: all

all: main

.PHONY: pre ceph site main

pre ceph site main: _TAGS      := $(if $(TAGS),-t $(TAGS),)
pre ceph site main: _SKIP_TAGS := $(if $(SKIP_TAGS),--skip-tags $(SKIP_TAGS),)
pre ceph site main: _VERBOSE   := $(if $(VERBOSE),-$(VERBOSE),)
pre ceph site main:
	cd $(SELF)/ && ansible-playbook $(_VERBOSE) -i $(INVENTORY) $(_TAGS) $(_SKIP_TAGS) opennebula.deploy.$@

.PHONY: requirements build publish

requirements: $(SELF)/requirements.yml
	ansible-galaxy collection install --requirements-file $<

build:
	ansible-galaxy collection build --force --verbose

publish: build
	shopt -qs failglob && \
	ansible-galaxy collection publish \
	"$$(ls -1 $(SELF)/opennebula-deploy-[0-9].[0-9].[0-9].tar.gz | sort --version-sort | tail -n1)" \
	--server="$$(cat $(SELF)/.galaxy-server)" \
	--token="$$(cat $(SELF)/.galaxy-key)"
