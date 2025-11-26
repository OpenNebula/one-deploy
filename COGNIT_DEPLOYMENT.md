# COGNIT Package Deployment with one-deploy

This guide explains how to deploy OpenNebula with custom packages (e.g., COGNIT frontend) on specific hosts using one-deploy.

## Overview

one-deploy uses Ansible host groups to target specific hosts. We've added:
- Custom inventory structure with dedicated host groups
- Separate playbook for installing custom packages on specific hosts

## Prerequisites

1. **SSH access** from your laptop to all target VMs
2. **SSH tunnel** for accessing custom apt repositories (if needed)
3. **Ansible** installed on your laptop (where one-deploy runs)

## Architecture

```
Frontend VM  → OpenNebula services (oned, scheduler, sunstone, fireedge)
Node VM(s)   → KVM hosts (libvirt, opennebula-node-kvm)
Cognit VM    → Custom packages (e.g., opennebula-cognit-frontend)
```

## Files Created

### 1. Inventory File: `inventory/microenv.yml`

Defines host groups and configuration:

```yaml
all:
  vars:
    ansible_user: root
    one_version: '7.1'
    cognit_apt_repo: "http://172.20.0.1:8080/apt/"  # Custom repo URL
    
frontend:
  hosts:
    f1: { ansible_host: 172.20.0.3 }

node:
  hosts:
    n1: { ansible_host: 172.20.0.8 }

cognit:  # Custom host group
  hosts:
    c1: { ansible_host: 172.20.0.77 }
```

### 2. Custom Playbook: `playbooks/cognit.yml`

Installs packages on hosts in the `cognit` group:

```yaml
- name: Install COGNIT Frontend on dedicated host
  hosts: cognit  # Targets only hosts in 'cognit' group
  tasks:
    - name: Add COGNIT apt repository file
      ansible.builtin.copy:
        dest: /etc/apt/sources.list.d/cognit.list
        content: "deb [trusted=yes] {{ cognit_apt_repo }} stable main\n"
        mode: '0644'
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: yes
    - name: Install opennebula-cognit-frontend
      ansible.builtin.apt:
        name: opennebula-cognit-frontend
        state: present
```

## Deployment Steps

### Step 1: Setup SSH Tunnel (if needed)

If your custom apt repository requires SSH tunnel access:

```bash
ssh -N -L 0.0.0.0:8080:192.168.120.1:80 -J root@194.28.122.112 root@10.10.10.2
```

**Important:** Bind to `0.0.0.0:8080` (not `localhost:8080`) so VMs can access it via your laptop's bridge IP.

### Step 2: Create Customer Inventory

Copy `inventory/microenv.yml` and customize:

```bash
cp inventory/microenv.yml inventory/customer-name.yml
```

Edit `customer-name.yml`:
- Update IP addresses for customer's VMs
- Update passwords (`one_pass`)
- Update network configuration (`vn.service.template`)
- Update `cognit_apt_repo` URL if different

### Step 3: Deploy OpenNebula

```bash
cd /opt/one-deploy
make I=inventory/customer-name.yml
```

### Step 4: Install Custom Packages

```bash
ansible-playbook -i inventory/customer-name.yml playbooks/cognit.yml
```

## How Host Groups Work

Ansible targets hosts based on the `hosts:` directive in playbooks:

| Playbook `hosts:` | Runs On |
|-------------------|---------|
| `hosts: frontend` | Only hosts in `frontend` group |
| `hosts: node` | Only hosts in `node` group |
| `hosts: cognit` | Only hosts in `cognit` group |
| `hosts: all` | All hosts |
| `hosts: frontend:node` | Both groups |

## Customizing for Different Packages

To install different packages on different hosts:

1. **Create new host group** in inventory:
   ```yaml
   custom_app:
     hosts:
       app1: { ansible_host: 10.0.1.10 }
   ```

2. **Create new playbook** (e.g., `playbooks/custom_app.yml`):
   ```yaml
   - hosts: custom_app
     tasks:
       - name: Install custom package
         ansible.builtin.apt:
           name: custom-package-name
           state: present
   ```

3. **Run playbook**:
   ```bash
   ansible-playbook -i inventory/customer-name.yml playbooks/custom_app.yml
   ```

## Repository Format

Ensure your apt repository follows standard Debian structure:

```
/apt/
  ├── dists/
  │   └── stable/
  │       └── main/
  │           └── binary-amd64/
  │               └── Packages
  └── pool/
      └── main/
```

Repository line format: `deb [trusted=yes] http://repo-url/apt/ stable main`

## Troubleshooting

**SSH tunnel not accessible from VMs:**
- Ensure tunnel binds to `0.0.0.0:8080`, not `localhost:8080`
- Verify VMs can reach your laptop's bridge IP (e.g., `172.20.0.1`)

**Package installation fails:**
- Check repository URL is correct
- Verify repository structure (`dists/stable/main/binary-amd64/Packages`)
- Test connectivity: `curl http://repo-url/apt/dists/stable/Release`

**Ansible playbook hangs:**
- Check for apt locks: `fuser /var/lib/apt/lists/lock`
- Verify SSH connectivity: `ansible all -i inventory/customer-name.yml -m ping`

## Example: Complete Customer Deployment

```bash
# 1. Setup tunnel (if needed)
ssh -N -L 0.0.0.0:8080:repo-server:80 -J jump-host user@target &

# 2. Create inventory
cp inventory/microenv.yml inventory/acme-corp.yml
# Edit acme-corp.yml with customer IPs

# 3. Deploy OpenNebula
make I=inventory/acme-corp.yml

# 4. Install custom packages
ansible-playbook -i inventory/acme-corp.yml playbooks/cognit.yml
```

