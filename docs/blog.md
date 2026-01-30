# ENTRY 6 | January 30, 2026, 03:27 A.M.

Hey there. Feeling a bit better after chilling out some time. Now I'm taking the time to properly update the documentation:

v0.7 was a smooth ride. Well, almost. All because of f*cking, mem_limit.

You see, since v0.5 I've been following this workflow;

Adding of the key features -->
Adding info parameter of the new features -->
Adding the new features to safe command -->
Adding new features to the profile supporting -->
Adding new features to the reset command -->
Bugfixing and tweaking

Now, when all of this updates key features were added, I move onto adding them to the profiles. When I tried them: the loading line for `mem_limit` worked when saving and loading, but, for some reason, it just didn't update the values. After some research, I determined it was a perms thing, because mem_limit file was write only, not read ig. So then I made a force read function thinking that it would work, but it didn't. I was tired and frustrated, so:

`tired dev + annoying feature = Annoying feature was deleted succesfully.`

I think the command itself worked properly, and writed the mem limit, but I rather delete a feature more than having it incomplete.

So, if I'm having problems with shity mem limit, I don't want to imagine how will v0.8 will go with Nvidia drivers... fuck it.

I'll continue uploading the docs and then the source code. See ya.



------------------------------------------------------------------------------------------------------------------------------------------------------
# ENTRY 5 | January 30, 2026, 00:55 A.M.
So... well. I don't feel very well today, but anyways, worked on v0.7, and completed it. Had a hard time, but not because of the update itself, more because I wasn't feeling well anyways. I'm afraid I'm not updating changelog, commands, roadmap, sourcecode and readme until tomorrow... but this is just for you guys to know that the v0.7 is complete.

I don't have anything else to say... more than thank you for reading this.

See ya.

------------------------------------------------------------------------------------------------------------------------------------------------------
# ENTRY 4 | January 29, 2026, 3:42 A.M
Uhum. Yeah... I didn't sleep. I was about to turn off the computer when I saw the roadmap and thought... "well, it can't be too hard to rush this, right?" I was right, apparentely. 3 hours passed and I've completed v0.6 adding even more tweaks than I was originally going to do: I only was planning to add TCP Metrics, WiFi Powersave and MTU Probing, and I ended up adding Buffer (RMEM and WMEM) and Offloading tweaks. Cool, right?

When fixing bugs, I tried to add things such as Packet Loss, WiFi Speed, DNS, etc. to `sudo pongtwkr info` because of the rush of the moment, and I've ended up making it go from a fast, easy to read command to a monster that delayed 11s to display info. Of course this wasn't added to the final version of v0.6...

I've also **ALMOST** forgot to add the new features to the Profile support. I've realised just before clicking commit changes...

Anyways, now, yeah, I'm heading to sleep... See ya.


------------------------------------------------------------------------------------------------------------------------------------------------------
# ENTRY 3 | January 29, 2026, 00:40 A.M
So crap... v0.5 is here now. Oh lord... This was the first "obstacle" in developing, making persistent changes with systemd. Oh, and THP, f*ck THP and how it saves in the Kernel. Had to do a whole "translator" from Kernel to CLI and from CLI to Kernel.

Excluding persistency and THP, profiles were easy: just `import json` and I was done. Oh, and I made my promise of fixing THP. In less than 7 hours...

I think the update was more centered on bugfixing & persistency than... profiles. For example, I've just realised that `sudo pongtwkr reset` was *almost* useles:

`sudo pongtwkr <any_command>`
> Here, the code runs `save_default()`, and saves the configuration to then replicate it with `sudo pongtwkr reset`
`sudo pongtwkr reset`
> Now it resets to the values that `save_default()` saved

**The problem:** if the first command was one that tweaked anything, the `save_default()` saved it. Understand? No? Well, no one is reading this, so I don't care.

Now, I'll go to sleep... or I dont know. See ya.
------------------------------------------------------------------------------------------------------------------------------------------------------
# ENTRY 2 | January 28, 2026. 5:07 P.M
Aw man... here we are. I've completed the update for now. **Dooon't, stop, me noww....**

I've had a hard time dealing with THP reseting when using `sudo pongtwkr reset`, since the Kernel does not like strange values, i've decided just to let it be, and just not reset it. Apart from that, it was a smooth ride: almost no errors / debugs.

If we ever get to make PongTWKR something big, I promise to fix that. Or not. I Don't really know...

Also had to dealt with `glob` finding the fan routes. If it's controlled by BIOS, then it won't pop up on `sudo pongtwkr info`.

Anyways, just working hard. Nothing else. See ya...

------------------------------------------------------------------------------------------------------------------------------------------------------
# ENTRY 1 | January 28, 2026. 2:16 A.M.
So. Hello! First entry here. I've just completed v0.3 "Foolproof". Decided it was a good way to limit the options, and added info.

When I coded this, I was half awake half asleep, so the first version had atrocious ortographic mistakes. Before doing this, I was feeling a bit dizzy, but I wen to sleep and I've got better. 

This update was needed, because, if I keep going with this in the future, a tweaker that lets you break your entire system, is, well... a not-so-useful-tweaker... anyways. Today I added /PongTWKR/docs. And did v0.2 and v0.3. 


Tomorrow, or in a couple of hours if I'm still awake, I'll upload v0.4. 

If anyone reads this, lol, I guess you found a simple tweaker too early... see ya.

------------------------------------------------------------------------------------------------------------------------------------------------------
