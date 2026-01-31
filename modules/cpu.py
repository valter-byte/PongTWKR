#!/usr/bin/env python3
"""
PongTWKR v0.8 - CPU Module
CPU frequency, governor, turbo, and SMT management
"""

import os
import glob
from .utils import write_file
from .logger import log_change

def set_governor(value):
    """Set CPU governor for all cores"""
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    if not paths:
        print("⚠️ Governor not available for this system.")
        return
    
    for path in paths:
        try:
            with open(path, "w") as f:
                f.write(value)
        except PermissionError:
            print(f"⚠️ Error: Please use SUDO {path}")
        except OSError as e:
            print(f"⚠️ Error when writing governor to {path}: {e}")
    
    print(f"✅ CPU governor set to {value} in {len(paths)} cores")
    log_change(f"Governor set to {value}")

def set_cpu_min_freq(value):
    """Set CPU minimum frequency"""
    try:
        ghz = float(value)
        khz = int(ghz * 1_000_000)
    except ValueError:
        print("⚠️ Error: value must be a number (GHz).")
        return
    
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq")
    if not paths:
        print("⚠️ CPU min freq not available.")
        return
    
    for path in paths:
        try:
            with open(path, "w") as f:
                f.write(str(khz))
        except PermissionError:
            print(f"⚠️ Error: Please use SUDO {path}")
        except OSError as e:
            print(f"⚠️ Error when applying cpu min freq in {path}: {e}. Kernel refused.")
    
    print(f"✅ CPU min freq set to {ghz:.2f} GHz ({khz} kHz)")
    log_change(f"CPU min freq set to {ghz:.2f} GHz")

def set_cpu_max_freq(value):
    """Set CPU maximum frequency"""
    try:
        ghz = float(value)
        khz = int(ghz * 1_000_000)
    except ValueError:
        print("⚠️ Error: value must be a number (GHz).")
        return
    
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq")
    if not paths:
        print("⚠️ CPU max freq not available.")
        return
    
    for path in paths:
        try:
            with open(path, "w") as f:
                f.write(str(khz))
        except PermissionError:
            print(f"⚠️ Error: Please use SUDO {path}")
        except OSError as e:
            print(f"⚠️ Error when applying cpu max freq en {path}: {e}. Kernel refused.")
    
    print(f"✅ CPU max freq set to {ghz:.2f} GHz ({khz} kHz)")
    log_change(f"CPU max freq set to {ghz:.2f} GHz")

def set_cputurbo(state):
    """Enable/disable CPU Turbo Boost (Intel) or Precision Boost (AMD)"""
    if state.lower() == "true":
        state = "on"
    elif state.lower() == "false":
        state = "off"
    else:
        print("⚠️ Error: cputurbo only accepts 'true' or 'false'.")
        return

    intel_path = "/sys/devices/system/cpu/intel_pstate/no_turbo"
    amd_path = "/sys/devices/system/cpu/cpufreq/boost"
    
    try:
        if os.path.exists(intel_path):
            val = "0" if state == "on" else "1"
            with open(intel_path, "w") as f:
                f.write(val)
            print(f"✅ Intel Turbo Boost set to {state}")
            log_change(f"Turbo Boost set to {state}")
        elif os.path.exists(amd_path):
            val = "1" if state == "on" else "0"
            with open(amd_path, "w") as f:
                f.write(val)
            print(f"✅ AMD Precision Boost set to {state}")
            log_change(f"Precision Boost set to {state}")
        else:
            print("⚠️ Turbo/Precision Boost not available on this system.")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except Exception as e:
        print(f"⚠️ Error when applying turbo/boost: {e}")

def set_smt(state):
    """Enable/disable SMT (Simultaneous Multi-Threading)"""
    path = "/sys/devices/system/cpu/smt/control"

    if state.lower() == "true":
        state = "on"
    elif state.lower() == "false":
        state = "off"
    else:
        print("⚠️ Error: smt only accepts 'true' or 'false'.")
        return

    try:
        if os.path.exists(path):
            with open(path, "w") as f:
                f.write(state)
            print(f"✅ SMT set to {state}")
            log_change(f"SMT set to {state}")
        else:
            print("⚠️ SMT control not available on this system.")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except Exception as e:
        print(f"⚠️ Error when applying SMT: {e}")