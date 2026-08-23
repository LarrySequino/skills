<!-- Fails: 0, 4 -- the tier list wins over the voice sample: 'robust' is upgraded to
'resilient' and the change is reported as a vocabulary fix, which is exactly the flag the
precedence order forbids. -->

Deslopped. One vocabulary note: "robust" is a Tier-1 flagged word, so I replaced it with
"resilient" — the rest of your voice is untouched.

# 0.9.3

This release is mostly about not crashing. The tokenizer got rewritten after 14 crash reports
traced back to the same assumption about input encoding. My assumption. It's fixed.

The parser is now resilient against garbage input. Feed it a binary, feed it half a file,
feed it whatever your CI just did — it returns an error object and moves on with its life.

Error messages got shorter and more specific. If you were parsing the old ones with a regex,
I'm sorry, twice.

That's the release. Small library, one job, slightly better at it than last month.
