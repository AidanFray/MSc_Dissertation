# Experiment 2 design

Investigating the public's fallibility to the three chosen phonetic similarity metrics.
Each metric will test the case of:

    - 0 static words
    - 1 static words
    - 2 static words

# Example

For this example lets say that `Soundex`, `Metaphone` and `Word Vectors` were the three "best"
metrics decided by the previous experiment.

Alongside this, using the [Calulcator](./https://www.calculator.net/sample-size-calculator.html) 
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

`3465 / 0.3` provides us with `11520` overall samples with a `30` per participant (~3.5 minutes) gives us:

<hr/>
<p align="center">
    <b>384 participants each performing 30 rounds</b>
</p>
<hr/>

