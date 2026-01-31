#!/usr/bin/env python3
"""
PongTWKR v0.8 - Reset & Safe Values Module
Handles resetting to defaults and applying safe configurations
"""

from .logger import get_original_defaults, log_change
from .profiles import load_profile

def reset_defaults():
    """Reset all values to original defaults (first run)"""
    defaults = get_original_defaults()
    
    if defaults is None:
        print("⚠️ No original defaults found. Run a tweak command first to save defaults.")
        return
    
    # Load the original defaults profile
    load_profile("original_defaults")
    print("✅ All values reset to original defaults")
    log_change("System reset to original defaults")

def safe_profile():
    """Apply safe, conservative values that won't harm any system"""
    from . import cpu, ram, network, compression
    
    print("🛡️  Applying safe configuration...")
    
    # CPU - Conservative settings
    cpu.set_governor("schedutil")  # Balanced governor
    # Don't touch CPU frequencies - leave at hardware defaults
    
    # RAM - Safe values
    ram.set_swappiness(60)  # Linux default
    ram.set_dirty_ratio(20)  # Conservative
    ram.set_dirty_background_ratio(10)  # Conservative
    ram.set_cache_pressure(100)  # Linux default
    ram.set_hugepages(0)  # Disabled
    ram.set_thp("madvise")  # Safe default
    
    # Network - Defaults
    network.set_tcp_metrics("false")  # Enable metrics (default)
    network.set_mtu_probing("off")  # Disabled (default)
    
    # Compression - Safe settings
    compression.set_zswap_enabled("false")  # Disabled by default
    compression.set_numa_balancing("true")  # Usually beneficial
    
    print("✅ Safe configuration applied")
    print("ℹ️  These are conservative values that work on most systems")
    log_change("Safe profile applied")
