# The first collisions for full SHA1

Attack relies on *Differential cryptanalysis*.

This is techniques designed ultimately to provide a delta of zero at the end.
The process involves undoing the previous operations of the other.

For example because of the Merkle-Damgard construction:

![](https://i.stack.imgur.com/2ZN51.png)

They introduce a difference with `M1(1)` and `M1(2)` and remove it with `M2(1)` and `M2(2)`. **How is this done**?

With the Prefix `P` and Suffix `S` if the center message blocks return the save value this will produce a collision.