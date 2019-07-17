# Key Attacks

This section will do the actual computation of the attack. 

The `target_key_priv.asc` is the randomly generated target key. This is the one we cannot change and, therefore, will remain static over
all experiments.

## Goal

The aim here is to show the actual attack is possible and its complexity. Due to how the main experiment has distributed out attacks into three strengths:

 - Zero static words
 - One static word 
 - Two static word

The overall aim will be to show that it is possible to find a key for each scenario. In this context the metric used doesn't matter as I won't be assessing the actual strength of them.

## Steps

1. Generate a "best scenario" key. This will involve a random search for the key with the highest number of combinations. This will be repeated for each attack strength.

2. This best key will then be used to generate a list of near collisions.

3. This near collision list will be used to find a key.

## TODO:

### NYSIIS
- [ ] Zero static
- [ ] One static
- [ ] *Two static* (In progress)