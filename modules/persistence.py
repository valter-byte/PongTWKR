#!/usr/bin/env python3
"""
PongTWKR v0.8 - Persistence Module
Handles systemd service creation for persistent settings across reboots
"""

import os
import sys
import subprocess
from .profiles import save_profile
from .logger import log_change

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
        print(f"ℹ️  Settings will be restored on every boot")
        log_change("Persistence service enabled successfully.")
    except Exception as e:
        print(f"⚠️ Error enabling persistence: {e}")

