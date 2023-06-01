SHELL := $(shell which bash)
SELF  := $(patsubst %/,%,$(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

I         ?= $(SELF)/inv/n1.yml
INVENTORY ?= $(I)

T    ?=
TAGS ?= $(T)

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

pre site main:
	cd $(SELF)/ && ansible-playbook $(if $(VERBOSE),-$(VERBOSE),) -i $(INVENTORY) $(if $(TAGS),-t $(TAGS),) $@.yml

.PHONY: mitogen

mitogen: $(SELF)/.mitogen/

$(SELF)/.mitogen/:
	git clone -b master git@github.com:mitogen-hq/mitogen.git $@
