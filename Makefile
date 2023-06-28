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

.PHONY: all

all: main

.PHONY: pre site main

pre site main: _TAGS      := $(if $(TAGS),-t $(TAGS),)
pre site main: _SKIP_TAGS := $(if $(SKIP_TAGS),--skip-tags $(SKIP_TAGS),)
pre site main: _VERBOSE   := $(if $(VERBOSE),-$(VERBOSE),)
pre site main:
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
	--api-key="$$(cat $(SELF)/.galaxy-key)"
