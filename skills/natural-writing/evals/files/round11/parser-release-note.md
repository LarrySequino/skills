# parser 0.9.3

This release took longer than I meant it to. I got stuck on one nasty edge case for about two weeks and had to admit my first fix was wrong before I found the real one. That's most of what this release is: one big fix and a handful of smaller patches around it.

The headline is that the tokenizer no longer chokes on malformed input the way it used to. We had 14 crash reports tied to the same root cause, all variations on badly nested brackets, and all of them are gone now. The parser is more robust against garbage input than it's ever been, which is a low bar, but I'll take it.

To leverage the new error paths, I also cleaned up how failures get reported, so you get a line number instead of a stack trace pointing at nothing. I didn't delve too deeply into performance this round, mostly because I ran out of time, not because it didn't need it.

In conclusion, this is a small release that fixes a real problem. Update when you get a chance, and if you hit anything weird, please open an issue. I read all of them, even the ones that turn out to be my own fault.
