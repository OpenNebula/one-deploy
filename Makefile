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

.PHONY: infra pre ceph site main

infra pre ceph site main: _TAGS      := $(if $(TAGS),-t $(TAGS),)
infra pre ceph site main: _SKIP_TAGS := $(if $(SKIP_TAGS),--skip-tags $(SKIP_TAGS),)
infra pre ceph site main: _VERBOSE   := $(if $(VERBOSE),-$(VERBOSE),)
infra pre ceph site main:
	cd $(SELF)/ && ansible-playbook $(_VERBOSE) -i $(INVENTORY) $(_TAGS) $(_SKIP_TAGS) opennebula.deploy.$@

.PHONY: requirements requirements-python requirements-galaxy

requirements: requirements-python requirements-galaxy

requirements-python: $(SELF)/requirements.txt
	pip3 install --requirement $< 2> /dev/null || pip3 install --break-system-packages --requirement $<

requirements-galaxy: $(SELF)/requirements.yml
	ansible-galaxy collection install --requirements-file $<
