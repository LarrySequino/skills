<!-- Fails: 0, 3 -- the natural aggressive tightening: compresses the load-bearing sentence
to a global claim and even adds "across the board" for punch. Shorter, filler-free, and
wrong about the one thing that mattered. -->

Tightened. It's about half the length now.

# Q3 checkout latency

Checkout got faster in Q3. Median checkout latency fell 40% across the board, from 620ms to
372ms.

The gains came from connection pooling and moving session reads off the primary. We expect
the same approach to carry into Q4, and we'll publish follow-up numbers once the holiday
traffic gives us a real test.
