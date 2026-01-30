#!/usr/bin/env python3
# PongTWKR v0.6 - A simple system tweaker for Linux systems.
# Author: valter-byte (and copilot ty ty for saving me from my crashouts at 3am)
# License: GLP-3.0
# uhm yeah ik its messy but idc
# im lazy and tired ok
# Enjoy it lol
# if anyone reads this, thank you for installing and messing around with it <3
import sys
import glob
import re
try:
    import psutil
except ImportError:
    print("❌ Error: For PongTWKR to work, you need to have psutil installed. Install it with sudo pip install psutil or however you like.")
    sys.exit(1)
import os
import datetime
import subprocess
import json
c1 = "\033[38;5;242m" # Gris rancio
c2 = "\033[38;5;248m" # Gris medio
c3 = "\033[38;5;255m" # Blanco Mente Fría
rs = "\033[0m"        # Reset (Sybau!)
# -- Persistence Module --
def enable_persistence():
    save_profile("persistent_settings")
    service_path = "/etc/systemd/system/pongtwkr.service"
    script_path = os.path.abspath(sys.argv[0])
    current_user = os.environ.get('SUDO_USER') or os.environ.get('USER') or "root"
    
    service_content = f"""[Unit]
Description=PongTWKR Persistence Service
After=multi-user.target

[Service]
Type=oneshot
User=root
Environment=SUDO_USER={current_user}
ExecStart=/usr/bin/python3 {script_path} load persistent_settings
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
"""
    try:
        with open(service_path, "w") as f:
            f.write(service_content)
        subprocess.run(["systemctl", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "enable", "pongtwkr.service"], check=True)
        print(f"✅ Persistence enabled for user: {current_user}")
        log_change("Persistence service enabled successfully.")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# fuck thp, heres the "translator"
def clean_thp_value(raw):
    if "[" in raw and "]" in raw:
        return raw.split("[")[1].split("]")[0].strip()
    return raw.strip()
# ah, herese the wifi reading for ts profile
def get_wifi_status_raw():
    interfaces = get_wifi_interfaces()
    if not interfaces: return "N/A"
    try:
        res = subprocess.check_output(["iw", "dev", interfaces[0], "get", "power_save"]).decode()
        return "on" if "on" in res.lower() else "off"
    except: return "N/A"

def get_offload_status_raw(feature):
    interfaces = get_physical_interfaces()
    if not interfaces: return "N/A"
    try:
        res = subprocess.check_output(["ethtool", "-k", interfaces[0]]).decode()
        for line in res.splitlines():
            if feature in line.lower():
                return "on" if "on" in line.lower() and "off" not in line.lower().split(":")[-1] else "off"
    except: return "N/A"
# -- Profile saving/loading --
def save_profile(name):
    def read_file(path):
        try:
            with open(path) as f:
                return f.read().strip()
        except:
            return "N/A"

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
        "offload_gso": get_offload_status_raw("generic-segmentation-offload")
    }

    path = os.path.join(log_dir, f"{name}.json")
    with open(path, "w") as f:
        json.dump(profile, f, indent=4)
    print(f"✅ Profile '{name}' saved at {path}")
    log_change(f"Profile {name} saved")

def load_profile(name):
    path = os.path.join(log_dir, f"{name}.json")
    if not os.path.exists(path):
        print(f"⚠️ Profile '{name}' not found.")
        return
    with open(path) as f:
        profile = json.load(f)

    if "swappiness" in profile: set_swappiness(profile["swappiness"])
    if "dirty_ratio" in profile: set_dirty_ratio(profile["dirty_ratio"])
    if "dirty_background" in profile: set_dirty_background_ratio(profile["dirty_background"])
    if "cache_pressure" in profile: set_cache_pressure(profile["cache_pressure"])
    if "governor" in profile: set_governor(profile["governor"])
    if "cpu_min" in profile: set_cpu_min_freq(float(profile["cpu_min"]) / 1_000_000)
    if "cpu_max" in profile: set_cpu_max_freq(float(profile["cpu_max"]) / 1_000_000)
    if "turbo_status_intel" in profile or "turbo_status_amd" in profile:
        set_cputurbo("true" if profile.get("turbo_status_amd") == "1" or profile.get("turbo_status_intel") == "0" else "false")
    if "smt" in profile: set_smt("true" if profile["smt"] == "on" else "false")
    if "hugepages" in profile: set_hugepages(profile["hugepages"])
    if "thp" in profile:
        set_thp(clean_thp_value(profile["thp"]))
    if "rmem_max" in profile: set_rmem(profile["rmem_max"])
    if "wmem_max" in profile: set_wmem(profile["wmem_max"])
    if "tcp_metrics" in profile: 
        set_tcp_metrics("true" if profile["tcp_metrics"] == "1" else "false")
    if "mtu_probing" in profile:
        mtu_map = {"0": "off", "1": "on", "2": "always"}
        set_mtu_probing(mtu_map.get(profile["mtu_probing"], "off"))
    if "wifi_powersave" in profile:
        set_wifi_power("true" if profile["wifi_powersave"] == "on" else "false")
    if "offload_gro" in profile: set_offload("gro", "true" if profile["offload_gro"] == "on" else "false")
    if "offload_tso" in profile: set_offload("tso", "true" if profile["offload_tso"] == "on" else "false")
    if "offload_gso" in profile: set_offload("gso", "true" if profile["offload_gso"] == "on" else "false")

    print(f"✅ Profile '{name}' applied")
    log_change(f"Profile {name} applied")

#-- Log making --
def find_real_user():
    user = os.environ.get('SUDO_USER') or os.environ.get('USER')
    if user and user != 'root':
        return user
    try:
        users = [d for d in os.listdir('/home') if os.path.isdir(os.path.join('/home', d)) and d != 'lost+found']
        if users: return users[0]
    except: pass
    return 'root'
real_user = find_real_user()
log_dir = f"/home/{real_user}/.pongtwkr" if real_user != 'root' else "/root/.pongtwkr"

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "logs.txt")

#-- Log updating --
def log_change(action):
    try:
        with open(log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {action}\n")
    except:
        pass
# -- Disclaimers --
def show_param_info(param):
    print(infos.get(param, "Ups, theres no info for this..."))
    if param in ("dirtyratio", "dirtybackground", "cachepressure"):
        print("⚠️ Security: values out of range may cause instablity and kernel errors.")
    if param in ("cpumin", "cpumax"):
        print("⚠️ Beware: The CPU automatically tops itself. No matter if you do override, the values will be topped to the physical limits of your CPU")
    if param == "governor":
        print("⚠️ Beware: Some governors may not be available for all systems.")
    if param == "thp":
        print("⚠️ Note: Setting THP to 'always' may lead to performance degradation in some workloads.")
    if param == "hugepages":
        print("⚠️ Note: Setting a high number of HugePages may lead to memory allocation issues for other applications.")
    if param == "smt":
        print("⚠️ SMT Multithreading may not be available on all systems.")
# -- Value Cappers
def limit_value(name, value, min_val, max_val):
    try:
        val = int(value)
    except ValueError:
        print(f"⚠️ Error: {name} has to be an integer number.")
        return None
    if val < min_val or val > max_val:
        print(f"⚠️ {name} out of safe range ({val}). Re-adjusted to {max_val}. Use sudo pongtwkr <option> <value> override to override this safety module.")
        return max_val
    return val

def limit_float(name, value, min_val, max_val):
    try:
        val = float(value)
    except ValueError:
        print(f"⚠️ Error: {name} has to be a number. (float).")
        return None
    if val < min_val or val > max_val:
        print(f"⚠️ {name} out of safe range ({val}). Re-adjusted to {max_val}. Use sudo pongtwkr <option> <value> override to override this safety module.")
        return max_val
    return val

# -- Info Array --
infos = {
    "swappiness": "Swappiness is how sensible is the system to switching to SWAP instead of RAM. Safe range: 0-100.",
    "dirtyratio": "Dirty Ratio defines the maximum percentage of dirty memory before writing onto the disk. Safe range: 20-70%",
    "dirtybackground": "Same as dirty ratio, but writing onto the background instead of the disk. IT SHOULD ALWAYS BE LOWER THAN DIRTY RATIO. Safe range: 5-50",
    "cachepressure": "Controls the pressure over the cache (duh), safe values: 0-100",
    "governor": "Governors are presets that the CPU comes with. If you want performance, use sudo pongtwkr governor performance, if you want power saving, use powersave.",
    "cpumin": "Defines the minimum frequency for the CPU",
    "cpumax": "Defines the maximum frequency for the CPU.",
    "info": "Shows a quick set of info and tweaks made.",
    "ping": "Well... just pings google to see your ms.. what did you expect???",
    "thp": """Transparent HugePages (THP) is a kernel feature that allows the system to use larger memory pages, 
improving performance for applications that use large amounts of memory.""",
    "hugepages": """HugePages is a memory management feature that allows the allocation of large memory pages, "
which can improve performance for certain applications by reducing overhead and increasing TLB efficiency.""",
    "cputurbo": """Enables or disables CPU Turbo Boost (Intel) or Precision Boost (AMD),
which allows the CPU to run at higher frequencies under certain conditions for improved performance.""",
    "smt": "Simultaneous Multi-Threading (SMT) allows multiple threads to run on each CPU core, improving parallelism and performance in multi-threaded applications.",
    "offload": "Network offloading features (like GRO, LRO, TSO, GSO) help reduce CPU load by offloading certain network processing tasks to the network interface card (NIC).",
    "tcpmetrics": "TCP metrics saving allows the kernel to save and reuse TCP connection metrics, improving performance for frequently used connections.",
    "wifipower": "Wifi power management allows the system to save power by reducing the power consumption of wifi interfaces when not in use.",
    "mtuprobing": "MTU probing helps optimize network performance by dynamically adjusting the Maximum Transmission Unit (MTU) size based on network conditions.",
    "rmem": "Sets the maximum receive buffer size for network sockets, which can improve network performance for high-throughput applications.",
    "wmem": "Sets the maximum send buffer size for network sockets, which can improve network performance for high-throughput applications."
}
# wifi detection, made this so future updates are easier
def get_wifi_interfaces():
    interfaces = []
    for iface in glob.glob("/sys/class/net/*"):
        if os.path.isdir(os.path.join(iface, "wireless")):
            interfaces.append(os.path.basename(iface))
    return interfaces
def get_physical_interfaces():
    interfaces = []
    for iface in glob.glob("/sys/class/net/*"):
        name = os.path.basename(iface)
        if name == "lo":
            continue                    # <-- skips loopback and virtual thingies...
        if name.startswith(("docker", "virbr", "br-", "veth")):
            continue
        interfaces.append(name)
    return interfaces


# -- wifi power management --
def set_wifi_power(state):
    if state.lower() not in ("true", "false"):
        print("⚠️ Error: wifi_power only accepts 'true' or 'false'.")
        return

    val = "on" if state.lower() == "false" else "off"
    wifi_ifaces = get_wifi_interfaces()

    if not wifi_ifaces:
        print("⚠️ What the hell..? No wifi interfaces found.")
        return

    for iface in wifi_ifaces:
        try:
            subprocess.run(["iw", "dev", iface, "set", "power_save", val], check=True)
            print(f"✅ Wifi power for {iface} set to {val}")
            log_change(f"Wifi power {iface} set to {val}")
        except Exception as e:
            print(f"⚠️ Error applying wifi power in {iface}: {e}")
# -- tcp metrics --
def set_tcp_metrics(state):
    path = "/proc/sys/net/ipv4/tcp_no_metrics_save"

    if not os.path.exists(path):
        print("⚠️ TCP metrics is not avaiable for IPv6-only or container systems.")
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
# mtu probing
def set_mtu_probing(mode):
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
# the GREATEST rmem and wmem tweak you have ever seen:
def parse_size(value):
    try:
        val = str(value).lower()
        if val.endswith("k"):
            return int(val[:-1]) * 1024
        elif val.endswith("m"):
            return int(val[:-1]) * 1024 * 1024
        else:
            return int(val)
    except ValueError:
        print("⚠️ Error: Buffer size must be an integer or end with 'K' or 'M' for kilobytes/megabytes. (Ex. 256K, 4M, 1048576)")
        return None
def set_rmem(value):
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

# -- offloading toggles --

def set_offload(feature, state):
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
            print("⚠️ Error: 'ethtool' not found. Please install it to manage offloading features.")
            return
        except subprocess.CalledProcessError:
            print(f"⚠️ {iface} does not support {feature}.")
        except PermissionError:
            print(f"⚠️ Error: please run with SUDO.")
        except Exception as e:
            print(f"⚠️ Unexpected error when applying  {feature} in {iface}: {e}")


    # -- THP or sum --
def set_thp(mode):
    path = "/sys/kernel/mm/transparent_hugepage/enabled"
    mode = mode.lower()

    # yk kernel is kinda a pussy with the value names
    allowed = {
        "always": "always",
        "enabled": "always",   
        "never": "never",
        "disabled": "never",  
        "madvise": "madvise"
    }

    if mode not in allowed:
        print(f"⚠️ Error: THP only accepts 'always', 'never', or 'madvise' (aliases: enabled/disabled). You gave '{mode}'.")
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

# huge pages
def set_hugepages(count):
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

# -- smt and the intel variable --
def set_smt(state):
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


# -- turbo boost and amd or whatever yeah yk... --
def set_cputurbo(state):
   
    
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
# --- Swappiness ---
def set_swappiness(value):
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
        print("⚠️ Error: Please use SUDO. (Ex. sudo pongtwkr swappiness 100)")
    except OSError as e:
        print(f"⚠️ Error when applying swappiness: {e}. The kernel refused")

# --- Governor ---
def set_governor(value):
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
            print(f"⚠️ Error when writing governor to {path}: {e} Please send this to me.")
    print(f"✅ CPU governor set to {value} in {len(paths)} cores")
    log_change(f"Governor set to {value}")

# --- Dirty Ratio ---
def set_dirty_ratio(value):
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
        print(f"⚠️ Error when applying dirty_ratio: {e}. Invalid value for the kernel. Remember its a percentage value. (Max. 100)")

# --- Dirty Background Ratio ---
def set_dirty_background_ratio(value):
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
        print(f"⚠️ Error when applying dirty_ratio: {e}. Invalid value for the kernel. Remember its a percentage value. (Max. 100)")

# --- Cache Pressure ---
def set_cache_pressure(value):
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
    except OSError as e:
        print(f"⚠️ Error when applying vfs_cache_pressure: {e}. Please send this error to me.")

# --- CPU min/max freq ---
def set_cpu_min_freq(value):
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

# --- Reset defaults --
defaults = {}
def save_defaults():
    defaults_path = os.path.join(log_dir, "original_defaults.json")
    if os.path.exists(defaults_path):
        return
    
    print("📦 First run detected! Backing up your original system defaults...")
    paths = {
        "swappiness": "/proc/sys/vm/swappiness",
        "dirtyratio": "/proc/sys/vm/dirty_ratio",
        "dirtybackground": "/proc/sys/vm/dirty_background_ratio",
        "cachepressure": "/proc/sys/vm/vfs_cache_pressure",
        "cputurbo_intel": "/sys/devices/system/cpu/intel_pstate/no_turbo",
        "cputurbo_amd": "/sys/devices/system/cpu/cpufreq/boost",
        "smt": "/sys/devices/system/cpu/smt/control",
        "hugepages": "/proc/sys/vm/nr_hugepages",
        "thp": "/sys/kernel/mm/transparent_hugepage/enabled",
        "tcpmetrics": "/proc/sys/net/ipv4/tcp_no_metrics_save", "mtuprobing": "/proc/sys/net/ipv4/tcp_mtu_probing", 
        "rmem_max": "/proc/sys/net/core/rmem_max",
        "wmem_max": "/proc/sys/net/core/wmem_max"
    }

    original_data = {}
    for param, path in paths.items():
        try:
            if os.path.exists(path):
                with open(path) as f:
                    raw_val = f.read().strip()
                    if param == "thp":
                        original_data[param] = clean_thp_value(raw_val)
                    else:
                        original_data[param] = raw_val
            else:
                original_data[param] = None
        except Exception as e:
            print(f"⚠️ Could not backup {param}: {e}")
            original_data[param] = None
    try:
        with open(defaults_path, "w") as f:
            json.dump(original_data, f, indent=4)
        print(f"✅ Backup created successfully at {defaults_path}")
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not save defaults JSON: {e}")

def reset_defaults():
    defaults_path = os.path.join(log_dir, "original_defaults.json")
    if not os.path.exists(defaults_path):
        print("⚠️ Error: No original defaults found. So... just run sudo pongtwkr safe...")
        return
    with open(defaults_path) as f:
        original_data = json.load(f)
    actions = {
        "swappiness": set_swappiness,
        "dirtyratio": set_dirty_ratio,
        "dirtybackground": set_dirty_background_ratio,
        "cachepressure": set_cache_pressure,
        "smt": set_smt,
        "hugepages": set_hugepages,
        "thp": set_thp,
        "tcpmetrics": set_tcp_metrics,
        "mtuprobing": set_mtu_probing, 
        "rmem_max": set_rmem, 
        "wmem_max": set_wmem
    }

    print("🔄 [RESET] Restoring system to default settings...")
    for param, val in original_data.items():
        if val is not None and val != "N/A":
            if param in actions:
                actions[param](val)
            elif param == "cputurbo_intel" and val is not None:
                set_cputurbo("true" if val == "0" else "false")
            elif param == "cputurbo_amd" and val is not None:
                set_cputurbo("true" if val == "1" else "false")

    print("✅ System successfully restored to the first-run state.")


# --- Safe profile ---
def safe_profile():
    set_swappiness(60)
    set_governor("powersave")
    set_dirty_ratio(20)
    set_dirty_background_ratio(10)
    set_cache_pressure(50)
    set_cputurbo("true")
    set_smt("true")
    set_hugepages(0)
    set_thp("madvise")
    set_tcp_metrics("false")
    set_mtu_probing("off")
    set_rmem("212992")
    set_wmem("212992")
    print("✅ Safe profile applied")
    log_change("Safe profile applied")

# Ping

def ping_test(host="8.8.8.8"):
    try:
        out = subprocess.check_output(["ping", "-c", "1", "-W", "2", host],
                                     universal_newlines=True,
                                     stderr=subprocess.STDOUT)

        match = re.search(r"time=([\d.]+)|tiempo=([\d.]+)", out)

        if match:
            ms = match.group(1) or match.group(2)
            print(f"🏓 Pong! {ms} ms")
        else:
            print(f"⚠️ Ping output failed.")

    except subprocess.CalledProcessError:
        print(f"⚠️ Ping failed: No answer from {host}.")
    except Exception as e:
        print(f"⚠️ You found a mega-hiper-strange error, please send it to me: {e}")
# def not the easter egg
def show_info_war():
    print(f"""
    ☢️ Designated Warheads: ALPHA & BETA
    📌 Designated objectives: Marked 35 cities in the USA.
    ✝️ Estimated casualties: +700 million
    ⏳ Time for impact: T-15 seconds for launch."
    🖥️ Executing command: sudo rm -rf / --no-preserve-root)
    Thank you, AGENT FINN MC MISSILE. Proceeding with launch...""")

# getting fan speeds, this is 100% not working
def get_all_fan_speeds(): 
    fan_speeds = [] 
    try: 
        fan_paths = glob.glob("/sys/class/hwmon/hwmon*/fan*_input") 
        for path in fan_paths: 
            try: 
                with open(path) as f: 
                    val = f.read().strip() 
                    if val.isdigit(): 
                        label = path.split("/")[-2] + "/" + path.split("/")[-1] 
                        fan_speeds.append(f"{label}: {val} RPM") 
            except: 
                    continue 
    except: 
        pass 
    return fan_speeds if fan_speeds else ["N/A"]
# amd intel translator
def format_turbo_status(intel_val, amd_val):
    if intel_val in ("0", "1"):
        return "Enabled" if intel_val == "0" else "Disabled"
    elif amd_val in ("0", "1"):
        return "Enabled" if amd_val == "1" else "Disabled"
    else:
        return "N/A"

# --- fakefetch ---
def show_info():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    threads = psutil.cpu_count(logical=True)
    cores = psutil.cpu_count(logical=False)

    def read_file(path):
        try:
            with open(path) as f:
                return f.read().strip()
        except:
            return "N/A"

    swappiness = read_file("/proc/sys/vm/swappiness")
    dirty_ratio = read_file("/proc/sys/vm/dirty_ratio")
    dirty_background = read_file("/proc/sys/vm/dirty_background_ratio")
    cache_pressure = read_file("/proc/sys/vm/vfs_cache_pressure")
    governor = read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    cpu_min = read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq")
    cpu_max = read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq")
    turbo_status_intel = read_file("/sys/devices/system/cpu/intel_pstate/no_turbo")
    turbo_status_amd = read_file("/sys/devices/system/cpu/cpufreq/boost")
    smt_status = read_file("/sys/devices/system/cpu/smt/control")
    hugepages_status = read_file("/proc/sys/vm/nr_hugepages")
    thp_status = read_file("/sys/kernel/mm/transparent_hugepage/enabled")
    fan_speed = get_all_fan_speeds()
    uptime_raw = read_file("/proc/uptime")
    process_count = str(len(psutil.pids()))
    tcp_metrics = read_file("/proc/sys/net/ipv4/tcp_no_metrics_save")
    mtu_probing = read_file("/proc/sys/net/ipv4/tcp_mtu_probing")
    rmem_max = read_file("/proc/sys/net/core/rmem_max")
    wmem_max = read_file("/proc/sys/net/core/wmem_max")
    try:
        wifi_power = subprocess.check_output(["iw", "dev", "wlan0", "get", "power_save"]).decode().strip()
    except:
        wifi_power = "N/A"
    def khz_to_ghz(val):
        try:
            return f"{int(val) / 1_000_000:.2f} GHz"
        except:
            return "N/A"

    cpu_min_ghz = khz_to_ghz(cpu_min)
    cpu_max_ghz = khz_to_ghz(cpu_max)

    # fakefetch disclaimers
    if swappiness.isdigit() and int(swappiness) > 100:
        print("⚠️ Swappiness out of range. It may cause performance issues.")
    if dirty_ratio.isdigit() and int(dirty_ratio) > 70:
        print("⚠️ Dirty Ratio out of range. It may cause performance issues.")
    if dirty_background.isdigit() and int(dirty_background) > 50:
        print("⚠️ Dirty Background Ratio out of range. It may cause performance issues.")
    if cache_pressure.isdigit() and int(cache_pressure) > 100:
        print("⚠️ vfs_cache_pressure out of range. It may cause performance issues.")
    if hugepages_status.isdigit() and int(hugepages_status) > 2046:
        print("⚠️ HugePages count unusually high.")
    try:
        if cpu_min.isdigit() and int(cpu_min) > 6_000_000:
            print("⚠️ CPU min freq unusually high (Check...).")
    except:
        pass    
    try:
        if cpu_max.isdigit() and int(cpu_max) > 6_000_000:
            print("⚠️ CPU max freq unusually high (Check...).")
    except:
        pass
    try:
        if rmem_max.isdigit():
            rmem_val = int(rmem_max)
            if rmem_val < 65536 or rmem_val > 16777216:
                print("⚠️ rmem_max out of safe range. It may cause instability.")
        if wmem_max.isdigit():
            wmem_val = int(wmem_max)
            if wmem_val < 65536 or wmem_val > 16777216:
                print("⚠️ wmem_max out of safe range. It may cause instability.")
    except:
        pass
        # --- Network info additions ---
    mtu_map = {"0": "Off", "1": "Fail only", "2": "Always"}
    mtu_text = mtu_map.get(mtu_probing, mtu_probing)

    tcp_text = "Disabled" if tcp_metrics == "1" else "Enabled" if tcp_metrics == "0" else tcp_metrics

#MB and KB yk formatter
    def format_bytes(val):
        try:
            val = int(val)
            if val >= 1024*1024:
                return f"{val // (1024*1024)} MB"
            elif val >= 1024:
                    return f"{val // 1024} KB"
            else:
                return f"{val} B"
        except:
            return val



    # --- ASCII Pong + Logo ---
    ascii_art = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║╔════════════════════════════════════════════════════════════════════════════╗║
║║                         ██████╗     |   ██╗  ██╗                           ║║
║║                         ╚════██╗    |   ██║  ██║                           ║║
║║  █                      █████╔╝     |   ███████║                           ║║
║║  █                      ╚═══██╗     |   ╚════██║                           ║║
║║  █                     ██████╔╝     |        ██║                           ║║
║║  █                     ╚═════╝      |        ╚═╝                           ║║
║║  █                                  |                                      ║║
║║                           ╔╗        |                                      ║║
║║                           ╚╝        |                                      ║║
║║                                     |                                      ║║
║║                                     |                                      ║║
║║                                     |                                      ║║
║║                                     |                                      ║║
║║                                     |                                 █    ║║
║║                                     |                                 █    ║║
║║                                     |                                 █    ║║
║║                                     |                                 █    ║║
║║                                     |                                 █    ║║
║║                                     |                                      ║║
║║                                     |                                      ║║
║╚════════════════════════════════════════════════════════════════════════════╝║
╚══════════════════════════════════════════════════════════════════════════════╝
{c1}$$$$$$$\   $$$$$$\  $$\   $$\  $$$$$$\ $$$$$$$$\ $$\      $$\ $$\   $$\ $$$$$$$\  
{c1}$$  __$$\ $$  __$$\ $$$\  $$ |$$  __$$\\__$$  __|$$ | $\  $$ |$$ | $$  |$$  __$$\ 
{c2}$$ |  $$ |$$ /  $$ |$$$$\ $$ |$$ /  \__|  $$ |   $$ |$$$\ $$ |$$ |$$  / $$ |  $$ |
{c2}$$$$$$$  |$$ |  $$ |$$ $$\$$ |$$ |$$$$\   $$ |   $$ $$ $$\$$ |$$$$$  /  $$$$$$$  |
{c3}$$  ____/ $$ |  $$ |$$ \$$$$ |$$ |\_$$ |  $$ |   $$$$  _$$$$ |$$  $$<   $$  __$$< 
{c3}$$ |      $$ |  $$ |$$ |\$$$ |$$ |  $$ |  $$ |   $$$  / \$$$ |$$ |\$$\  $$ |  $$ |
{c3}$$ |       $$$$$$  |$$ | \$$ |\$$$$$$  |  $$ |   $$  /   \$$ |$$ | \$$\ $$ |  $$ |
{c3}\__|       \______/ \__|  \__| \______/   \__|   \__/     \__|\__|  \__|\__|  \__|{rs}
"""
    ascii_art = ascii_art.format(c1="\033[95m", c2="\033[94m", c3="\033[92m", rs="\033[0m")
    info_lines = [
        f"💾 RAM: {mem.available // (1024**2)} MB libres / {mem.total // (1024**2)} MB totales",
        f"⚙️ CPU usage per core: {cpu_usage}",
        f"🧵 Threads: {threads} | Physical Cores: {cores}",
        f"🔧 Swappiness: {swappiness}",
        f"📝 vm.dirty_ratio: {dirty_ratio}",
        f"📝 vm.dirty_background_ratio: {dirty_background}",
        f"📝 vm.vfs_cache_pressure: {cache_pressure}",
        f"🚀 Turbo/Precision Boost: {format_turbo_status(turbo_status_intel, turbo_status_amd)}",
        f"🧬 SMT: {smt_status}",
        f"📄 HugePages: {hugepages_status}",
        f"📄 THP: {thp_status}",
        *[f"🌀 {fs}" for fs in fan_speed],
        f"⏱️ Uptime: {int(float(uptime_raw.split()[0])) // 3600} hours",
        f"⚙️ Processes running: {process_count}",
        f"⚡ Governor: {governor}",
        f"⚡ CPU min freq: {cpu_min_ghz}",
        f"⚡ CPU max freq: {cpu_max_ghz}",
        f"💾 Swap: {swap.used // (1024**2)} MB used / {swap.total // (1024**2)} MB total",
        f"📂 Buffers: {mem.buffers // (1024**2)} MB | Cached: {mem.cached // (1024**2)} MB",
        f"📊 TCP Metrics Save: {tcp_text}",
        f"📡 MTU Probing: {mtu_text}", 
        f"📦 rmem_max: {format_bytes(rmem_max)}", 
        f"📦 wmem_max: {format_bytes(wmem_max)}", 
        f"⚙ Wifi Power: {wifi_power}", 
    ]
    # merge ascii and fetch
    ascii_lines = ascii_art.splitlines()
    max_len = max(len(line) for line in ascii_lines)
    for i in range(max(len(ascii_lines), len(info_lines))):
        left = ascii_lines[i] if i < len(ascii_lines) else " " * max_len
        right = info_lines[i] if i < len(info_lines) else ""
        print(f"{left:<{max_len}}   {right}")


# main ig, justs tell you how to use if u do sudo pongtwkr
if __name__ == "__main__":
    save_defaults()

    if len(sys.argv) < 2:
        print("Usage: pongtwkr <option> [value]")
        sys.exit(1)

    option = sys.argv[1]
    
    # Definimos qué opciones requieren obligatoriamente un segundo argumento (sys.argv[2])
    needs_value = [
        "swappiness", "cputurbo", "smt", "governor", "thp", 
        "dirtyratio", "dirtybackground", "cachepressure", 
        "hugepages", "cpumin", "cpumax", "save", "load"
    ]

    # Validación global de argumentos para comandos que requieren valor
    if option in needs_value and len(sys.argv) < 3:
        print(f"⚠️ Error: The option '{option}' requires a value.")
        print(f"Usage: sudo pongtwkr {option} <value>")
        sys.exit(1)

    # Override kinda
    option = sys.argv[1]

    override = "override" in sys.argv

    if option == "swappiness":
        if override:
            set_swappiness(sys.argv[2])
        else:
            val = limit_value("Swappiness", sys.argv[2], 0, 100)
            if val is not None:
                set_swappiness(val)
    elif option == "cputurbo": 
        set_cputurbo(sys.argv[2])
    elif option == "smt": 
        set_smt(sys.argv[2])
    elif option == "governor":
        set_governor(sys.argv[2])
    elif option == "thp": 
        set_thp(sys.argv[2])
    elif option == "dirtyratio":
        if override:
            set_dirty_ratio(sys.argv[2])
        else:
            val = limit_value("Dirty Ratio", sys.argv[2], 0, 70)
            if val is not None:
                set_dirty_ratio(val)

    elif option == "dirtybackground":
        if override:
            set_dirty_background_ratio(sys.argv[2])
        else:
            val = limit_value("Dirty Background Ratio", sys.argv[2], 0, 50)
            if val is not None:
                set_dirty_background_ratio(val)

    elif option == "cachepressure":
        if override:
            set_cache_pressure(sys.argv[2])
        else:
            val = limit_value("Cache Pressure", sys.argv[2], 0, 1000)
            if val is not None:
                set_cache_pressure(val)
    elif option == "hugepages":
        if override:
            set_hugepages(sys.argv[2])
        else:
            val = limit_value("HugePages", sys.argv[2], 0, 2046)
            if val is not None:
                set_hugepages(val)
    elif option == "cpumin":
        if override:
            set_cpu_min_freq(sys.argv[2])
            print(f"The value tops with your CPU: no matter if you use override, it will top to the physical limit of your CPU.")
        else:
            val = limit_float("CPU min freq (GHz)", sys.argv[2], 0.5, 6.0)
            if val is not None:
                set_cpu_min_freq(val)

    elif option == "cpumax":
        if override:
            set_cpu_max_freq(sys.argv[2])
            print(f"The value tops with your CPU: no matter if you use override, it will top to the physical limit of your CPU.")
        else:
            val = limit_float("CPU max freq (GHz)", sys.argv[2], 0.5, 6.0)
            if val is not None:
                set_cpu_max_freq(val)

    elif option == "info":
         if override:
             print(f"🚀 [WARNING] INFO OVERRIDE MODE ACTIVATED.")
             print(f"☢️ NUCLEAR WARHEADS ALPHA & BETA ACTIVE AND POINTING TO DALLAS, HOUSTON AND NEW YORK.")
             print(f"🛰️ SATELLITE UPLINK ESTABLISHED. THANK YOU, MR. PUTIN.")
             show_info_war()
         else:
            show_info()
    elif option == "save": 
        if len(sys.argv) < 3: 
            print("⚠️ Please provide a profile name.") 
        elif sys.argv[2] == "persistent_settings" or sys.argv[2] == "original_defaults":
            print("❌ Yeah bro... that name is reserved.")
        else: 
            save_profile(sys.argv[2]) 

    elif option == "load": 
        if len(sys.argv) < 3: 
            print("⚠️ Please provide a profile name.") 
        elif sys.argv[2] == "persistent_settings" or sys.argv[2] == "original_defaults":
            if os.getuid() != 0: # <-- useless security method that only works on sum distros
                print("❌ Yeah bro... that name is reserved for system persistence.")
            else:
                load_profile(sys.argv[2])
        else: 
            load_profile(sys.argv[2])
    elif option == "rmem":
        if override:
            set_rmem(sys.argv[2])
        else:
            val = parse_size(sys.argv[2])
            if val is not None:
                val = limit_value("rmem_max", val, 65536, 16777216)
                if val is not None:
                    set_rmem(val)

    elif option == "wmem":
        if override:
            set_wmem(sys.argv[2])
        else:
            val = parse_size(sys.argv[2])
            if val is not None:
                val = limit_value("wmem_max", val, 65536, 16777216)
                if val is not None:
                    set_wmem(val)
    elif option == "offload":
        if len(sys.argv) < 4:
            print("⚠️ Use: pongtwkr offload <feature> <true/false>. Features are: gro, gso, tso, ufo, sg, rx, tx.")
        else:
            set_offload(sys.argv[2], sys.argv[3])

    elif option == "reset":
        reset_defaults()
    elif option == "wifipower":
        set_wifi_power(sys.argv[2])
    elif option == "tcpmetrics":
        set_tcp_metrics(sys.argv[2])
    elif option == "mtuprobing":
        set_mtu_probing(sys.argv[2])

    elif option == "safe":
        safe_profile()

    elif option == "ping":
        ping_test()
    elif option == "persist":
        enable_persistence()
    else:
        print("⚠️ Unknown option or bad usage. Please refer to the documentation for further help.")

