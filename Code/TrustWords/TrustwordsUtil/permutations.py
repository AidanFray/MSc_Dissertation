import itertools

from CONFIG import MAX_PEM_SIZE

def multimap_perms(wordlist, mappingWordToHex, PRINT=True):
    mappings = multimap_combinations(wordlist, mappingWordToHex)

    if check_perm_size(mappings):
        perms = get_perms(mappings)

        if PRINT:
            print(f"[*] Mapping allows {len(perms)} same combinations!")

    return perms

def multimap_combinations(wordlist, wordToHexMapping):
    mappings = []

    for word in wordlist:
        mappings.append(wordToHexMapping[word])

    return mappings

def similar_perms(trustwords, similarWordMapping, wordToHexMapping, PRINT=True):
    """
    This method takes multi-mappings (Same word multiple value) and
    similar words and creates all the permutations of fingerprints
    that allow these near matches
    """

    fingerprint_chunks = similar_combinations(trustwords, similarWordMapping, wordToHexMapping)
    
    output_perms = []
    if check_perm_size(fingerprint_chunks):
        output_perms = get_perms(fingerprint_chunks)
        if PRINT: print(f"[*] Mapping allows {len(output_perms)} similar combinations!")

    return output_perms

def similar_combinations(trustwords, similarWordsMapping, wordToHexMapping, staticPos=[]):
    similar_words = []

    # Finds all similar words from the current fingerprint
    for index, word in enumerate(trustwords):

        if index not in staticPos:
            try:
                similar_words.append(similarWordsMapping[word])
            
            # No similar words
            except KeyError:
                similar_words.append([])

    for index, _ in enumerate(similar_words):
        # Adds the original words to the lists
        similar_words[index].append(trustwords[index])

    # Then finds all multi-mapped words and calculates the full number of perms
    fingerprint_chunks = []
    for words in similar_words:

        perms = []
        for w in words:
            chunk = wordToHexMapping[w]
            perms += chunk

        fingerprint_chunks.append(perms)

    return fingerprint_chunks

def get_perms(lists):
    """
    This method uses ittertools to create all the
    permutations of fingerprints
    """

    perm_size = 1
    for l in lists:
        perm_size *= len(l) 

    size = len(lists)

    # Full mapping
    if size == 10:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                    lists[4],
                    lists[5],
                    lists[6],
                    lists[7],
                    lists[8],
                    lists[9]
                    ))

    # Long mapping
    if size == 9:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                    lists[4],
                    lists[5],
                    lists[6],
                    lists[7],
                    lists[8],
                    ))

    # Short mapping
    elif size == 5:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                    lists[4],
                    ))

    # Minimum size
    elif size == 4:
        return list(itertools.product(
                    lists[0],
                    lists[1],
                    lists[2],
                    lists[3],
                    ))
    else:
        raise Exception("Invalid permutation size!")

def check_perm_size(lists):
    perm_size = get_perm_size(lists)

    if perm_size > MAX_PEM_SIZE:
        print(f"[!] Permutation too big at: {perm_size}. Ignoring due to RAM constraints")
        return False
    else:
        return True

def get_perm_size(lists):
    perm_size = 1
    for l in lists:
        perm_size *= len(l) 

    return perm_size
