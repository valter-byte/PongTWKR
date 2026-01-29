# ENTRY 3 | January 28, 2026, 00:40 A.M
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
