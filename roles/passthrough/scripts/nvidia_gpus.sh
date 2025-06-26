#!/bin/bash

# This script gathers information about the NVIDIA GPUs in the system, their IOMMU groups, and other devices within those groups.

DEVICE_CLASS_PREFIX="03"   # Search for Device Class: Display Controller [03**] https://admin.pci-ids.ucw.cz/read/PD/03/00
VENDOR_ID_HEX="10de"       # Search for Vendor ID: NVIDIA [10de:] https://admin.pci-ids.ucw.cz/read/PC/10de

DEVICE_CLASS_REGEX="\[${DEVICE_CLASS_PREFIX}..]"
VENDOR_ID_REGEX="\[${VENDOR_ID_HEX}:"

echo "["
first_gpu=1

lspci -nnD | grep -i "${DEVICE_CLASS_REGEX}.*${VENDOR_ID_REGEX}" | awk '{print $1}' | while read gpu_bus_id; do
    gpu_vendor_id="$(cat /sys/bus/pci/devices/"${gpu_bus_id}"/vendor)"  # 0x10de
    gpu_device_id="$(cat /sys/bus/pci/devices/"${gpu_bus_id}"/device)"  # 0x1e84
    gpu_driver=$(readlink -e "/sys/bus/pci/devices/${gpu_bus_id}/driver" 2>/dev/null | xargs -r basename || echo null)

    if iommu_group_resolved=$(readlink -e "/sys/bus/pci/devices/${gpu_bus_id}/iommu_group" 2>/dev/null); then
        iommu_group_id="$(basename "${iommu_group_resolved}")"
        # Devices inside the same IOMMU group
        iommu_group_devices_json="["
        first_in_group=1
        for group_device_path in /sys/kernel/iommu_groups/"${iommu_group_id}"/devices/*; do
            group_device_bus_id=$(basename "${group_device_path}")
            group_device_vendor_id=$(cat "${group_device_path}/vendor")
            group_device_device_id=$(cat "${group_device_path}/device")
            group_device_driver=$(readlink -e "${group_device_path}/driver" 2>/dev/null | xargs -r basename || echo null)

            [ "${first_in_group}" -eq 0 ] && iommu_group_devices_json+=", " || first_in_group=0
            iommu_group_devices_json+="{\"bus_id\": \"${group_device_bus_id}\", \"vendor_device_id\": \"${group_device_vendor_id#0x}:${group_device_device_id#0x}\", \"driver\": \"${group_device_driver}\"}"
        done
        iommu_group_devices_json+="]"

    else
        iommu_group_id=null
        iommu_group_devices_json="[]"
    fi

    # Print JSON object for each device
    # If FIRST is not 0, print a comma before the object
    [ "${first_gpu}" -eq 0 ] && echo "," || first_gpu=0
    echo "  {"
    echo "    \"bus_id\": \"${gpu_bus_id}\","
    echo "    \"vendor_device_id\": \"${gpu_vendor_id#0x}:${gpu_device_id#0x}\","
    echo "    \"driver\": \"${gpu_driver}\","
    echo "    \"iommu_group\": \"${iommu_group_id}\","
    echo "    \"iommu_group_devices\": ${iommu_group_devices_json}"
    echo -n "  }"
done

echo
echo "]"