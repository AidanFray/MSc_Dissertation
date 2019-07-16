file_path = "."

def load_mappings(fileName, mapping):
    """
    Loads the hex -> word mapping into a local dictionary
    """

    with open(f"{file_path}/{fileName}") as file:

        line = None
        while True:
            line = file.readline()
            if line == '':
                break
            
            line_parts = line.split(",")

            # Maps string to
            word = line_parts[2]
            word_hex = hex(int(line_parts[1]))[2:].zfill(4)

            # Hex --> Word
            mapping._hex_to_word_mapping.update(
                {
                    word_hex: word
                })

            # Word --> Hex
            if word in mapping._word_to_hex_mapping:
                mapping._word_to_hex_mapping[word].append(word_hex)
            else:
                mapping._word_to_hex_mapping.update({word: [word_hex]})

def load_similar_mappings(fileName, mapping):
    """
    Loads the mapping that have been found to be similar
    from an external file. The external loading uncouples
    this program from the method used to determine
    'similarity'
    """
    with open(f"{file_path}/{fileName}") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        line_parts = line.split(",")

        base_word = line_parts[0]
        similar_words = line_parts[1:-1]

        mapping._similar_word_mapping.update({base_word: similar_words})
