import os

from modules.utils import limit_value, parse_size

def set_runtime_pm(device_name, enable_performance):
    path = f"/sys/block/{device_name}/device/power/control"
    
    if not os.path.exists(path):
        print(f" ⚠️ [ERROR] Power control not found for {device_name}. Are you sure this device exists?")
        return False
    if str(enable_performance).lower() in ["on", "true", "yes", "1"]:
        mode = "on"
    elif str(enable_performance).lower() in ["off", "false", "no", "0"]:
        mode = "auto"
    else:
        print(" ⚠️ [ERROR] Invalid value for enable_performance. Use True/False or On/Off.")
        return False
    try:
        with open(path, "w") as f:
            f.write(mode)
        print(f"✅ {device_name} runtime power management set to {mode}.")
        return True
    except PermissionError:
        print("Please run with sudo...")
        return False
    except Exception as e:
        print(f" ⚠️ [ERROR] Could not set power mode for {device_name}: {e}")
        return False

def set_io_scheduler(device_name, scheduler_name):
    path = f"/sys/block/{device_name}/queue/scheduler"
    if not os.path.exists(path):
        print(f"⚠️ [ERROR] Path not found for {device_name}. Are you using a virtual drive..?")
        return False

    try:
        with open(path, "w") as f:
            f.write(scheduler_name)  
            
        print(f"✅ {device_name} scheduler set to: {scheduler_name.upper()}.")
        return True
    except OSError:
        print(f"⚠️ {scheduler_name} is not available for this drive.")
        return False
    except PermissionError:
        print("Please run with sudo...")
        return False
    except Exception as e:
        print(f"⚠️ [ERROR] Could not set scheduler for {device_name}: {e}")
        return False
def set_ncq_depth(device_name, value):
    path = f"/sys/block/{device_name}/queue/nr_requests"
    if value is None: return False
    try:
        with open(path, "w") as f:
            f.write(str(value))
        print(f"✅ {device_name} NCQ Depth set to: {value}.")
        return True
    except Exception as e:
        print(f"⚠️ Error when applying NCQ Depth: {e}")
        return False
def set_max_sectors(device_name, size_input):
    path = f"/sys/block/{device_name}/queue/max_sectors_kb"
    kb_value = parse_size(size_input) // 1024
    if kb_value is None: return False
    elif kb_value <= 0:
        print(f"⚠️ [ERROR] Size must be a positive number. E.g., '512K', '4M', '1G'.")
        return False
    try:
        with open(path, "w") as f:
            f.write(str(kb_value))
        print(f"✅ {device_name} Max Sectors set to: {kb_value} KB.")
        return True
    except Exception as e:
        print(f"⚠️ [ERROR] Could not set Max Sectors for {device_name}: {e}")
        return False