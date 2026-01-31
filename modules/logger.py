#!/usr/bin/env python3
"""
PongTWKR v0.8 - Logging Module
Handles change logging and default value storage
"""

import os
import datetime
import json
from .utils import ensure_log_dir, read_file, clean_thp_value, get_wifi_status_raw, get_offload_status_raw

def log_change(message):
    """Log a change to the log file"""
    log_dir = ensure_log_dir()
    log_file = os.path.join(log_dir, "changes.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def save_original_defaults():
    """Save original system defaults before any changes"""
    log_dir = ensure_log_dir()
    defaults_file = os.path.join(log_dir, "original_defaults.json")
    
    # Only save if doesn't exist (first run)
    if os.path.exists(defaults_file):
        return
    
    defaults = {
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
    }
    
    with open(defaults_file, "w") as f:
        json.dump(defaults, f, indent=4)
    
    log_change("Original defaults saved")

def get_original_defaults():
    """Load original defaults from file"""
    log_dir = ensure_log_dir()
    defaults_file = os.path.join(log_dir, "original_defaults.json")
    
    if not os.path.exists(defaults_file):
        return None
    
    with open(defaults_file, "r") as f:
        return json.load(f)
