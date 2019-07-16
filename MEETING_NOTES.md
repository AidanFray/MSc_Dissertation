# Meeting Notes

Minimum wage: $7.25

Living wage:  ~$15.00

## Experiment 1

### Participants and timings

Timing: **2:30 mins**

Required participants: **80** (5 samples per metric total required 384)

Payment per completion: **$0.30**

TOTAL:                  **$24**


### Wordvec value
Choice for the Word vector size

```
Soundex         - 1,527,554

Word vector 
             3   - 14,550
            (4)  - 73,962
             5   - 685,516

Leven
            1   - 97,730
            2   - 1,070,656

Metephone       - 412,916
NYSIIS          - 188,474
```

## Experiment 2

### Participants and timing

Timing: **3.5 minuites**

Required participants: **385**

Payment for completion: **$0.42**

TOTAL:                  **$161.7**

### Currrently broken attacks

Examples like:
```
'MOTTLE', 'INTEROCULAR', 'COLONIAL', 'PLEASANTER'
'SOCORRO', 'WIGEON', 'STRONGBOW', 'ARCO'
```

Are producing **exactly** the same audio as their worded counterparts. This is proudcing attacks that show literally nothing.

### Attack Cases

Number of permutations aim for a 24 hour compute time.

```
0 static words (100,000 -   1 GPU) (2^48)
1 static words ( 10,000 -  10 GPU) (2^51)
2 static words (  1,000 - 100 GPU) (2^54)
```

Where all attack keys will be sampled from a list of keys
found as **vulnerable**

### 1,000 - 2 static words

```
soundex      67671/100000   (67.67%)
metaphone    11759/100000   (11.75%)
nysiis       4638/100000    ( 4.63%)
leven        1727/100000    ( 1.72%)
wordvec      1187/100000    ( 1.18%)
```

### 10,000 - 1 static words

```
soundex      83364/100000   (83.36%)
metaphone    15750/100000   (15.75%)
nysiis       6422/100000    ( 6.42%)
leven        2979/100000    ( 2.97%)
wordvec      2359/100000    ( 2.35%)
```

### 100,000 - 0 static words

```
soundex      92006/100000   (92.00%)
metaphone    22902/100000   (22.90%)
nysiis       10900/100000   (10.90%)
leven        6537/100000    ( 6.53%)
wordvec      5478/100000    ( 5.478)
```

# Test pilot study

Remove results with a "high" average for the random values?

```
Leven       - 3.49
WordVec     - 2.91
NYSIIS      - 2.78
Metaphone   - 2.51
Soundex     - 2.38
Random      - 1.52
```

Rejectable result
```
8 
    RANDOM VALUES: ['4', '4', '2', '3', '4']
    UNIVERISTY-UNIVERISTY: 3
```