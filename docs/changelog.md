# CHANGELOG 
## Here will go the changes added to the tweaker.
# v0.7 "Rammed"
> Rest in piss mem_limit

### New features
- ***Added ZSWAP I/O, ZSWAP Pool % tweaking, ZSWAP algorithms tweaking, ZRAM disk size tweaking, ZRAM algorithms tweaking, ZRAM streams tweaking, and NUMA Balancing toggling***
- ***Added "stop-and-go" tweaks to the ZRAM commands*** so when you run it you dont have to mannually turn it off.
- ***General tweaks and fixes to the code.***

# v0.6 "Wifi-ed"
> This update came surprisingly before I expected.

### New Features
- ***Addded TCP Metrics, MTU Probing, WiFi Powersave, Offloading toggle, RMEM and WMEM Buffer support.***
- ***Revamped the ASCII on `sudo pongtwkr info`***
- ***Added network data to `sudo pongtwkr info`***
- ***General tweaks and fixes to the code***

  
# v0.5 "Profiled"
> The name is a lie. It's more a hotfix than a "Profiles" update.

### New Features
- ***Added profile management*** saving .json on the .pongtwkr directorie, with `sudo pongtwkr save <name>` & `sudo pongtwkr load <name>`
- ***Added tweaks persistency*** now tweaks persist after reboots, with `sudo pongtwkr persist`

### Fixes
> The first bugfixes... were needed.
- ***Fixed using a command without value making the script crash*** *(`sudo pongtwkr swappiness` or `sudo pongtwkr dirtyratio`, for example)*
- ***Fixed `sudo pongtwkr reset*** working partially
- ***General tweaks and fixes to the code. (yk)***
# v0.4 "More Tweaks"
> I mean, who doesnt love being able to change your HugePages with just a command line?

### New features
Added CPU Turbo/Boost, THP, HugePages, and SMT support.

- ***Added CPU Turbo/Boost enable/disable*** the program detects your path (Intel/AMD) and applies the changes.
- ***Added THP selection*** now you can select `enable` , `disable` or `madvise`.
- ***Added HugePages quantity selector*** just choose how many HugePages you want.
- ***Added SMT (Multithreading) toggler***  for both Intel/AMD.

### Tweaks
- ***Addition of the limiters/security/disclaimers*** to the new commands.
- ***Integration to the safe/reset command*** to the new tweaks.
- ***Extra info on `sudo pongtwkr info`*** more specifically, Fan speed, uptime, processes, hugepages, THP, Turbo I/O and SMT.
- ***General tweaks to the code.***

# v0.3 "Foolproof"
> "Safety first. I guess..."

### Safety Module
The whole purpose of this update was setting safe bounds and information. Nothing else.

- ***Added value limiter*** Now you can't  make `sudo pongtwkr swappiness 10000000000000`. It will be automatically capped to a safe maximum. This works for everything.
- ***Added `info` and `override` parameters.*** Info... well, shows you info of the requested command and override overrides the cap.
   > Example: sudo pongtwkr swappiness 150 override | sudo pongtwkr swappiness info
- ***Added a bit more info to `sudo pongtwkr info`*** alongside a set of warnings if some values are out of the cap.
- ***Added a log.txt to see what changes you made.***
   > The log is located in **/home/your_user/.pongtwkr/log.txt**
   > To see hidden directories/files (The ones that start with "."), use Super + H
- ***Added `sudo pongtwkr reset` and `sudo pongtwkr safe`***
   > Reset resets all the values to the ones that were before starting the program.
   > Safe resets all the values to regular ones that will work on any PC.
- ***General tweaks and fixes. yeah, you know...***
- ***Added an ultra special hidden easter egg...***

# v0.2 "Just some cache..."
> Added a bit more tweaks to the now not-so-useless tweaker.
### Tweaks added
Just added a bit more tweaks to the program. Playing around...
- ***Added `sudo pongtwkr dirtyratio`, `sudo pongtwkr dirtybackground` and  `sudo pongtwkr cachepressure`***
- ***Added ASCII to `sudo pongtwkr info` to make it COOLER.***

# v0.1 "Useless Tweaker"
> What did you expect from a v0.1????

### First version with few commands.
- ***Added `sudo pongtwkr swappiness`, `sudo pongtwkr governor` and `sudo pongtwkr info`***
