# PGP Fingerprints

## DEF CON 22 - Check Your Fingerprints - Cloning the Strong Set

https://www.youtube.com/watch?v=Ow-YcP_KsIw

https://evil32.com/

A talk about the weaknesses in the GPG implementation.

To include a PGP key you can either specify a 64 bit or 32 bit ID

Mentions the web-of-trust. This requires some more research.

Demo of PGP package verification. Vulnerability is with collisions in Key IDs

Big part of the video is the method used to generate keys for checking collisions. They quote the tool at being able to achieve 500 million key generations a second.

It works by generating a single key and then just incrementing it's exponent, the new key is then hashed and checked against the target.

64bit keys are a little harder
```
Looking for any of 100 keys with 20 mid range GPUs takes 107 days
```

