I have the dialogue working with tkinter. That was GPT4 and pretty easy.

The next step is telling when we are AFK.
I think querying the activity watch server for AFK events and seeing if we just closed one out with more than x minutes is a good idea.
That way this app does not need to worry about detecting AFK itself.
And also the AFK is always in sync.
This app could even save the ID of the AFK event as metadata.

Before release, make it easy to report bugs. See https://twitter.com/ID_AA_Carmack/status/1705223649790144724.
