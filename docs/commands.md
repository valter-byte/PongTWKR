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
## Misc.
- `sudo pongtwkr info`
**Shows a quick-info panel with a cool ASCII. Totally-self-produced idea... *cough* fastfetch but with other info... *cough* yeah..-**
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
