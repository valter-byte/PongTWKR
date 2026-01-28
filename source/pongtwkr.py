#!/usr/bin/env python3
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
# Log making
real_user = os.environ.get('SUDO_USER') or os.environ.get('USER')
if real_user:
    log_dir = f"/home/{real_user}/.pongtwkr"
else:
    log_dir = os.path.expanduser("~/.pongtwkr")
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "logs.txt")

# Log changing
def log_change(action):
    try:
        with open(log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {action}\n")
    except:
        pass
# infos
def show_param_info(param):
    print(infos.get(param, "Ups, theres no info for this..."))
    # Añadir aviso de seguridad similar al de swappiness para otros tweaks
    if param in ("dirtyratio", "dirtybackground", "cachepressure"):
        print("⚠️ Security: values out of range may cause instablity and kernel errors.")
    if param in ("cpumin", "cpumax"):
        print("⚠️ Beware: The CPU automaticaly tops itself. No matter if you do override, the values will be topped to the physical limits of your CPY")
    if param == "governor":
        print("⚠️ Beware: Some governors may not be available for all systems.")

# Value limiter.
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

# --- Info de parámetros ---
infos = {
    "swappiness": "Swappiness is how sensible is the system to switching to SWAP instead of RAM. Safe range: 0-100.",
    "dirtyratio": "Dirty Ratio defines the maximum percentage of dirty memory before writing onto the disk. Safe range: 20-70%",
    "dirtybackground": "Same as dirty ratio, but writing onto the background instead of the disk. IT SHOULD BE ALWAYS LOWER THAN DIRTY RATIO. Safe range: 5-50",
    "cachepressure": "Controls the pressure over the cache (duh), safe values: 0-100",
    "governor": "Governors are presets that the CPU comes with. If you want performance, use sudo pongtwkr governor performance, if you want power saving, uso powersave.",
    "cpumin": "Defines the minimum frequency for the CPU",
    "cpumax": "Defines the maximum frequency for the CPU.",
    "info": "Shows a quick set of info and tweaks made.",
    "ping": "Well... justs ping google to see your ms.. what did you expect???"
}



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

# --- Reset defaults ---
defaults = {}
def save_defaults():
    for param, path in {
        "swappiness": "/proc/sys/vm/swappiness",
        "dirtyratio": "/proc/sys/vm/dirty_ratio",
        "dirtybackground": "/proc/sys/vm/dirty_background_ratio",
        "cachepressure": "/proc/sys/vm/vfs_cache_pressure"
    }.items():
        try:
            with open(path) as f:
                defaults[param] = f.read().strip()
        except:
            defaults[param] = None

def reset_defaults():
    for param, path in {
        "swappiness": "/proc/sys/vm/swappiness",
        "dirtyratio": "/proc/sys/vm/dirty_ratio",
        "dirtybackground": "/proc/sys/vm/dirty_background_ratio",
        "cachepressure": "/proc/sys/vm/vfs_cache_pressure"
    }.items():
        if defaults.get(param) is not None:
            try:
                with open(path, "w") as f:
                    f.write(defaults[param])
                print(f"✅ {param} reset to {defaults[param]}")
                log_change(f"{param} reset to {defaults[param]}")
            except Exception as e:
                print(f"⚠️ Could not reset {param}: {e}")

# --- Safe profile ---
def safe_profile():
    set_swappiness(60)
    set_governor("powersave")
    set_dirty_ratio(20)
    set_dirty_background_ratio(10)
    set_cache_pressure(50)
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
# easter egg
def show_info_war():
    print(f"""
    ☢️ Designated Warheads: ALPHA & BETA
    📌 Designated objectives: Marked 35 cities in the USA.
    ✝️ Estimated casualties: +700 million
    ⏳ Time for impact: T-15 seconds for launch."
    🖥️ Executing command: sudo rm -rf / --no-preserve-root)
    Thank you, AGENT FINN MC MISSILE. Proceding with launch...""")
# --- Info estilo gamer ---
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

    # Convertir frecuencias a GHz si son números
    def khz_to_ghz(val):
        try:
            return f"{int(val) / 1_000_000:.2f} GHz"
        except:
            return "N/A"

    cpu_min_ghz = khz_to_ghz(cpu_min)
    cpu_max_ghz = khz_to_ghz(cpu_max)

    # Avisos fuera de rango (seguridad)
    if swappiness.isdigit() and int(swappiness) > 100:
        print("⚠️ Swappiness out of range. It may cause performance issues.")
    if dirty_ratio.isdigit() and int(dirty_ratio) > 20:
        print("⚠️ Dirty Ratio out of range. It may cause performance issues.")
    if dirty_background.isdigit() and int(dirty_background) > 50:
        print("⚠️ Dirty Background Ratio out of range. It may cause performance issues.")
    if cache_pressure.isdigit() and int(cache_pressure) > 100:
        print("⚠️ vfs_cache_pressure out of range. It may cause performance issues.")
    # Aviso sobre frecuencias absurdas (en kHz)
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

    # --- ASCII Pong + Logo ---
    ascii_art = """
+------------------------------------------------------------+
|                                                            |
|                          o                                 |
|                                                            |
|   |                                                        |
|                                                            |
|                                                        |   |
+------------------------------------------------------------+

██████╗░░█████╗░███╗░░██╗░██████╗░████████╗░██╗░░░░░░░██╗██╗░░██╗██████╗░
██╔══██╗██╔══██╗████╗░██║██╔════╝░╚══██╔══╝░██║░░██╗░░██║██║░██╔╝██╔══██╗
██████╔╝██║░░██║██╔██╗██║██║░░██╗░░░░██║░░░░╚██╗████╗██╔╝█████═╝░██████╔╝
██╔═══╝░██║░░██║██║╚████║██║░░╚██╗░░░██║░░░░░████╔═████║░██╔═██╗░██╔══██╗
██║░░░░░╚█████╔╝██║░╚███║╚██████╔╝░░░██║░░░░░╚██╔╝░╚██╔╝░██║░╚██╗██║░░██║
╚═╝░░░░░░╚════╝░╚═╝░░╚══╝░╚═════╝░░░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝
"""

    # Info lines (incluye dirty_background y cache_pressure y frecuencias)
    info_lines = [
        f"💾 RAM: {mem.available // (1024**2)} MB avaiable / {mem.total // (1024**2)} MB total",
        f"⚙️ CPU usage per core: {cpu_usage}",
        f"🧵 Threads: {threads} | Physical Cores: {cores}",
        f"🔧 Swappiness: {swappiness}",
        f"📝 vm.dirty_ratio: {dirty_ratio}",
        f"📝 vm.dirty_background_ratio: {dirty_background}",
        f"📝 vm.vfs_cache_pressure: {cache_pressure}",
        f"⚡ Governor: {governor}",
        f"⚡ CPU min freq: {cpu_min_ghz}",
        f"⚡ CPU max freq: {cpu_max_ghz}",
        f"💾 Swap: {swap.used // (1024**2)} MB used / {swap.total // (1024**2)} MB total",
        f"📂 Buffers: {mem.buffers // (1024**2)} MB | Cached: {mem.cached // (1024**2)} MB",
    ]

    # Combinar ASCII izquierda + info derecha
    ascii_lines = ascii_art.splitlines()
    max_len = max(len(line) for line in ascii_lines)
    for i in range(max(len(ascii_lines), len(info_lines))):
        left = ascii_lines[i] if i < len(ascii_lines) else " " * max_len
        right = info_lines[i] if i < len(info_lines) else ""
        print(f"{left:<{max_len}}   {right}")


# --- Main ---
if __name__ == "__main__":
    save_defaults()

    if len(sys.argv) < 2:
        print("Usage: pongtwkr <option> [value]")
        sys.exit(1)

    option = sys.argv[1]

    # Info de parámetros (ej: pongtwkr swappiness info)
    if len(sys.argv) == 3 and sys.argv[2] == "info":
        show_param_info(option)
        sys.exit(0)

    # Override
    option = sys.argv[1]

    override = "override" in sys.argv

    if option == "swappiness":
        if override:
            set_swappiness(sys.argv[2])
        else:
            val = limit_value("Swappiness", sys.argv[2], 0, 100)
            if val is not None:
                set_swappiness(val)

    elif option == "governor":
        set_governor(sys.argv[2])

    elif option == "dirtyratio":
        if override:
            set_dirty_ratio(sys.argv[2])
        else:
            val = limit_value("Dirty Ratio", sys.argv[2], 0, 20)
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

    elif option == "cpumin":
        # rango seguro sugerido: 0.5 - 6.0 GHz
        if override:
            set_cpu_min_freq(sys.argv[2])
            print(f"The value tops with your CPU: no matter if you use override, it will top to the physical limit of your CPU.")
        else:
            val = limit_float("CPU min freq (GHz)", sys.argv[2], 0.5, 6.0)
            if val is not None:
                set_cpu_min_freq(val)

    elif option == "cpumax":
        # rango seguro sugerido: 0.5 - 6.0 GHz
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

    elif option == "reset":
        reset_defaults()

    elif option == "safe":
        safe_profile()

    elif option == "ping":
        ping_test()

    else:
        print("⚠️ Unknown option or bad usage. Please refer to the documentation for further help.")
