# `create_perms.py`

This script is used to perform functions related to similar mapping to trustwords

### Average permutations

The average calculation is split into two sections:

 - **Multi-mapping**
   - Calculating the average number of multi mapped words

 - **Similar**
    - Uses a defined similar list to create all the permutations

Multi-mapping
```
python trustwords_util.py --average-multi -s <SIMILAR_LIST>
```

Similar
```
python trustwords_util.py --average -s <SIMILAR_LIST>
```
        
### Trustwords from keys

Two pem key files can be passed as parameter and the resulting trustwords can be produced.

```
python trustwords_util.py -t <KEY_1> <KEY_2>
```

### Find key
Finds an actual key that creates the biggest permutation size.

```
python trustword_util.py -f -s <SIMILAR_LIST>
```

### Permutations from words
A set of trustwords can be passed as a parameter. The script will out the number of similar permutations

```
python trustword_util.py -p "['WORD1', 'WORD2', 'WORD3', WORD4']" -s <SIMILAR_LIST>
```

### Options

**Similar list (`-s`)**
<br/>
The similar word list can be changed. This is required for some modes

**Language (`-l`)** 
<br/>
Language can be changed

**Key (`-k`)**
<br/>
Controllable key can be changed

**Number of words (`-n`)**
<br/>
Number of words can be changed