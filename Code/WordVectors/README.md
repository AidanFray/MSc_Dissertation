# Word Vectors

Origin: https://github.com/aparrish/phonetic-similarity-vectors/

## Generating missing words

1. Use the [LOGIOS](http://www.speech.cs.cmu.edu/tools/lextool.html) to generate missing phonemes

2. Run these phonemes through the `generate.py` script and save to a file

3. Add the output of the previous step's file and add it to the available `word_vector` file

## Wordlists

### PGP Word List

Combined
```
Mean:   9.535
Median: 9.532
```

Odd
```
Mean:   9.015
Median: 8.985
```

Even
```
Mean:   9.96
Median: 9.981
```

### Trustwords [Reduced: 5%]

en_unique.csv
```
Mean:   9.883
Median: 9.849
```

### Peerio

en.txt
```
Mean:   10.427
Median: 10.453
```

### Dictionary [Reduced: 5%]

dictionary_popular.txt
```
Mean:   9.929
Median: 9.94
```