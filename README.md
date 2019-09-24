# Investigating the Security of p≡p’s Trustwords

**Abstract** – Many encrypted connections require
the comparison of a fingerprint to protect
against eavesdropping. A substantial amount
of past work has aimed to propose fingerprint
representations that work better with human
limitations. “Trustwords” proposed by pEp
is an example of such a scheme, where the
fingerprint is encoded as words in an attempt
to improve usability.

This work’s main aim is to assess if Trustword’s recommended minimum number of four
words is sufficient. In order to achieve this goal,
this work implements an attack on Trustwords
and quantifies its effectiveness on more than
400 participants. A tool called GreenOnion
was designed to assist in quantifying attack
feasibility. GreenOnion improved substantially
on a similar tool’s ability to search for matches
concurrently. Our findings show a substantial
increase in attack success compared to related
literature.
We believe this increase is due
to levering the design flaws in the Trustword
scheme. Therefore, we believe a minimum of
four Trustwords is insufficient to provide even a
basic level of security.
