SHELL := $(shell which bash)
SELF  := $(patsubst %/,%,$(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

I         ?= $(SELF)/inv/n1.yml
INVENTORY ?= $(I)

T    ?=
TAGS ?= $(T)

S         ?=
SKIP_TAGS ?= $(S)

V       ?= vv
VERBOSE ?= $(V)

ifneq (,$(wildcard $(SELF)/.mitogen/))
ANSIBLE_STRATEGY_PLUGINS := $(realpath $(SELF)/.mitogen/ansible_mitogen/plugins/strategy)
ANSIBLE_STRATEGY         := mitogen_linear
endif

export

.PHONY: all

all: main

.PHONY: pre site main

pre site main: _TAGS      := $(if $(TAGS),-t $(TAGS),)
pre site main: _SKIP_TAGS := $(if $(SKIP_TAGS),--skip-tags $(SKIP_TAGS),)
pre site main: _VERBOSE   := $(if $(VERBOSE),-$(VERBOSE),)
pre site main:
	cd $(SELF)/ && ansible-playbook $(_VERBOSE) -i $(INVENTORY) $(_TAGS) $(_SKIP_TAGS) $@.yml

.PHONY: mitogen

mitogen: $(SELF)/.mitogen/

$(SELF)/.mitogen/:
	git clone -b master git@github.com:mitogen-hq/mitogen.git $@
