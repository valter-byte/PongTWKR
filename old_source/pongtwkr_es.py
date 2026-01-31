#!/usr/bin/env python3
import sys
import glob
import re
try:
    import psutil
except ImportError:
    print("❌ Error: Para que PongTWKR funcione, debe tener instalado 'psutil'. Instálelo con 'sudo pip install psutil' o mediante su gestor de paquetes.")
    sys.exit(1)
import os
import datetime
import subprocess

# Configuración de Registros (Logs)
real_user = os.environ.get('SUDO_USER') or os.environ.get('USER')
if real_user:
    log_dir = f"/home/{real_user}/.pongtwkr"
else:
    log_dir = os.path.expanduser("~/.pongtwkr")

if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "logs.txt")

def log_change(action):
    try:
        with open(log_file, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {action}\n")
    except:
        pass

# Información de Parámetros
def show_param_info(param):
    print(infos.get(param, "Ups, no hay información disponible para este comando..."))
    if param in ("dirtyratio", "dirtybackground", "cachepressure"):
        print("⚠️ Seguridad: Valores fuera de rango pueden causar inestabilidad y errores de kernel.")
    if param in ("cpumin", "cpumax"):
        print("⚠️ Advertencia: La CPU se limita automáticamente. Aunque use 'override', los valores se ajustarán a los límites físicos de su procesador.")
    if param == "governor":
        print("⚠️ Advertencia: Algunos gobernadores pueden no estar disponibles en todos los sistemas.")

# Limitadores de Valores
def limit_value(name, value, min_val, max_val):
    try:
        val = int(value)
    except ValueError:
        print(f"⚠️ Error: {name} debe ser un número entero.")
        return None
    if val < min_val or val > max_val:
        print(f"⚠️ {name} fuera de rango seguro ({val}). Reajustado a {max_val}. Use 'override' al final del comando para ignorar este módulo de seguridad.")
        return max_val
    return val

def limit_float(name, value, min_val, max_val):
    try:
        val = float(value)
    except ValueError:
        print(f"⚠️ Error: {name} debe ser un número decimal (float).")
        return None
    if val < min_val or val > max_val:
        print(f"⚠️ {name} fuera de rango seguro ({val}). Reajustado a {max_val}. Use 'override' al final del comando para ignorar este módulo de seguridad.")
        return max_val
    return val

# --- Diccionario de Información ---
infos = {
    "swappiness": "Define la tendencia del kernel a mover procesos de la RAM al SWAP. Rango seguro: 0-100.",
    "dirtyratio": "Porcentaje máximo de memoria sucia antes de que el sistema comience a escribir en el disco. Rango: 5-50%.",
    "dirtybackground": "Similar a dirty_ratio, pero para escritura en segundo plano. Rango seguro: 5-20%.",
    "cachepressure": "Controla la tendencia del kernel a recuperar memoria utilizada para caché de directorios e inodos. Rango: 0-1000.",
    "governor": "Ajustes preestablecidos de la CPU. 'performance' para máximo rendimiento, 'powersave' para ahorro de energía.",
    "cpumin": "Define la frecuencia mínima de operación de la CPU (en GHz).",
    "cpumax": "Define la frecuencia máxima de operación de la CPU (en GHz).",
    "info": "Muestra el panel de estado actual y los ajustes realizados.",
    "ping": "Realiza una prueba de latencia hacia los servidores de Google."
}

# --- Funciones de Ajuste (Traducción de mensajes de salida) ---
def set_swappiness(value):
    try:
        ival = int(value)
        with open("/proc/sys/vm/swappiness", "w") as f:
            f.write(str(ival))
        print(f"✅ Swappiness establecido en {ival}")
        log_change(f"Swappiness establecido en {ival}")
    except PermissionError:
        print("⚠️ Error: Requiere privilegios de ROOT (SUDO).")
    except OSError as e:
        print(f"⚠️ Error al aplicar Swappiness: {e}. El kernel rechazó el valor.")

def set_governor(value):
    paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")
    if not paths:
        print("⚠️ El control de gobernador no está disponible en este sistema.")
        return
    for path in paths:
        try:
            with open(path, "w") as f:
                f.write(value)
        except Exception as e:
            print(f"⚠️ Error al escribir en {path}: {e}")
    print(f"✅ Gobernador de CPU establecido en '{value}' para {len(paths)} núcleos.")
    log_change(f"Gobernador establecido en {value}")

def set_dirty_ratio(value):
    try:
        ival = int(value)
        with open("/proc/sys/vm/dirty_ratio", "w") as f:
            f.write(str(ival))
        print(f"✅ vm.dirty_ratio establecido en {ival}")
        log_change(f"Dirty Ratio establecido en {ival}")
    except Exception as e:
        print(f"⚠️ Error al aplicar dirty_ratio: {e}")

def set_dirty_background_ratio(value):
    try:
        ival = int(value)
        with open("/proc/sys/vm/dirty_background_ratio", "w") as f:
            f.write(str(ival))
        print(f"✅ vm.dirty_background_ratio establecido en {ival}")
        log_change(f"Dirty Background Ratio establecido en {ival}")
    except Exception as e:
        print(f"⚠️ Error al aplicar dirty_background_ratio: {e}")

def set_cache_pressure(value):
    try:
        ival = int(value)
        with open("/proc/sys/vm/vfs_cache_pressure", "w") as f:
            f.write(str(ival))
        print(f"✅ vm.vfs_cache_pressure establecido en {ival}")
        log_change(f"Cache Pressure establecido en {ival}")
    except Exception as e:
        print(f"⚠️ Error al aplicar vfs_cache_pressure: {e}")

def set_cpu_min_freq(value):
    try:
        ghz = float(value)
        khz = int(ghz * 1_000_000)
        paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq")
        for path in paths:
            with open(path, "w") as f:
                f.write(str(khz))
        print(f"✅ Frecuencia mínima de CPU establecida en {ghz:.2f} GHz.")
        log_change(f"Frecuencia mínima establecida en {ghz:.2f} GHz")
    except Exception as e:
        print(f"⚠️ Error al aplicar frecuencia mínima: {e}")

def set_cpu_max_freq(value):
    try:
        ghz = float(value)
        khz = int(ghz * 1_000_000)
        paths = glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq")
        for path in paths:
            with open(path, "w") as f:
                f.write(str(khz))
        print(f"✅ Frecuencia máxima de CPU establecida en {ghz:.2f} GHz.")
        log_change(f"Frecuencia máxima establecida en {ghz:.2f} GHz")
    except Exception as e:
        print(f"⚠️ Error al aplicar frecuencia máxima: {e}")

# --- Perfiles y Reset ---
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
    for param, path in defaults.items():
        if path and defaults[param]:
            try:
                # Mapeo de nombre a ruta real para escribir
                sys_path = {
                    "swappiness": "/proc/sys/vm/swappiness",
                    "dirtyratio": "/proc/sys/vm/dirty_ratio",
                    "dirtybackground": "/proc/sys/vm/dirty_background_ratio",
                    "cachepressure": "/proc/sys/vm/vfs_cache_pressure"
                }[param]
                with open(sys_path, "w") as f:
                    f.write(defaults[param])
                print(f"✅ {param} restaurado a su valor inicial: {defaults[param]}")
            except:
                pass

def safe_profile():
    set_swappiness(60)
    set_governor("powersave")
    set_dirty_ratio(20)
    set_dirty_background_ratio(10)
    set_cache_pressure(100)
    print("✅ Perfil de seguridad aplicado correctamente.")

def ping_test(host="8.8.8.8"):
    try:
        out = subprocess.check_output(["ping", "-c", "1", "-W", "2", host], universal_newlines=True)
        match = re.search(r"time=([\d.]+)|tiempo=([\d.]+)", out)
        if match:
            ms = match.group(1) or match.group(2)
            print(f"🏓 Pong! Latencia: {ms} ms")
        else:
            print(f"⚠️ No se pudo procesar la salida del ping.")
    except:
        print(f"⚠️ El servidor {host} no responde.")

# --- Easter Egg Nuclear ---
def show_info_war():
    print(f"""
    🚀 [ADVERTENCIA] MODO INFO OVERRIDE ACTIVADO.
    ☢️ Ojivas nucleares designadas: ALPHA & BETA
    📌 Objetivos: 35 ciudades identificadas en territorio extranjero.
    ✝️ Bajas estimadas: +700 millones de personas.
    ⏳ Tiempo para impacto: T-15 segundos para el lanzamiento.
    🖥️ Ejecutando comando: sudo rm -rf / --no-preserve-root
    
    Gracias, AGENTE FINN MC MISSILE. Procediendo con la secuencia...
    """)

# --- Panel de Información ---
def show_info():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    
    def read_file(path):
        try:
            with open(path) as f: return f.read().strip()
        except: return "N/A"

    sw = read_file("/proc/sys/vm/swappiness")
    dr = read_file("/proc/sys/vm/dirty_ratio")
    db = read_file("/proc/sys/vm/dirty_background_ratio")
    cp = read_file("/proc/sys/vm/vfs_cache_pressure")
    gv = read_file("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    
    # ... (ASCII Art se mantiene igual por estética) ...
    print("--- ESTADO DEL SISTEMA ---")
    print(f"💾 RAM: {mem.available // (1024**2)} MB libres / {mem.total // (1024**2)} MB totales")
    print(f"⚙️ Uso de CPU por núcleo: {cpu_usage}")
    print(f"🔧 Swappiness: {sw} | Dirty Ratio: {dr}% | Background: {db}%")
    print(f"⚡ Gobernador: {gv} | Presión de Cache: {cp}")
    print(f"💾 Swap: {swap.used // (1024**2)} MB en uso / {swap.total // (1024**2)} MB totales")

# --- Main ---
if __name__ == "__main__":
    save_defaults()
    if len(sys.argv) < 2:
        print("Uso: sudo pongtwkr <opción> [valor]")
        sys.exit(1)

    option = sys.argv[1]
    override = "override" in sys.argv

    if len(sys.argv) == 3 and sys.argv[2] == "info":
        show_param_info(option)
        sys.exit(0)

    if option == "swappiness":
        if override: set_swappiness(sys.argv[2])
        else:
            val = limit_value("Swappiness", sys.argv[2], 0, 100)
            if val is not None: set_swappiness(val)

    elif option == "governor":
        set_governor(sys.argv[2])

    elif option == "dirtyratio":
        if override: set_dirty_ratio(sys.argv[2])
        else:
            val = limit_value("Dirty Ratio", sys.argv[2], 0, 50)
            if val is not None: set_dirty_ratio(val)

    elif option == "dirtybackground":
        if override: set_dirty_background_ratio(sys.argv[2])
        else:
            val = limit_value("Dirty Background Ratio", sys.argv[2], 0, 20)
            if val is not None: set_dirty_background_ratio(val)

    elif option == "info":
        if override: show_info_war()
        else: show_info()

    elif option == "reset":
        reset_defaults()

    elif option == "safe":
        safe_profile()

    elif option == "ping":
        ping_test()

    else:
        print("⚠️ Opción desconocida o uso incorrecto. Consulte la documentación.")
