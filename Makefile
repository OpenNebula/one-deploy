SHELL := $(shell which bash)
SELF  := $(patsubst %/,%,$(dir $(abspath $(firstword $(MAKEFILE_LIST)))))

HATCH_BIN ?= $(shell command -v hatch)

ifneq ($(strip $(HATCH_BIN)),)
ENV_RUN      = $(HATCH_BIN) env run -e $(1) --
ENV_DEFAULT := $(shell $(HATCH_BIN) env find default)
ENV_CEPH    := $(shell $(HATCH_BIN) env find ceph)
endif

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

ifdef ENV_DEFAULT
$(ENV_DEFAULT):
	$(HATCH_BIN) env create default
endif

infra pre site main: $(ENV_DEFAULT)
	cd $(SELF)/ && \
	$(call ENV_RUN,default) ansible-playbook $(_VERBOSE) -i $(INVENTORY) $(_TAGS) $(_SKIP_TAGS) opennebula.deploy.$@

ifdef ENV_CEPH
$(ENV_CEPH):
	$(HATCH_BIN) env create ceph
endif

ceph: $(ENV_CEPH)
	cd $(SELF)/ && \
	$(call ENV_RUN,ceph) ansible-playbook $(_VERBOSE) -i $(INVENTORY) $(_TAGS) $(_SKIP_TAGS) opennebula.deploy.$@

.PHONY: requirements requirements-hatch requirements-python requirements-galaxy clean-requirements

requirements: requirements-$(if $(ENV_RUN),hatch,python) requirements-galaxy

requirements-hatch: $(SELF)/pyproject.toml $(ENV_DEFAULT)

requirements-python: $(SELF)/requirements.txt
	pip3 install --requirement $<

requirements-galaxy: $(SELF)/requirements.yml $(ENV_DEFAULT)
	$(call ENV_RUN,default) ansible-galaxy collection install --requirements-file $<

clean-requirements:
	find $(SELF)/ansible_collections/ -mindepth 1 -maxdepth 1 -type d ! -name opennebula -exec rm -rf {} +
	$(if $(ENV_DEFAULT),$(HATCH_BIN) env remove default,)
	$(if $(ENV_CEPH),$(HATCH_BIN) env remove ceph,)
