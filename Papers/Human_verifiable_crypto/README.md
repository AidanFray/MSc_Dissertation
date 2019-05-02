# Human Verifiable Crypto

## Can Unicorns Help Users Compare Crypto Key Fingerprints?

Study used 661 participants to test.


Paper talks about the optimal length of fingerprints and why they need to be a certain length:
```
Fingerprints are by design long enough for it to be exceedingly
unlikely that two different keys will have the same fingerprint,
yet short enough for manual comparison to be feasible.
```

Other possibilities to the conventional hexadecimal form:

- ASCII art
- Numbers
- Pronounceable strings
- Avatars
- SAS
- Compare-and-select

Initial recommendations from the paper:

When security is the highest **none** of the representations were adequate

Graphical representations are best for usability but in low risk situations

For balance use-cases textual representations (i.e. hexadecimal) seems most appropriate

The testing environment involved the use of MTurk. They enrolled people in a fictional scenario. Where they had to fill out information regarding SSN with a time limit.

During this time a pop-up appeared stating that a message was available from a possible employee. They had to check the fingerprint with the one visible on the 'desk'. To simulate modern pressure they included a $1 bonus to the participants that could complete the task the quickest.

WhatsApp uses iterated hashing to improve its fingerprint?

### RESULTS

The best was sentences where participants only missed 6% of the attacks. Unicorns was the worst where 54% of the attacks were missed.

Hexadecimal was around 21% attacks missed. Uppercase and lower case were very similar.

Attack strengths also did not seem to affect the miss rate.

They didn't test the use of software to check the signature. Examples of this are QR codes and smartphone cameras.


## Usability and Security of Out-Of-BandChannels in Secure Device Pairing Protocols

Paper will focus on the use of Out-of-band (OOB) authentication that can be used to verify or transport crypto secrets

OOB utilises human involvement to set-up and manage authentication channels

OOBs are somewhat not vulnerable to MITM attacks. One example is direct human interaction. With the correct config the trust exhibited here can be transferred to the party's devices.

Examples of OOBs are: 

- Comparison of visual, auditory or language based content 
- Pictures of QR codes taken using a device

Paper ranks usability:

- Comparing strings
- Typing strings 
- Comparing and selecting strings
- Barcode scanning

Then, with security included:

- Typing strings
- Barcode scanning
- Comparing and confirming
- Comparing strings