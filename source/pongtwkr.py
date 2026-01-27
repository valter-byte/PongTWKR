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
        print("⚠️ Error: Please uso SUDO. (Ex. sudo pongtwkr swappiness 100")

# --- Governor (todos los cores) ---
def set_governor(value):
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    if not paths:
        print("⚠️ Governor not avaiable for this system. Sorry :(.")
        return
    for path in paths:
        try:
            with open(path, "w") as f:
                f.write(value)
        except PermissionError:
            print(f"⚠️ Error: Please use SUDO {path}")
    print(f"✅ CPU governor set to {value} in {len(paths)} cores")

# --- Info estilo gamer ---
def show_info():
    # RAM
    mem = psutil.virtual_memory()
    print(f"💾 RAM: {mem.available // (1024**2)} MB libres / {mem.total // (1024**2)} MB totales")

    # CPU usage y cores
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    print(f"⚙️ CPU usage per core: {cpu_usage}")
    print(f"🧵 Threads: {psutil.cpu_count(logical=True)} | Physical Cores: {psutil.cpu_count(logical=False)}")

    # Swappiness
    with open("/proc/sys/vm/swappiness") as f:
        print(f"🔧 Swappiness: {f.read().strip()}")

    # Governor (primer core como referencia)
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor") as f:
            print(f"⚡ Governor: {f.read().strip()}")
    except FileNotFoundError:
        print("⚠️ Governor info not avaiable.")

    # Temperatura (si el sistema expone sensores)
    thermal_paths = glob.glob("/sys/class/thermal/thermal_zone*/temp")
    if thermal_paths:
        for path in thermal_paths:
            try:
                with open(path) as f:
                    temp = int(f.read().strip()) / 1000.0
                    print(f"🌡️ Temp sensor {path.split('/')[-2]}: {temp:.1f}°C")
            except:
                pass
    else:
        print("🌡️ Temperature not avaiable...")

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
    elif option == "info":
        show_info()
    else:
        print("⚠️ Unknown option or bad usage. Please refer to the documentation for further help.")

