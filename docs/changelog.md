# CHANGELOG 
## Here will go the changes added to the tweaker. 

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
