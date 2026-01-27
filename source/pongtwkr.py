#!/usr/bin/env python3
import sys
import glob
import psutil  # instalar con: sudo pip3 install psutil

# --- Swappiness ---
def set_swappiness(value):
    try:
        with open("/proc/sys/vm/swappiness", "w") as f:
            f.write(str(value))
        print(f"✅ Swappiness set to {value}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO. (Ex. sudo pongtwkr swappiness 100)")

# --- Governor (todos los cores) ---
def set_governor(value):
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    if not paths:
        print("⚠️ Governor not available for this system. Sorry :(.")
        return
    for path in paths:
        try:
            with open(path, "w") as f:
                f.write(value)
        except PermissionError:
            print(f"⚠️ Error: Please use SUDO {path}")
    print(f"✅ CPU governor set to {value} in {len(paths)} cores")

# --- Dirty Ratio ---
def set_dirty_ratio(value):
    try:
        with open("/proc/sys/vm/dirty_ratio", "w") as f:
            f.write(str(value))
        print(f"✅ vm.dirty_ratio set to {value}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO. (Ex. sudo pongtwkr dirtyratio 20)")

# --- Dirty Background Ratio ---
def set_dirty_background_ratio(value):
    try:
        with open("/proc/sys/vm/dirty_background_ratio", "w") as f:
            f.write(str(value))
        print(f"✅ vm.dirty_background_ratio set to {value}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO. (Ex. sudo pongtwkr dirtybackground 10)")

# --- Cache Pressure ---
def set_cache_pressure(value):
    try:
        with open("/proc/sys/vm/vfs_cache_pressure", "w") as f:
            f.write(str(value))
        print(f"✅ vm.vfs_cache_pressure set to {value}")
    except PermissionError:
        print("⚠️ Error: Please use SUDO. (Ex. sudo pongtwkr cachepressure 50)")

# --- CPU min/max freq (input en GHz, convertido a kHz) ---
def set_cpu_min_freq(value):
    try:
        ghz = float(value)
        khz = int(ghz * 1_000_000)  # convertir GHz -> kHz
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
    print(f"✅ CPU min freq set to {ghz:.2f} GHz ({khz} kHz) in {len(paths)} cores")

def set_cpu_max_freq(value):
    try:
        ghz = float(value)
        khz = int(ghz * 1_000_000)  # convertir GHz -> kHz
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
    print(f"✅ CPU max freq set to {ghz:.2f} GHz ({khz} kHz) in {len(paths)} cores")


# --- Info estilo gamer ---
def show_info():
    # Recoger datos
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
    governor = read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    dirty_ratio = read_file("/proc/sys/vm/dirty_ratio")
    dirty_background = read_file("/proc/sys/vm/dirty_background_ratio")
    cache_pressure = read_file("/proc/sys/vm/vfs_cache_pressure")
    cpu_min = read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq")
    cpu_max = read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq")
    cpu_min_ghz = f"{int(cpu_min) / 1_000_000:.2f} GHz" if cpu_min.isdigit() else "N/A"
    cpu_max_ghz = f"{int(cpu_max) / 1_000_000:.2f} GHz" if cpu_max.isdigit() else "N/A"

    # Temperaturas
    temps = []
    for path in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
        try:
            with open(path) as f:
                temp = int(f.read().strip()) / 1000.0
                temps.append(f"{path.split('/')[-2]}: {temp:.1f}°C")
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

    # Info lines
    info_lines = [
        f"💾 RAM: {mem.available // (1024**2)} MB libres / {mem.total // (1024**2)} MB totales",
        f"⚙️ CPU usage per core: {cpu_usage}",
        f"🧵 Threads: {threads} | Physical Cores: {cores}",
        f"🔧 Swappiness: {swappiness}",
        f"⚡ Governor: {governor}",
        f"💾 Swap: {swap.used // (1024**2)} MB used / {swap.total // (1024**2)} MB total",
        f"📂 Buffers: {mem.buffers // (1024**2)} MB | Cached: {mem.cached // (1024**2)} MB",
        f"📝 vm.dirty_ratio: {dirty_ratio}",
        f"📝 vm.dirty_background_ratio: {dirty_background}",
        f"📝 vm.vfs_cache_pressure: {cache_pressure}",
        f"⚡ CPU min freq: {cpu_min_ghz} gHz",
        f"⚡ CPU max freq: {cpu_max_ghz} gHz",
    ] + [f"🌡️ {t}" for t in temps]

    # Combinar ASCII izquierda + info derecha
    ascii_lines = ascii_art.splitlines()
    max_len = max(len(line) for line in ascii_lines)
    for i in range(max(len(ascii_lines), len(info_lines))):
        left = ascii_lines[i] if i < len(ascii_lines) else " " * max_len
        right = info_lines[i] if i < len(info_lines) else ""
        print(f"{left:<{max_len}}   {right}")

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pongtwkr <option> [value]")
        sys.exit(1)

    option = sys.argv[1]


    if option == "swappiness" and len(sys.argv) == 3:
        set_swappiness(sys.argv[2])
    elif option == "governor" and len(sys.argv) == 3:
        set_governor(sys.argv[2])
    elif option == "dirtyratio" and len(sys.argv) == 3:
        set_dirty_ratio(sys.argv[2])
    elif option == "dirtybackground" and len(sys.argv) == 3:
        set_dirty_background_ratio(sys.argv[2])
    elif option == "cachepressure" and len(sys.argv) == 3:
        set_cache_pressure(sys.argv[2])
    elif option == "cpumin" and len(sys.argv) == 3:
        set_cpu_min_freq(sys.argv[2])
    elif option == "cpumax" and len(sys.argv) == 3:
        set_cpu_max_freq(sys.argv[2])
    elif option == "info":
        show_info()
    else:
        print("⚠️ Unknown option or bad usage. Please refer to the documentation for further help.")

