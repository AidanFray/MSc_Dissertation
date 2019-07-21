# Similar Words

C++ Program used to run through a dictionary and collate a list of matches using a defined metric.

E.g.

```
./SimilarWords.out <LIST_IN> <LIST_OUT> -l
```

Will compute all the matches of `LIST_IN` using Levenshtein distance as the metric

## Params

```
-s - Soundex
-l - Levenshtein
-m - Metaphone
-v - Word Vector
-n - NYSIIS
```