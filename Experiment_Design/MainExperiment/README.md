# Experiment Design

### Rounds
35 (5 at the start always benign)

### Attack Ratio
30/70 Attack to non-attack with there being an equal chance to receive one of three attacks:

    - 0 static words (100,000 perms  - 1   GPU Day)
    - 1 static words (10,000  perms  - 10  GPU Days)
    - 2 static words (1,000   perms  - 100 GPU Days)

NOTE: Number of permutations aim for a 24 hour compute time.

These are defined with attack strength in mind. Where all attack keys will be sampled from a list of keys
found as **vulnerable** with these permutations in mind

Three metrics will also be assessed. The ones chosen will be selected in 
the pilot study.

### Vulnerable keys percentages

**TODO**

### Data Collection
    - Overall Start/end time
    - Round Start/end time
    - Accept/Decline results
    - User agent
    - Audio button clicks

## Attention metrics
    - Audio button clicks - (i.e. 0 button clicks is a red flag)
    - Time taken (This will require creating a 'reasonable' time)

## Statistical Design

For this example lets say that `Soundex`, `Metaphone` and `Word Vectors` were the three "best"
metrics decided by the previous experiment.

Alongside this, using the [Calculator](./https://www.calculator.net/sample-size-calculator.html) 
using the values: 

    - Confidence level          - 95%
    - Margin of error           - 5%
    - Population proportion     - 50% 
        - (Potential for the attack-miss percentage to be higher or lower than the true value)

Gives us a sample size of `385`. So we need `385` samples to give us the desired constraints defined 
previously. This, however, applies to each metric and each attack.

This is assuming they are all equally sampled. I.e. `Soundex - 1 static words` is equally likely as `Metaphone - 0 static words`. 

So for `Soundex`:

    - 0 static words: 385 samples
    - 1 static words: 385 samples
    - 2 static words: 385 samples

This gives a total of `1155` samples per metric. 

Providing us with a total of `3465` samples required to provide a confidence level of `95%` alongside a margin of
error `+- 5%`.

However, due to the split of 70/30 for non-attacks/attack for the simulation we will require a higher number of samples. 
This means as `70%` of the samples are effectively pointless we need to increase the sample values to match the proportion

`3465 / 0.3` provides us with `11520` overall samples with a `30` per participant gives us:

<hr/>
<p align="center">
    <b>384 participants each performing 30 rounds</b>
</p>
<hr/>
