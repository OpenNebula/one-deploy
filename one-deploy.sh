#!/usr/bin/env bash
set -euo pipefail

### This tool supports both environmental variables and command line arguments
### enabling retrocompatibility with the existing makefile, + adding additional features


#######################################
# 🔰 HEADER SECTION
#######################################

SELF="$(dirname "$(readlink -f "${0}")")"
HATCH_BIN="$(command -v hatch || true)"
# 🔍 If Hatch is available, try to find the 'default' and 'ceph' environments
if [[ -n "${HATCH_BIN}" ]]; then
    ENV_DEFAULT="$(${HATCH_BIN} env find default 2>/dev/null || true)"
    ENV_CEPH="$(${HATCH_BIN} env find ceph 2>/dev/null || true)"
fi

# 🧠 Default variables (overridable by env-vars or CLI arguments)
INVENTORY="${INVENTORY:-${SELF}/inventory/example.yml}"
TAGS="${TAGS:-}"
SKIP_TAGS="${SKIP_TAGS:-}"
VERBOSE="${VERBOSE:-vv}"
DRY_RUN="${DRY_RUN:-false}"   # For --check

# 🔓 Make sure we source ANSIBLE_ settings from ansible.cfg exclusively.
unset "$(compgen -v | grep '^ANSIBLE_')" || true


#######################################
# 🛠 Functions
#######################################

# 🐣 Create a Hatch environment if it doesn't exist
_create_env_if_needed() {
    local env_name="${1}"
    local env_path

    if [[ "${env_name}" == "default" ]]; then
        env_path="${ENV_DEFAULT}"
    elif [[ "${env_name}" == "ceph" ]]; then
        env_path="${ENV_CEPH}"
    fi

    if [[ -z "${env_path}" || ! -d "${env_path}" ]]; then
        echo "[+] Creating Hatch '${env_name}' environment..."
        ${HATCH_BIN} env create "${env_name}"
    else
        echo "[+] Using Hatch '${env_name}' environment..."
    fi
}

# 🛠 Generic function to run an Ansible playbook
run_playbook() {
    local playbook_name="${1}"
    local env_name="${2}"       # If Hatch is available, environment can be 'default' or 'ceph'

    _create_env_if_needed "${env_name}"

    cd "${SELF}"
    cmd=(ansible-playbook "-${VERBOSE}" -i "${INVENTORY}" --ask-become-pass)

    # 🔐 If INVENTORY contains variable $ANSIBLE_VAULT, include option --ask-vault-pass
    if grep -q '\$ANSIBLE_VAULT;' "${INVENTORY}"; then
        cmd+=(--ask-vault-pass)
    fi

    if [[ -n "${TAGS}" ]]; then
        cmd+=(--tags "${TAGS}")
    fi

    if [[ -n "${SKIP_TAGS}" ]]; then
        cmd+=(--skip-tags "${SKIP_TAGS}")
    fi

    if [[ "${DRY_RUN}" == "true" ]]; then
        cmd+=(--check)
    fi
    
    cmd+=("opennebula.deploy.${playbook_name}")

    if [[ -n "${HATCH_BIN}" && -n "${env_name}" ]]; then
        "${HATCH_BIN}" env run -e "${env_name}" -- "${cmd[@]}"
    else
        "${cmd[@]}"
    fi
}

# 📦 Install project's requirements (Python + Galaxy). Creates virtualenvs if Hatch is available
install_requirements() {
    if [[ -n "${HATCH_BIN}" && -n "${ENV_DEFAULT}" ]]; then
        echo "[+] Installing dependencies in the corresponding environments using Hatch (pyproject.toml)..."
        _create_env_if_needed "default"
        ${HATCH_BIN} env run -e default -- ansible-galaxy collection install \
            --requirements-file "${SELF}/requirements.yml"
        _create_env_if_needed "ceph"
        ${HATCH_BIN} env run -e ceph -- ansible-galaxy collection install \
            --requirements-file "${SELF}/requirements.yml"
    elif [[ -f "${SELF}/requirements.txt" &&  -f "${SELF}/requirements.yml" ]]; then      
        echo "[+] Hatch not found in the system. Installing python requirements using pip and ansible-galaxy..."
        pip3 install -r "${SELF}/requirements.txt"             # TODO: Rename to python-requirements.txt                                 
        ansible-galaxy collection install --requirements-file "${SELF}/requirements.yml"  # TODO: Rename to galaxy-requirements.yaml
    fi
}

# 🧹 Clean Ansible Galaxy Collections and Hatch environments
clean_requirements() {
    echo "[+] Cleaning Ansible Galaxy Collections (except opennebula)..."
    find "${SELF}/ansible_collections/" -mindepth 1 -maxdepth 1 -type d ! -name opennebula -exec rm -rf {} +

    if [[ -n "${ENV_DEFAULT}" ]]; then
        echo "[+] Cleaning Hatch 'default' environment..."
        ${HATCH_BIN} env remove default
    fi
    if [[ -n "${ENV_CEPH}" ]]; then
        echo "[+] Cleaning Hatch 'ceph' environment..."
        ${HATCH_BIN} env remove ceph
    fi
}

# 🧽 Run ansible-lint over roles and playbooks
lint_ansible() {
    if [[ -n "${ENV_DEFAULT}" ]]; then
        ${HATCH_BIN} env run -e default -- ansible-lint "${SELF}/roles/" "${SELF}/playbooks/"
    else
        ansible-lint "${SELF}/roles/" "${SELF}/playbooks/"
    fi
}

# 📚 Show usage information
usage() {
    cat <<EOF
This script is a wrapper for ansible-playbook, providing a simple interface to run OpenNebula playbooks
It supports running playbooks in different environments using Hatch, and allows for setting various options via environment variables or command line arguments
It also provides a way to install project requirements and clean up environments
It is recommended to use this script instead of running ansible-playbook directly, as it handles some common tasks and provides a consistent interface
This script is part of the OpenNebula project and is licensed under the Apache License, Version 2.0
Copyright (C) 2025 OpenNebula Systems, S.L. <

Usage: ${0} [OPTIONS] <subcommand>

Note: Always set at least the INVENTORY env-var or '--inventory' option.
Note: Run the 'requirements' subcommand before any playbook to install the project's software requirements.

OPTIONS:
  -i | -I | --inventory PATH          Local/absolute path to an Ansible inventory file. Overrides the INVENTORY env-var (default: inventory/example.yml)
  -t | -T | --tags ANSIBLE_TAGS       Additional Ansible tags. Overrides the TAGS env-var (default: empty)
  -s | -S | --skip-tags ANSIBLE_TAGS  Blacklisted Ansible tags. Overrides the SKIP_TAGS env-var (default: empty)
  -v | -V | --verbosity LEVEL         Verbosity level (v, vv, vvv, vvvv, vvvvv or vvvvvv). Overrides the VERBOSE env-var (default: vv)
  -c | -C | --check | --dry-run       Run playbooks in dry-run mode. Overrides the DRY_RUN env-var (default: false)
  -h | -H | --help                    Show this help

SUBCOMMANDS:
  infra          → 🛠 Run playbook infra.yml
  pre            → 🛠 Run playbook pre.yml
  ceph           → 🛠 Run playbook ceph.yml
  site           → 🛠 Run playbook site.yml
  main           → 🛠 Run playbook main.yml
  passthrough    → 🛠 Run playbook passthrough.yml
  requirements   → 📦 Install project's requirements (Python + Galaxy). Creates virtualenvs if Hatch is available
  clean          → 🧹 Clean Ansible Galaxy Collections and Hatch environments
  lint           → 🧽 Run ansible-lint over roles and playbooks
  help           → 📚 Show this usage information

For a list of the available tags, check https://github.com/OpenNebula/one-deploy/wiki/sys_use#available-tags

EOF
}


#######################################
# 🎛 Argument parsing (GNU-style)
#######################################

ARGS=()
while [[ ${#} -gt 0 ]]; do
    case "${1}" in
        --inventory|-i|-I)
            if [[ $# -lt 2 ]]; then
                echo "❌ Option '${1}' requires an argument: Local/absolute path to an Ansible inventory file"
                exit 1
            fi
            INVENTORY="${2}"
            shift 2
            ;;
        --tags|-t|-T)
            if [[ $# -lt 2 ]]; then
                echo "❌ Option '${1}' requires an argument: Additional Ansible tags"
                exit 1
            fi
            TAGS="${2}"
            shift 2
            ;;
        --skip-tags|-s|-S)
            if [[ $# -lt 2 ]]; then
                echo "❌ Option '${1}' requires an argument: Blacklisted Ansible tags"
                exit 1
            fi
            SKIP_TAGS="${2}"
            shift 2
            ;;
        --verbosity|-v|-V)
            if [[ $# -lt 2 ]]; then
                echo "❌ Option '${1}' requires an argument: Verbosity level (v, vv, vvv, vvvv, vvvvv or vvvvvv)"
                exit 1
            fi
            VERBOSE="${2}"
            shift 2
            ;;
        --check|--dry-run|-c|-C)
            DRY_RUN="true"
            shift
            ;;
        --help|-h|-H)
            usage
            exit 0
            ;;
        --)
            shift
            break
            ;;
        -*)
            echo "❌ Unknown option: ${1}"
            usage
            exit 1
            ;;
        *)
            ARGS+=("${1}")
            shift
            ;;
    esac
done

# Treat remaining arguments as subcommands
set -- "${ARGS[@]}"
SUBCOMMAND="${1:-}"


#######################################
# ✅ Argument validation
#######################################

# Validate INVENTORY
if [[ ! -e "${INVENTORY}" ]]; then
    echo "❌ Inventory path '${INVENTORY}' does not exist."
    exit 1
fi
if [[ -f "${INVENTORY}" ]]; then
    if [[ ! -s "${INVENTORY}" ]]; then
        echo "❌ Inventory file '${INVENTORY}' exists but is empty."
        exit 1
    fi
elif [[ -d "${INVENTORY}" ]]; then
    shopt -s nullglob
    inventory_files=("${INVENTORY}"/*.{yml,yaml,ini})
    if [[ ${#inventory_files[@]} -eq 0 ]]; then
        echo "❌ Inventory directory '${INVENTORY}' does not contain any YAML/INI files."
        exit 1
    fi
    shopt -u nullglob
else
    echo "❌ Inventory '${INVENTORY}' is neither a file nor a valid directory."
    exit 1
fi
# Validate TAGS and SKIP_TAGS
ALLOWED_TAGS=(
    bastion ceph datastore flow frontend fstab gate grafana gui
    hosts infra keys libvirt network node preinstall prometheus
    provision stage1 stage2 stage3
)
for var in TAGS SKIP_TAGS; do
    value="${!var}"
    IFS=',' read -ra input_tags <<< "${value}"

    for tag in "${input_tags[@]}"; do
        if [[ -z "${tag}" ]]; then
            continue
        fi
        found=0
        for allowed in "${ALLOWED_TAGS[@]}"; do
            if [[ "${tag}" == "${allowed}" ]]; then
                found=1
                break
            fi
        done
        if [[ ${found} -eq 0 ]]; then
            echo "❌ Invalid ${var} value: '${tag}'. Allowed tags are: ${ALLOWED_TAGS[*]}"
            exit 1
        fi
    done
done
# Validate VERBOSE
if [[ ! "${VERBOSE}" =~ ^v{1,6}$ ]]; then
    echo "❌ Invalid verbosity value: ${VERBOSE}"
    echo "It can only be from 0 to 6 consecutive 'v's: v, vv, vvv, vvvv, vvvvv or vvvvvv"
    exit 1
fi
# Validate DRY_RUN
if [[ "${DRY_RUN}" != "true" && "${DRY_RUN}" != "false" ]]; then
    echo "❌ Invalid DRY_RUN value: ${DRY_RUN}"
    echo "It can only be 'true' or 'false'"
    exit 1
fi


if [[ ${#VERBOSE} -ge 3 ]]; then
    echo "Verbosity level: ${VERBOSE}, greater than 3, showing debug information..."
    echo
    echo "[i] INVENTORY:   ${INVENTORY}"
    echo "[i] TAGS:        ${TAGS}"
    echo "[i] SKIP_TAGS:   ${SKIP_TAGS}"
    echo "[i] DRY_RUN:     ${DRY_RUN}"
    if [[ -n "${HATCH_BIN}" ]]; then
        echo "[i] HATCH_BIN:   ${HATCH_BIN}"
        echo "[i] ENV_DEFAULT: ${ENV_DEFAULT:-<not found>}"
        echo "[i] ENV_CEPH:    ${ENV_CEPH:-<not found>}"
    else
        echo "[i] Hatch not detected in the system."
    fi
    echo
    echo
fi


#######################################
# 🧠 Subcommand dispatcher
#######################################

case "${SUBCOMMAND}" in
    infra|pre|site|main|passthrough)
        run_playbook "${SUBCOMMAND}" "default"
        ;;
    ceph)
        run_playbook "ceph" "ceph"
        ;;
    requirements)
        install_requirements
        ;;
    clean)
        clean_requirements
        ;;
    lint)
        lint_ansible
        ;;
    help|"")
        usage
        ;;
    *)
        echo "❌ Unknown subcommand: ${1}"
        usage
        exit 1
        ;;
esac