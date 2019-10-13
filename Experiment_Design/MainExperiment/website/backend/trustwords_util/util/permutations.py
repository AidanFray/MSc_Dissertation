import itertools
import sys

from .CONFIG import *
from .mappings import *

def multimap_perms(wordlist, mapping, PRINT=True):
    combinations = multimap_combinations(wordlist, mapping)

    if check_perm_size(combinations):
        perms = get_perms(combinations)

        if PRINT:
            print(f"[*] Mapping allows {len(perms)} same combinations!")

    return perms

def multimap_combinations(wordlist, mapping):
    combinations = []

    for word in wordlist:
        combinations.append(mapping.getMapping(MappingModes.WordToHex, word))

    return combinations

# BUG: List created by this method contains repeated values
    # Temporary fix is to set() the output
def similar_perms(trustwords, mapping, PRINT=True, staticPos=[]):
    """
    This method takes multi-mappings (Same word multiple value) and
    similar words and creates all the permutations of fingerprints
    that allow these near matches
    """

    fingerprint_chunks = similar_combinations(trustwords, mapping, staticPos)

    if not check_perm_size(fingerprint_chunks):
        output_perms = get_perms(fingerprint_chunks, limit=True)
    else:
        output_perms = get_perms(fingerprint_chunks, limit=False)
        
    if PRINT: 
        print(f"[*] Mapping allows {len(output_perms)} similar combinations!")

    return list(set(output_perms))

def similar_perms_size(trustwords, mapping, staticPos=[]):
    """
    This method just calculates the size of the permutations
    this should save time and memory
    """
    fingerprint_chunks = similar_combinations(trustwords, mapping, staticPos)
    return get_perm_size(fingerprint_chunks)

def similar_combinations(trustwords, mapping, staticPos=[]):
    similar_words = []

    # Finds all similar words from the current fingerprint
    for index, word in enumerate(trustwords):

        if index not in staticPos:
            try:
                similar_words.append(mapping.getMapping(MappingModes.SimilarWord, word))
            
            # No similar words
            except KeyError:
                similar_words.append([])

        else:
            similar_words.append([])

    for index, _ in enumerate(similar_words):
        # Adds the original words to the lists
        similar_words[index].append(trustwords[index])

    # Then finds all multi-mapped words and calculates the full number of perms
    fingerprint_chunks = []
    for words in similar_words:

        perms = []
        for w in words:
            chunk = mapping.getMapping(MappingModes.WordToHex, w)
            perms += chunk

        fingerprint_chunks.append(perms)

    return fingerprint_chunks.copy()

def get_perms(lists, limit=False):
    """
    This method uses ittertools to create all the
    permutations of fingerprints
    """
    perm_size = 1
    for l in lists:
        perm_size *= len(l) 

    size = len(lists)

    if limit:
        max_list_size = int(MAX_PEM_SIZE ** 0.25)
    else:
        max_list_size = None

    # Minimum size
    if size == 4:
        return list(itertools.product(
                    lists[0][:max_list_size],
                    lists[1][:max_list_size],
                    lists[2][:max_list_size],
                    lists[3][:max_list_size],
                    ))
    else:
        raise Exception("Invalid permutation size!")

def check_perm_size(lists):
    perm_size = get_perm_size(lists)

    if perm_size > MAX_PEM_SIZE:
        sys.stderr.write(f"[!] Permutation too big at: {perm_size}. Ignoring due to RAM constraints\n")
        return False
    else:
        return True

def get_perm_size(lists):
    perm_size = 1
    for l in lists:
        perm_size *= len(l) 

    return perm_size