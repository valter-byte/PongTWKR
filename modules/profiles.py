#!/usr/bin/env python3

import os
import json
import glob
from .utils import (
    ensure_profile_dir, read_file, clean_thp_value,
    get_wifi_status_raw, get_offload_status_raw, get_all_physical_disks
)
from .logger import log_change

def save_profile(name):
    disk_list = glob.glob("/sys/block/sd*") + glob.glob("/sys/block/nvme*")
    disks_data = {}

    for disk_path in disk_list:
        disk_name = os.path.basename(disk_path)
        if "zram" in disk_name or (disk_name[-1].isdigit() and "nvme" not in disk_name):
            continue 
        disks_data[disk_name] = {
            "scheduler": clean_thp_value(read_file(f"{disk_path}/queue/scheduler")),
            "ncq_depth": read_file(f"{disk_path}/queue/nr_requests"),
            "max_sectors": read_file(f"{disk_path}/queue/max_sectors_kb"),
            "runtime_pm": read_file(f"{disk_path}/device/power/control")
        }
    profile = {
        "swappiness": read_file("/proc/sys/vm/swappiness"),
        "dirty_ratio": read_file("/proc/sys/vm/dirty_ratio"),
        "dirty_background": read_file("/proc/sys/vm/dirty_background_ratio"),
        "cache_pressure": read_file("/proc/sys/vm/vfs_cache_pressure"),
        "governor": read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"),
        "cpu_min": read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq"),
        "cpu_max": read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"),
        "turbo_status_intel": read_file("/sys/devices/system/cpu/intel_pstate/no_turbo"),
        "turbo_status_amd": read_file("/sys/devices/system/cpu/cpufreq/boost"),
        "smt": read_file("/sys/devices/system/cpu/smt/control"),
        "hugepages": read_file("/proc/sys/vm/nr_hugepages"),
        "thp": clean_thp_value(read_file("/sys/kernel/mm/transparent_hugepage/enabled")),
        "rmem_max": read_file("/proc/sys/net/core/rmem_max"),
        "wmem_max": read_file("/proc/sys/net/core/wmem_max"),
        "tcp_metrics": read_file("/proc/sys/net/ipv4/tcp_no_metrics_save"),
        "mtu_probing": read_file("/proc/sys/net/ipv4/tcp_mtu_probing"),
        "wifi_powersave": get_wifi_status_raw(),
        "offload_gro": get_offload_status_raw("generic-receive-offload"),
        "offload_tso": get_offload_status_raw("tcp-segmentation-offload"),
        "offload_gso": get_offload_status_raw("generic-segmentation-offload"),
        "zram_algo": clean_thp_value(read_file("/sys/block/zram0/comp_algorithm")),
        "zram_size": read_file("/sys/block/zram0/disksize"),
        "zram_streams": read_file("/sys/block/zram0/max_comp_streams"),
        "zswap_enabled": "true" if read_file("/sys/module/zswap/parameters/enabled") == "Y" else "false",
        "zswap_algo": read_file("/sys/module/zswap/parameters/compressor"),
        "zswap_pool": read_file("/sys/module/zswap/parameters/max_pool_percent"),
        "numa_balancing": "true" if read_file("/proc/sys/kernel/numa_balancing") == "1" else "false",
        "disks": disks_data

    }

    profile_dir = ensure_profile_dir()
    path = os.path.join(profile_dir, f"{name}.json")
    
    with open(path, "w") as f:
        json.dump(profile, f, indent=4)
    
    print(f"✅ Profile '{name}' saved at {path}")
    log_change(f"Profile {name} saved")

def load_profile(name):
    from . import cpu, ram, net, disks
    
    profile_dir = ensure_profile_dir()
    path = os.path.join(profile_dir, f"{name}.json")
    
    if not os.path.exists(path):
        print(f"⚠️ Profile '{name}' not found.")
        return
    
    with open(path) as f:
        profile = json.load(f)
    print(f"🔄 Applying profile '{name}'... Hold tight. You may experience stuttering / freezing.")
    if "swappiness" in profile: 
        ram.set_swappiness(profile["swappiness"])
    if "dirty_ratio" in profile: 
        ram.set_dirty_ratio(profile["dirty_ratio"])
    if "dirty_background" in profile: 
        ram.set_dirty_background_ratio(profile["dirty_background"])
    if "cache_pressure" in profile: 
        ram.set_cache_pressure(profile["cache_pressure"])
    if "governor" in profile: 
        cpu.set_governor(profile["governor"])
    if "cpu_min" in profile: 
        cpu.set_cpu_min_freq(float(profile["cpu_min"]) / 1_000_000)
    if "cpu_max" in profile: 
        cpu.set_cpu_max_freq(float(profile["cpu_max"]) / 1_000_000)
    if "turbo_status_intel" in profile or "turbo_status_amd" in profile:
        turbo_val = "true" if profile.get("turbo_status_amd") == "1" or profile.get("turbo_status_intel") == "0" else "false"
        cpu.set_cputurbo(turbo_val)
    if "smt" in profile: 
        cpu.set_smt("true" if profile["smt"] == "on" else "false")
    if "hugepages" in profile: 
        ram.set_hugepages(profile["hugepages"])
    if "thp" in profile:
        ram.set_thp(clean_thp_value(profile["thp"]))
    if "rmem_max" in profile: 
        net.set_rmem(profile["rmem_max"])
    if "wmem_max" in profile: 
        net.set_wmem(profile["wmem_max"])
    if "tcp_metrics" in profile: 
        net.set_tcp_metrics("true" if profile["tcp_metrics"] == "1" else "false")
    if "mtu_probing" in profile:
        mtu_map = {"0": "off", "1": "on", "2": "always"}
        net.set_mtu_probing(mtu_map.get(profile["mtu_probing"], "off"))
    if "wifi_powersave" in profile:
        net.set_wifi_power("true" if profile["wifi_powersave"] == "on" else "false")
    if "offload_gro" in profile: 
        net.set_offload("gro", "true" if profile["offload_gro"] == "on" else "false")
    if "offload_tso" in profile: 
        net.set_offload("tso", "true" if profile["offload_tso"] == "on" else "false")
    if "offload_gso" in profile: 
        net.set_offload("gso", "true" if profile["offload_gso"] == "on" else "false")
    if "zram_algo" in profile: 
        ram.set_zramalgo(profile["zram_algo"])
    if "zram_size" in profile: 
        ram.set_zramsize(profile["zram_size"]) 
    if "zram_streams" in profile: 
        ram.set_zramstreams(profile["zram_streams"])
    if "zswap_enabled" in profile: 
        ram.set_zswap_enabled(profile["zswap_enabled"])
    if "zswap_algo" in profile: 
        ram.set_zswap_algo(profile["zswap_algo"])
    if "zswap_pool" in profile: 
        ram.set_zswap_pool(profile["zswap_pool"])
    if "numa_balancing" in profile: 
        ram.set_numa_balancing(profile["numa_balancing"])
    if "disks" in profile:
        for disk_name, settings in profile["disks"].items():
            print(f"📦 Configuring storage device: {disk_name}...")
            if "scheduler" in settings:
                disks.set_io_scheduler(disk_name, settings["scheduler"])
            if "ncq_depth" in settings:
                disks.set_ncq_depth(disk_name, settings["ncq_depth"]) 
            if "max_sectors" in settings:
                disks.set_max_sectors(disk_name, settings["max_sectors"]) 
            if "runtime_pm" in settings:
                perf_mode = True if settings["runtime_pm"] == "on" else False
                disks.set_runtime_pm(disk_name, perf_mode)
    

    print(f"✅ Profile '{name}' applied")
    log_change(f"Profile {name} applied")