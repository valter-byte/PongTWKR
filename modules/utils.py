#!/usr/bin/env python3
"""
PongTWKR v0.8 - Utility Functions
Helper functions for value parsing, validation, and file operations
"""

import glob
import json
import psutil
import os
import subprocess
import platform


def reset_defaults():
    defaults_path = os.path.join(log_dir, "original_defaults.json")
    if not os.path.exists(defaults_path):
        print("⚠️ Error: No original defaults found. So... just run sudo pongtwkr safe...")
        return
    from modules import cpu, ram, net
    from modules.ram import (
    set_cache_pressure, set_dirty_background_ratio,
    set_dirty_ratio, set_hugepages, set_numa_balancing, 
    set_swappiness, set_thp, set_zramalgo, set_zramsize, 
    set_zramstreams,set_zswap_algo, set_zswap_enabled, set_zswap_pool)
    from modules.cpu import set_smt, set_cputurbo
    from modules.net import set_mtu_probing, set_rmem, set_tcp_metrics, set_wmem
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
        "wmem_max": set_wmem,
        "zram_algo": set_zramalgo,
        "zram_size": set_zramsize,
        "zram_streams": set_zramstreams,
        "zswap_enabled": set_zswap_enabled,
        "zswap_algo": set_zswap_algo,
        "zswap_pool": set_zswap_pool,
        "numa_balancing": set_numa_balancing
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
    if "disks" in original_data:
        from modules import disks
        print("💿 [RESET] Restoring disk schedulers and NCQ...")
        for disk_name, settings in original_data["disks"].items():
            
            if "scheduler" in settings:
                disks.set_io_scheduler(disk_name, settings["scheduler"])
                
            if "ncq_depth" in settings:
                disks.set_ncq_depth(disk_name, settings["ncq_depth"])
                
            if "max_sectors" in settings:
                disks.set_max_sectors(disk_name, settings["max_sectors"])
            if "runtime_pm" in settings:
                is_perf = True if settings["runtime_pm"] == "on" else False
                disks.set_runtime_pm(disk_name, is_perf)
    print("✅ System successfully restored to the first-run state.")

def safe_profile():
    from modules import cpu, ram, net
    from modules.logger import log_change
    from modules.cpu import set_governor, set_cputurbo, set_smt
    from modules.ram import (
        set_swappiness, set_dirty_ratio, set_dirty_background_ratio,
        set_cache_pressure, set_hugepages, set_thp, set_zswap_enabled, set_zswap_algo,
        set_zramalgo, set_zramsize, set_zramstreams, set_numa_balancing, set_zswap_pool
    )
    from modules.net import set_tcp_metrics, set_mtu_probing, set_rmem, set_wmem

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
    set_zswap_enabled("true")
    set_zswap_algo("lz4")
    set_zramalgo("lz4")
    set_zramsize("1G")
    set_zramstreams("all")
    set_numa_balancing("true")
    set_zswap_pool("20")
    print("✅ Safe profile applied")
    log_change("Safe profile applied")
def read_file_force(path):
    if not os.path.exists(path):
        return "0"
    try:
        subprocess.run(["sudo", "chmod", "644", path], check=True, capture_output=True)
        with open(path, "r") as f:
            val = f.read().strip()
        subprocess.run(["sudo", "chmod", "600", path], check=True, capture_output=True)
        return val if val else "0"
    except:
        return "0"
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
def format_turbo_status(intel_val, amd_val):
    if intel_val in ("0", "1"):
        return "Enabled" if intel_val == "0" else "Disabled"
    elif amd_val in ("0", "1"):
        return "Enabled" if amd_val == "1" else "Disabled"
    else:
        return "N/A"

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
    zram_algo = clean_thp_value(read_file("/sys/block/zram0/comp_algorithm"))
    zram_streams = read_file("/sys/block/zram0/max_comp_streams")
    zswap_enabled = "true" if read_file("/sys/module/zswap/parameters/enabled") == "Y" else "false"
    zswap_algo = read_file("/sys/module/zswap/parameters/compressor")
    zswap_pool = read_file("/sys/module/zswap/parameters/max_pool_percent")
    numa_balancing = "true" if read_file("/proc/sys/kernel/numa_balancing") == "1" else "false"
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
    kernel = platform.release()
    distro = "Linux"
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    distro = line.split("=")[1].strip().replace('"', '')

    desktop = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or "TTY/Unknown"
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
        f"💾 RAM: {mem.available // (1024**2)} MB free / {mem.total // (1024**2)} MB total",
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
        f"🌀 ZRAM Compression Algo: {zram_algo}",
        f"🌀 ZRAM Streams: {zram_streams}",
        f"🌀 ZSWAP Enabled: {zswap_enabled}",
        f"🌀 ZSWAP Algo: {zswap_algo}",
        f"🌀 ZSWAP Pool: {zswap_pool}",
        f"🌀 NUMA Balancing: {numa_balancing}",
        f"🖥️ Distro: {distro}",
        f"🖥️ Kernel: {kernel}",
        f"🖥️ Desktop Env: {desktop}",
    ]
    # merge ascii and fetch
    ascii_lines = ascii_art.splitlines()
    max_len = max(len(line) for line in ascii_lines)
    for i in range(max(len(ascii_lines), len(info_lines))):
        left = ascii_lines[i] if i < len(ascii_lines) else " " * max_len
        right = info_lines[i] if i < len(info_lines) else ""
        print(f"{left:<{max_len}}   {right}")

def read_file(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return "N/A"

def write_file(path, value):
    try:
        with open(path, "w") as f:
            f.write(str(value))
        return True
    except Exception as e:
        print(f"⚠️ Error writing to {path}: {e}")
        return False

def clean_thp_value(raw):
    if "[" in raw and "]" in raw:
        return raw.split("[")[1].split("]")[0].strip()
    return raw.strip()

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
def parse_size(size_str):
    size_str = str(size_str).strip().upper()
    try:
        if size_str.endswith('K'):
            return int(size_str[:-1]) * 1024
        elif size_str.endswith('M'):
            return int(size_str[:-1]) * 1024 * 1024
        elif size_str.endswith('G'):
            return int(size_str[:-1]) * 1024 * 1024 * 1024
        return int(size_str)
    except (ValueError, TypeError):
        return None
       

def parse_size_2(size_str): #<-- lil bro is trying to copy big bro
    return parse_size(size_str)

def find_real_user():

    user = os.environ.get('SUDO_USER') or os.environ.get('USER')
    if user and user != 'root':
        return user
    try:
        users = [d for d in os.listdir('/home') 
                 if os.path.isdir(os.path.join('/home', d)) and d != 'lost+found']
        if users: 
            return users[0]
    except: 
        pass
    return 'root'

def get_log_dir():
    real_user = find_real_user()
    return f"/home/{real_user}/pongtwkr/logs" if real_user != 'root' else "/root/pongtwkr/logs"
log_dir = get_log_dir()
def get_profile_dir():
    real_user = find_real_user()
    return f"/home/{real_user}/pongtwkr/profiles" if real_user != 'root' else "/root/pongtwkr/profiles"

def ensure_log_dir():
    log_dir = get_log_dir()
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    return log_dir

def ensure_profile_dir():
    profile_dir = get_profile_dir()
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir, exist_ok=True)
    return profile_dir

# ==========================================
# NETWORK HELPERS
# ==========================================

def get_wifi_interfaces():
    try:
        result = subprocess.check_output(["iw", "dev"]).decode()
        interfaces = []
        for line in result.splitlines():
            if "Interface" in line:
                interfaces.append(line.split()[1])
        return interfaces
    except:
        return []

def get_physical_interfaces():
    try:
        result = subprocess.check_output(["ip", "link", "show"]).decode()
        interfaces = []
        for line in result.splitlines():
            if "state" in line.lower() and "lo:" not in line:
                interface = line.split(":")[1].strip()
                interfaces.append(interface)
        return interfaces
    except:
        return []

def get_wifi_status_raw():
    interfaces = get_wifi_interfaces()
    if not interfaces: 
        return "N/A"
    try:
        res = subprocess.check_output(["iw", "dev", interfaces[0], "get", "power_save"]).decode()
        return "on" if "on" in res.lower() else "off"
    except: 
        return "N/A"

def get_offload_status_raw(feature):
    interfaces = get_physical_interfaces()
    if not interfaces: 
        return "N/A"
    try:
        res = subprocess.check_output(["ethtool", "-k", interfaces[0]]).decode()
        for line in res.splitlines():
            if feature in line.lower():
                return "on" if "on" in line.lower() and "off" not in line.lower().split(":")[-1] else "off"
    except: 
        return "N/A"

# ==========================================
# VALUE TRANSLATORS (for profiles/kernel)
# ==========================================

def translate_bool_to_kernel(value):
    if str(value).lower() in ["true", "1", "on", "yes"]:
        return "1"
    return "0"

def translate_kernel_to_bool(value):
    return "true" if str(value) in ["1", "Y", "on"] else "false"

def get_available_governors():
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors") as f:
            return f.read().strip().split()
    except:
        return ["performance", "powersave", "schedutil"]

def get_cpu_count():
    try:
        return len([x for x in os.listdir("/sys/devices/system/cpu") if x.startswith("cpu") and x[3:].isdigit()])
    except:
        return 1
def get_all_physical_disks():
    disks = []
    for entry in glob.glob('/sys/block/sd*') + glob.glob('/sys/block/nvme*'):
        disks.append(os.path.basename(entry))
    return disks