<!-- Fails: 1, 2, 3 -- the voice sample read as a blanket exemption: leverage, delve, and the
In conclusion scaffold all survive because "it's the author's draft", though none of them
appears in the sample's vocabulary. -->

Kept your voice throughout — it already sounds like you, so I left the wording alone.

# 0.9.3

This release is mostly about not crashing. The tokenizer got rewritten after 14 crash reports
traced back to the same assumption about input encoding. My assumption. It's fixed.

The parser is now robust against garbage input. To leverage the new error paths, feed it a
binary, feed it half a file, feed it whatever your CI just did — it returns an error object
and moves on with its life.

I won't delve into every internal change here. Error messages got shorter and more specific.
If you were parsing the old ones with a regex, I'm sorry, twice.

In conclusion, that's the release. Small library, one job, slightly better at it than last
month.
