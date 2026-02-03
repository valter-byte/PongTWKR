# PongTWKR

PongTWKR is an easy-to-use, modular toolkit for tweaking CPU, RAM, GPU, and other Linux system parameters (like swappiness, governors, dirty ratios, ZRAM, etc.) without having to dive into obscure directories or memorize dozens of commands.

The project is designed for users who want better performance and control but prefer a safe, gamer‑friendly CLI instead of manual sysctl edits or scattered scripts.
## ✨ Features (current v0.8)

  - CPU tweaks: governors, frequency locks, dirty ratios.

  - RAM tweaks: ZRAM algorithms, streams, limits, disksize.

  - VM tweaks: swappiness, cache pressure.

  - Disk tweaks: I/O Scheduler, NCQ, Runtime Power Management
  
  - Modular CLI commands with instant feedback and reset functions.

  - Logging of every change for transparency.

*(Check `commands.md` for further info)*

# 🚀 Roadmap
# (GPU TWEAKS WERE DELAYED DUE TO LACK OF TESTERS.)

## v0.8 "Diskette support"
  - I/O Scheduler
  - Max Sectors KB
  - NCQ
  - Runtime Power Management

# 📖 Philosophy

PongTWKR is built on five pillars:

### Transparency → every tweak is logged, every error is shown.

### Safety → instant rollback/reset, no hidden changes.

### All-In-One → No more bloated "gaming packs" with hundreds of tools you'll never use. Install the base. Browse modules you like. Install. Enjoy

### Freedom → Do whatever you want. Your PC. Your rules. Want to explode it? Explode it.

### Fun and ease → We are a gaming focused program. You won't have to browse a 1023 page doc to change swappiness. `sudo pongtwkr swappiness` and done.

# 🛠 Installation

For now, clone the repo and move pongtwkr.py to your PATH (/usr/local/bin, /usr/bin, etc.).
From v0.8 onwards, you can use the official installer:
bash

`curl -s https://raw.githubusercontent.com/valter-byte/PongTWKR/main/install.sh | sudo bash`

Run it with:
bash

sudo pongtwkr

📜 Commands

The commands in PongTWKR CLI follow a basic scheme:

`sudo pongtwkr <command> <value> <parameter>`

No satanic rituals. No donating your soul to the Kernel:

`sudo pongtwkr governor performance`
`sudo pongtwkr info`
`sudo pongtwkr offload gro false`
`sudo pongtwkr dirtyratio 100 override`

See? As easy as that.
(See commands.md for full list.)

# 🗂 Changelog

    v0.7 “Rammed” → advanced RAM tweaks (zramalgo, zramstreams, zramlimit, zramsize).

    v0.6 "WiFi-ed" → WiFi tweaks. TCP Metrics, MTU Probing, Offloading, etc..

    v0.5 "Profiled" → Profiles. Hotfix.

(See changelog.md for detailed history.)

# 👤 About me

I’m Valter, a Linux enthusiast who struggled with performance tweaks when starting out. PongTWKR is my attempt to make those tweaks accessible, safe, and fun.

I document every step in blog.md — including setbacks, breakthroughs, and crazy ideas — because I believe in building openly and iteratively.
