#!/usr/bin/env python3
"""
PongTWKR v0.8 - RAM Module
Memory management: swappiness, dirty ratios, cache, hugepages, THP, NUMA
"""

from datetime import time
import os
import subprocess
from .utils import parse_size_2
import psutil
from .logger import log_change

def set_swappiness(value):
    """Set swappiness value"""
    try:
        ival = int(value)
    except ValueError:
        print("⚠️ Error: swappiness has to be an integer.")
        return
    
    try:
        with open("/proc/sys/vm/swappiness", "w") as f:
            f.write(str(ival))
        print(f"✅ Swappiness set to {ival}")
        log_change(f"Swappiness set to {ival}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except OSError as e:
        print(f"⚠️ Error when applying swappiness: {e}. The kernel refused")

def set_dirty_ratio(value):
    """Set dirty ratio"""
    try:
        ival = int(value)
    except ValueError:
        print("⚠️ Error: dirty_ratio has to be an integer number from 1 to 100.")
        return
    
    try:
        with open("/proc/sys/vm/dirty_ratio", "w") as f:
            f.write(str(ival))
        print(f"✅ vm.dirty_ratio set to {ival}")
        log_change(f"Dirty Ratio set to {ival}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except OSError as e:
        print(f"⚠️ Error when applying dirty_ratio: {e}.")

def set_dirty_background_ratio(value):
    """Set dirty background ratio"""
    try:
        ival = int(value)
    except ValueError:
        print("⚠️ Error: dirty_background_ratio has to be an integer number from 1 to 100.")
        return
    
    try:
        with open("/proc/sys/vm/dirty_background_ratio", "w") as f:
            f.write(str(ival))
        print(f"✅ vm.dirty_background_ratio set to {ival}")
        log_change(f"Dirty Background Ratio set to {ival}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except OSError as e:
        print(f"⚠️ Error when applying dirty_background_ratio: {e}.")

def set_cache_pressure(value):
    """Set VFS cache pressure"""
    try:
        ival = int(value)
    except ValueError:
        print("⚠️ Error: cache_pressure has to be an integer number.")
        return
    
    try:
        with open("/proc/sys/vm/vfs_cache_pressure", "w") as f:
            f.write(str(ival))
        print(f"✅ vm.vfs_cache_pressure set to {ival}")
        log_change(f"Cache Pressure set to {ival}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except Exception as e:
        print(f"⚠️ Error when applying vfs_cache_pressure: {e}.")

def set_hugepages(count):
    """Set number of huge pages"""
    path = "/proc/sys/vm/nr_hugepages"
    try:
        with open(path, "w") as f:
            f.write(str(count))
        print(f"✅ HugePages set to {count}")
        log_change(f"HugePages set to {count}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except Exception as e:
        print(f"⚠️ Error when applying HugePages: {e}")

def set_thp(mode):
    """Set Transparent Huge Pages mode"""
    path = "/sys/kernel/mm/transparent_hugepage/enabled"
    mode = mode.lower()

    allowed = {
        "always": "always",
        "enabled": "always",   
        "never": "never",
        "disabled": "never",  
        "madvise": "madvise"
    }

    if mode not in allowed:
        print(f"⚠️ Error: THP only accepts 'always', 'never', or 'madvise'. You gave '{mode}'.")
        return

    try:
        with open(path, "w") as f:
            f.write(allowed[mode])
        print(f"✅ Transparent HugePages set to {allowed[mode]}")
        log_change(f"THP set to {allowed[mode]}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except Exception as e:
        print(f"⚠️ Error when applying THP: {e}")

def set_numa_balancing(state):
    """Enable/disable NUMA balancing"""
    path = "/proc/sys/kernel/numa_balancing"
    if not os.path.exists(path):
        print("⚠️ NUMA Balancing not supported by your CPU/Kernel.")
        return
    
    s = str(state).lower()
    if s in ["true", "on", "1", "y", "yes", "enable"]:
        val = "1"
        msg = "ENABLED"
    elif s in ["false", "off", "0", "n", "no", "disable"]:
        val = "0"
        msg = "DISABLED"
    else:
        print(f"⚠️ Invalid value '{state}' for NUMA Balancing. Must be 'true' or 'false'")
        return

    try:
        with open(path, "w") as f:
            f.write(val)
        print(f"✅ NUMA Balancing is now {msg}.")
        log_change(f"NUMA Balancing set to {val}")
    except PermissionError:
        print("⚠️ Please run with SUDO")
    except Exception as e:
        print(f"❌ ERROR: {e}")

# here starts ZSWAP
# zswap pools
def set_zswap_pool(percent):
    path = "/sys/module/zswap/parameters/max_pool_percent"
    if not os.path.exists(path):
        print("⚠️ ZSWAP Pool management not available on this system.")
        return
    try:
        with open(path, "w") as f:
            f.write(str(percent))
        print(f"✅ ZSWAP Max Pool set to {percent}%")
        log_change(f"ZSWAP Max Pool set to {percent}%")
    except PermissionError:
        print("⚠️ Please run with SUDO")
    except Exception as e:
        print(f"❌ ERROR: {e}")
# zswap algos
def set_zswap_algo(algo):
    path_algo = "/sys/module/zswap/parameters/compressor"
    path_available = "/sys/kernel/debug/zswap/available_compressors"  
    if not os.path.exists(path_algo):
        print("⚠️ ZSWAP not available or not enabled in Kernel.")
        return
    algo = algo.lower().strip()
    available = []
    if os.path.exists(path_available):
        try:
            with open(path_available, "r") as f:
                available = f.read().strip().split()
        except PermissionError:
            pass 
    if available and algo not in available:
        print(f"⚠️ Invalid ZSWAP algo '{algo}'. Available: {', '.join(available)}")
        return
    try:
        with open(path_algo, "w") as f:
            f.write(algo)
        print(f"✅ ZSWAP Compressor set to {algo}")
    except OSError:
        print(f"❌ ERROR: Algorithm '{algo}' is not supported by your Kernel. (Check /sys/kernel/debug/zswap/available_compressors) ")

    except PermissionError:
        print("⚠️ Please run with SUDO")
    except Exception as e:
        print(f"❌ ERROR: {e}")
# -- zswap enable/disable --
def set_zswap_enabled(state):
    path = "/sys/module/zswap/parameters/enabled"
    if not os.path.exists(path):
        print("⚠️ ZSWAP not supported by your Kernel...")
        return
    s = str(state).lower()
    if s in ["true", "on", "1", "y", "yes"]:
        val = "Y"
        msg = "ENABLED"
    elif s in ["false", "off", "0", "n", "no"]:
        val = "N"
        msg = "DISABLED"
    else:
        print(f"⚠️ '{state}' Is not a valid state. Please use true/false")
        return
    try:
        with open(path, "w") as f:
            f.write(val)
        print(f"✅ ZSWAP is now {msg}.")
        log_change(f"ZSWAP enabled set to {val}")
    except PermissionError:
        print("⚠️ Please run with SUDO")
    except Exception as e:
        print(f"❌ ERROR: {e}")
# here is size
def set_zramsize(new_size):
    path_reset = "/sys/block/zram0/reset"
    path_algo = "/sys/block/zram0/comp_algorithm"
    path_size = "/sys/block/zram0/disksize"

    if not os.path.exists(path_size):
        print("⚠️ ZRAM not available.")
        return

    size_bytes = parse_size_2(new_size) 
    if size_bytes is None: return

    try:
        with open(path_algo, "r") as f:
            current_algo = f.read().split('[')[1].split(']')[0] # <another shitty kernell translator.
        result = subprocess.run(["sudo", "swapoff", "/dev/zram0"], stderr=subprocess.DEVNULL)
        
        if result.returncode != 0:
            print("⚠️ Warning: swapoff failed... do you have enough RAM?")

        
        import time
        time.sleep(1)

        with open(path_reset, "w") as f:
            f.write("1")
        with open(path_algo, "w") as f:
            f.write(current_algo)
        with open(path_size, "w") as f:
            f.write(str(size_bytes))
        subprocess.run(["mkswap", "/dev/zram0"], check=True, capture_output=True)
        subprocess.run(["swapon", "/dev/zram0", "-p", "100"], check=True, capture_output=True)
        print(f"✅ ZRAM Resized to {new_size} ({size_bytes} bytes).")
        log_change(f"ZRAM Resized to {new_size}")

    except Exception as e:
        print(f"❌ ERROR:{e}")

def set_zramalgo(algo):
    path = "/sys/block/zram0/comp_algorithm"
    if not os.path.exists(path):
        print("⚠️ ZRAM algos not available on this system.")
        return
    try:
        with open(path, "r") as f:
            available = [a.replace("[", "").replace("]", "") for a in f.read().strip().split()]
        if algo not in available:
            print(f"⚠️ Invalid algorithm '{algo}'. Available: {', '.join(available)}")
            return
    except Exception as e:
        print(f"⚠️ Could not read available algorithms: {e}")
        return
    try:
        # preserve size
        with open("/sys/block/zram0/disksize", "r") as f:
            current_size = f.read().strip()
        # checking it out ykyk
        try:
            active_swaps = subprocess.check_output(["swapon", "--show"]).decode()
            if "/dev/zram0" in active_swaps:
                subprocess.run(["swapoff", "/dev/zram0"], check=True)
        except subprocess.CalledProcessError:
            print("⚠️ Warning: swapoff failed, maybe not active. Continuing...")
        # clean reset
        with open("/sys/block/zram0/reset", "w") as f:
            f.write("1")
        with open("/sys/block/zram0/comp_algorithm", "w") as f:
            f.write(algo)
        with open("/sys/block/zram0/disksize", "w") as f:
            f.write(current_size)
        # re-make swap
        subprocess.run(["mkswap", "/dev/zram0"], check=True)
        subprocess.run(["swapon", "/dev/zram0", "-p", "100"], check=True)
        print(f"✅ ZRAM Algorithm set to {algo} (Size {current_size} preserved).")
        log_change(f"ZRAM Algorithm set to {algo}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except Exception as e:
        print(f"❌ ERROR: Something went wrong: {e}")
# streams thingy
def set_zramstreams(streams):
    path = "/sys/block/zram0/max_comp_streams"
    if not os.path.exists(path):
        print("⚠️ ZRAM streams not available on this system.")
        return
    if isinstance(streams, str) and streams.lower() == "all":
        val = 0
    else:
        try:
            val = int(streams)
        except ValueError:
            print("⚠️ Error: streams must be an integer or 'all'.")
            return
    if val == 0 and (isinstance(streams, str) and streams != "all"):
        print("⚠️ Error: value should be more than 0. Use 'all' if you want auto mode.")
        return
    max_streams = psutil.cpu_count(logical=True)
    if val > max_streams:
        print(f"⚠️ Warning: streams capped to {max_streams} (CPU thread count).")
        val = max_streams
    try:
        with open(path, "w") as f:
            f.write(str(val))
        if val == 0:
            print("✅ ZRAM compression streams set to auto (all cores).")
            log_change("ZRAM compression streams set to auto (all cores)")
        else:
            print(f"✅ ZRAM compression streams set to {val}")
            log_change(f"ZRAM compression streams set to {val}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO.")
    except Exception as e:
        print(f"❌ ERROR: Something went wrong: {e}")
