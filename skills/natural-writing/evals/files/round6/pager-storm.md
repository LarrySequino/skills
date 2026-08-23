We took 900 pages in one week. Nine hundred! I counted them on a Sunday because I couldn't sleep, and somewhere around page 400 I stopped reading the text at all. That's the part that should have scared me.

Here is what the count said: 812 of those pages were the same three alerts. Disk over 80 percent on the log box (it has been over 80 percent since 2023, it is fine, and it will be fine next year). A p99 latency alert that fires on any single request slower than two seconds, which the batch export does at 04:00 every day, by design. And a synthetic check still probing a health endpoint we deprecated in March.

So we didn't have an alerting problem. We had a nobody-turns-alerts-off problem.

That distinction decides the fix. You can tune thresholds for a month and the pager still goes off at 4am, because the thresholds were never the thing. Somebody has to delete rules. It is worth noting that deleting things is unpopular in a way that tuning things is not.

We deleted 41 rules in an afternoon. Kept 12. The test we used was blunt: if a rule has fired more than twice and nobody has ever *acted* on it, it isn't an alert, it's a *notification*, and notifications go to a channel, not to a phone. None of this is a new idea. The SRE book has been saying it since 2016. Reading it and doing it on a Thursday are different activities.

Pages the following week: 31. Thirteen of the 900 had been real, which is 1.4 percent; 6 of the 31 were, which is about 19 percent. Sleep improved (mine, and Ruth's, who had the rotation after me). But honestly the bigger change was that people started reading the pages again. When the pager means something, you look at it. When it doesn't, you learn not to.

Two things I'd do differently. I would have pulled the acted-on counts before the meeting instead of arguing from memory, because the counts ended the argument in four minutes and the memory version of that argument had been running since February. And I would have put the deletion review on a repeat. We're back up to 19 rules already. Nineteen! Three of them look familiar.
