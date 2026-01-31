#!/usr/bin/env python3
"""
PongTWKR v0.8 - Network Module  
WiFi power, TCP settings, MTU, buffer sizes, offloading
"""

import os
import subprocess
from .utils import get_wifi_interfaces, get_physical_interfaces, parse_size
from .logger import log_change

def set_wifi_power(state):
    """Set WiFi power management"""
    if state.lower() not in ("true", "false"):
        print("⚠️ Error: wifi_power only accepts 'true' or 'false'.")
        return

    val = "on" if state.lower() == "false" else "off"
    wifi_ifaces = get_wifi_interfaces()

    if not wifi_ifaces:
        print("⚠️ No wifi interfaces found.")
        return

    for iface in wifi_ifaces:
        try:
            subprocess.run(["iw", "dev", iface, "set", "power_save", val], check=True)
            print(f"✅ Wifi power for {iface} set to {val}")
            log_change(f"Wifi power {iface} set to {val}")
        except Exception as e:
            print(f"⚠️ Error applying wifi power in {iface}: {e}")

def set_tcp_metrics(state):
    """Enable/disable TCP metrics save"""
    path = "/proc/sys/net/ipv4/tcp_no_metrics_save"

    if not os.path.exists(path):
        print("⚠️ TCP metrics is not available for IPv6-only or container systems.")
        return

    if state.lower() == "false":
        val = "1"
    elif state.lower() == "true":
        val = "0"
    else:
        print("⚠️ Error: tcpmetrics only accepts 'true' or 'false'.")
        return

    try:
        with open(path, "w") as f:
            f.write(val)
        print(f"✅ TCP metrics save set to {val} ({'disabled' if val=='1' else 'enabled'})")
        log_change(f"TCP metrics save set to {val}")
    except PermissionError:
        print("⚠️ Error: please use SUDO.")
    except Exception as e:
        print(f"⚠️ Error when applying TCP metrics: {e}")

def set_mtu_probing(mode):
    """Set MTU probing mode"""
    path = "/proc/sys/net/ipv4/tcp_mtu_probing"

    allowed = {
        "off": "0",
        "fail": "1",
        "always": "2"
    }

    if mode.lower() not in allowed:
        print("⚠️ Error: mtu_probing only accepts 'off', 'fail' or 'always'.")
        return

    if not os.path.exists(path):
        print("⚠️ MTU probing is not available on IPv6-only or container systems.")
        return

    try:
        with open(path, "w") as f:
            f.write(allowed[mode.lower()])
        print(f"✅ MTU probing set to {mode.lower()} ({allowed[mode.lower()]})")
        log_change(f"MTU probing set to {mode.lower()}")
    except PermissionError:
        print("⚠️ Error: please use SUDO to modify MTU probing.")
    except Exception as e:
        print(f"⚠️ Error when applying MTU probing: {e}")

def set_rmem(value):
    """Set maximum receive buffer size"""
    path = "/proc/sys/net/core/rmem_max"
    size = parse_size(value)
    if size is None:
        return
    
    try:
        with open(path, "w") as f:
            f.write(str(size))
        print(f"✅ rmem_max set to {size} bytes")
        log_change(f"rmem_max set to {size}")
    except PermissionError:
        print("⚠️ Error: please run with SUDO")
    except Exception as e:
        print(f"⚠️ Error when applying rmem_max: {e}")

def set_wmem(value):
    """Set maximum send buffer size"""
    path = "/proc/sys/net/core/wmem_max"
    size = parse_size(value)
    if size is None:
        return
    
    try:
        with open(path, "w") as f:
            f.write(str(size))
        print(f"✅ wmem_max set to {size} bytes")
        log_change(f"wmem_max set to {size}")
    except PermissionError:
        print("⚠️ Error: please run with SUDO")
    except Exception as e:
        print(f"⚠️ Error when applying wmem_max: {e}")

def set_offload(feature, state):
    """Set network offloading feature"""
    allowed_features = ["gro", "lro", "tso", "gso"]
    if feature.lower() not in allowed_features:
        print(f"⚠️ Error: offload only accepts {allowed_features}.")
        return

    val = "on" if state.lower() == "true" else "off" if state.lower() == "false" else None
    if val is None:
        print("⚠️ Error: offload only accepts 'true' or 'false'.")
        return

    interfaces = get_physical_interfaces()
    if not interfaces:
        print("⚠️ No physical network interfaces found...")
        return

    for iface in interfaces:
        try:
            subprocess.run(["ethtool", "-K", iface, feature.lower(), val], check=True)
            print(f"✅ Offload {feature} en {iface} set to {val}")
            log_change(f"Offload {feature} en {iface} set to {val}")
        except FileNotFoundError:
            print("⚠️ Error: 'ethtool' not found. Please install it.")
            return
        except subprocess.CalledProcessError:
            print(f"⚠️ {iface} does not support {feature}.")
        except PermissionError:
            print(f"⚠️ Error: please run with SUDO.")
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")