# PongTWKR
The objective of PongTWKR is to be an easy-to-use, handy tool for tweaking CPU, RAM, and other PC components like Swappiness, governor, etc. easily, without having to confront the terminal or shady directories. Please note that this program is targeted for those that can't/don't want to mess with commands or files on their Linux Distro, but want to get overall better performance.

# How to use?
Well, as for January 27, 2026, PongTWKR is still on early development. v0.2. It is a simple program that makes it easier to make changes/tweaks to CPU/RAM configurations, such as governor, dirty_ratio, etc. Just install (Move pongtwkr.py to /usr/local/bin, /usr/bin or any other PATH directorie) and use it by the terminal!

## v0.2 commands:

- `sudo pongtwkr swappiness <value>`
  - Adjusts vm.swappiness
- `sudo pongtwkr governor <value>` (Generally performance or powersave)
  - Adjusts the governor preset for your CPU.
- `sudo pongtwkr cpumin <value_in_ghz>`
  - Limits the minimum frequency of your CPU in GhZ.
- `sudo pongtwkr cpumax <value_in_ghz>`
  - Limits the maximum frequency of your CPU in GhZ.
- `sudo pongtwkr dirtyratio <value>`
  - Adjusts vm.dirty_ratio
- `sudo pongtwkr dirtybackground <value>`
  - Adjusts vm.dirty_background_ratio
- `sudo pongtwkr cachepressure <value>`
  - Adjusts vm.vfs_cache_pressure
- sudo pongtwkr info`
  - Shows a quick-info panel
 
## v0.2 Changelog
- Added dirty ratio command
- Added dirty background ratio command
- Added vfs cache pressure command
- Added maximum and minimum CPU frequency command
- Added more info + a cute design to 'sudo pongtwkr info'

# Our objective & philosophy
PongTWKR aims to unify Linux performance tweaks that are usually scattered across different packages.  
Our long-term goal is to be a *modular* and *open-source* toolkit, avoiding the need to install huge “gaming packs” with hundreds of tools you’ll never use.  
Instead, just install PongTWKR and enjoy a growing set of 150+ tweaks (future roadmap), or keep it minimal and use only what you need.


# About me
Welp, I'm just a "dev" that enjoys Linux and, when I started with it, had problems when making tweaks like this. I'll love to see how far I can get with PongTWKR.

