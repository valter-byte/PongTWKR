# Command & Parameter list.
# NEW MEGA EPIC USEFULL COMMAND:
- `sudo pongtwkr persist`
**Makes the current settings persist after reboot.**
## Tweaking
- `sudo pongtwkr swappiness <value>`
**Changes the swappiness of the system to the designated value.**
- `sudo pongtwkr governor <value>`
**Sets the CPU governor to the selected preset**
- `sudo pongtwkr dirtyratio <value>`
**Sets the dirty memory % before the system starts writing on the disk. The value only goes from 0 to 100.**
- `sudo pongtwkr dirtybackground <value>`
**Sets the dirty memory % before the system starts writing on the background. The value only goes from 0 to 100** ***AND SHALL ALWAYS BE SMALLER THAN DIRTY RATIO.**
- `sudo pongtwkr cachepressure <value>`
**Sets the VFS Cache pressure to the designated value.**
- `sudo pongtwkr cpumin <value_in_GHz>`
**Sets the CPU minimum frequency to the designated value.**
-  `sudo pongtwkr cpumax <value_in_GHz>`
**Sets the CPU maximum frequency to the designated value.**
> Please note that the CPU will automatically cap itself: If you have a 3.5GHz CPU, no matter if you run `sudo pongtwkr cpumax 7 override` the CPU will be capped to 3.5GHz.
-  `sudo pongtwkr cputurbo <true/false>`
**Enables/Disables Intel Turbo Boost or AMD Precision Boost depending on your system.**
-  `sudo pongtwkr hugepages <count>`
**Sets the HugePages to the designated number.**
-  `sudo pongtwkr thp <enable|disable|madvise>`
**Sets the THP (Transparent Huge Pages) to the designated option.**
-  `sudo pongtwkr smt <true/false>`
**Toggles the SMT (Multithreading) to the designated option.**
- `sudo pongtwkr wifipower <true/false>`
***Enables / Disables the WiFi Save Power*** TRUE disables it, FALSE enables it.
> Made it that way so the logic is "TRUE = Optimized".
- `sudo pongtwkr wmem <value>`
***Sets the maximum WMEM Buffer Size to the determinated value.***
- `sudo pongtwkr rmem <value>`
**Sets the maximum RMEM Buffer Size to the determined value.***
> Note that in WMEM & RMEM values should be entered with M for Mb, K for Kb and integers for bytes. Ex: `sudo pongtwkr rmem 16M`
- `sudo pongtwkr offload <feature> <true/false>`
***Enables / Disable the offload of the selected feature.***
> The officially supported features are `gro, lro, tso, gso`. If you input any other feature feature, it will probably work because PongTWKR uses ethtool, but it will send errors, wrong messages or sum...
- `sudo pongtwkr tcpmetrics <true/false>`
***Enables / Disables the TCP Metrics.***
- `sudo pongtwkr mtuprobing <true/false>`
***Enables / Disables the MTU Probing.***
- `sudo pongtwkr numa <true/false>`
***Enables / Disables NUMA Balancing.***
- `sudo pongtwkr zswap <true/false>`
***Enables / Disables ZSWAP***
- `sudo pongtwkr zswapalgo <algorithm>`
***Applies the entered ZSWAP algorithm.***
- `sudo pongtwkr zswappool <0-100 value>`
***Sets the max ZSWAP Pool max % value.***
- `sudo pongtwkr zramalgo <algorithm>`
***Applies the entered ZRAM algorithm.***
- `sudo pongtwkr zramsize <size>`
> As other size tweaks, zramsize accepts 4G, 4000M and Bytes inputs.
***Sets the ZRAM Size to the entered size***
- `sudo pongtwkr zramstreams <streams>`
> Automatically capped to your CPU Thread count.
***Sets the ZRAM streams  to the designated value.***
## Misc.
- `sudo pongtwkr info`
**Shows a quick-info panel with a cool ASCII. Totally-self-produced idea... *cough* fastfetch but with other info... *cough* yeah..-**
- `sudo pongtwkr reset`
**Resets all the tweaked values to the ones that were setted when the first command EVER was ran.**
- `sudo pongtwkr safe`
**Sets all the parameters to safe options that won't harm any system.**
- `sudo pongtwkr save <profile_name>`
**Saves the current tweaks to a .json on ~/.pongtwkr, to load them later with `sudo pongtwkr load <profile_name>`.**
- `sudo pongtwkr load <profile_name>`
**Loads the profile selected, from the .json on ~/.pongtwkr.**



## Parameters
- `sudo pongtwkr <command> info`
**Shows an essential description of the command.**
> Yeah. It works for `sudo pongtwkr info`. `sudo pongtwkr info info` is a thing, lol...
- `sudo pongtwkr <command> override`
**Overrides the safety values. Don't try anything stupid...**
