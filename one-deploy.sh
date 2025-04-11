#!/usr/bin/env bash
set -euo pipefail

# 🧠 Global variables
SELF="$(dirname $(readlink -f ${0}))"
INVENTORY="${INVENTORY:-${SELF}/inventory/example.yml}"
TAGS="${TAGS:-}"
SKIP_TAGS="${SKIP_TAGS:-}"
VERBOSE="${VERBOSE:-vv}"
HATCH_BIN="$(command -v hatch || true)"
ENV_DEFAULT=""
ENV_CEPH=""


# 🔍 If Hatch is available, try to find the 'default' and 'ceph' environments
if [[ -n "${HATCH_BIN}" ]]; then
    ENV_DEFAULT="$(${HATCH_BIN} env find default 2>/dev/null || true)"
    ENV_CEPH="$(${HATCH_BIN} env find ceph 2>/dev/null || true)"
fi

# 🔐 If $INVENTORY contains variable $ANSIBLE_VAULT, include option --ask-vault-pass
ASK_VAULT=""
if grep -q '\$ANSIBLE_VAULT;' "${INVENTORY}"; then
    ASK_VAULT="--ask-vault-pass"
fi



# 🛠 Generic function to run an Ansible playbook
run_playbook() {
    local playbook_name="${1}"
    local env_name="${2}"       # If Hatch is available, environment 'default' or 'ceph'

    local tag_flags=""
    [[ -n "${TAGS}" ]] && tag_flags="-t ${TAGS}"
    [[ -n "${SKIP_TAGS}" ]] && tag_flags="$tag_flags --skip-tags ${SKIP_TAGS}"

    cd "${SELF}"
    if [[ -n "${HATCH_BIN}" && -n "${env_name}" ]]; then
        $HATCH_BIN env run -e "${env_name}" -- \
            ansible-playbook -${VERBOSE} -i "$INVENTORY" $ASK_VAULT --ask-become-pass ${tag_flags} "opennebula.deploy.${playbook_name}"
    else
        ansible-playbook -${VERBOSE} -i "$INVENTORY" $ASK_VAULT --ask-become-pass ${tag_flags} "opennebula.deploy.${playbook_name}"
    fi
}

# 📦 Install project's requirements (Python + Galaxy). Creates virtualenvs if Hatch is available
install_requirements() {
    if [[ -n "${HATCH_BIN}" && -n "${ENV_DEFAULT}" ]]; then
        echo "[+] Installing dependencies using Hatch (pyproject.toml)..."
        ${HATCH_BIN} env run -e default -- ansible-galaxy collection install --requirements-file "${SELF}/requirements.yml"
    elif [[ -f "${SELF}/requirements.txt" ]]; then
        echo "[+] Installing dependencies usingn pip..."
        pip3 install -r "${SELF}/requirements.txt"                                          # TODO: Rename to python-requirements.txt
        ansible-galaxy collection install --requirements-file "${SELF}/requirements.yml"    # TODO: Rename to galaxy-requirements.yaml
    fi
}

# 🧹 Clean Ansible Galaxy Collections and Hatch environments
clean_requirements() {
    echo "[+] Cleaning Ansible Galaxy Collections (except opennebula)..."
    find "${SELF}/ansible_collections/" -mindepth 1 -maxdepth 1 -type d ! -name opennebula -exec rm -rf {} +

    if [[ -n "$ENV_DEFAULT" ]]; then
        ${HATCH_BIN} env remove default
    fi
    if [[ -n "$ENV_CEPH" ]]; then
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
Usage: ${0} <subcommand>

Available subcommands:
  infra          → 🛠 Run playbook infra.yml
  pre            → 🛠 Run playbook pre.yml
  ceph           → 🛠 Run playbook ceph.yml
  site           → 🛠 Run playbook site.yml
  main           → 🛠 Run playbook main.yml
  requirements   → 📦 Install project's requirements (Python + Galaxy). Creates virtualenvs if Hatch is available
  clean          → 🧹 Clean Ansible Galaxy Collections and Hatch environments
  lint           → 🧽 Run ansible-lint over roles and playbooks
  help           → 📚 Show this usage information

Optional environment variables:
  INVENTORY      → Local/absolute path to an inventory file (default: inventory/example.yml)
  TAGS           → Additional tags (-t)
  SKIP_TAGS      → Blacklisted tags (--skip-tags)
  VERBOSE        → Verbosity level (v, vv, ... vvvvvv). Default: vv
For a list of the available tags, check https://github.com/OpenNebula/one-deploy/wiki/sys_use#available-tags
EOF
}


# 🧠 Subcommand menu
case "${1:-}" in
    infra|pre|site|main)
        run_playbook "${1}" "default"
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