# Complex wordlist generator
# written in python by Vlad Stanoiu

import itertools

def generate_wordlist(base_word, prepend_number, append_number, prepend_symbols, append_symbols, middle_symbols, start_year, end_year, complex_mode):
    """Generates the wordlist according to the specifications."""
    wordlist_set = set()  # Use a set to avoid duplicates

    # Replacement rules for complex mode
    replacements = {
        'a': ['a', '@'],
        'A': ['A', '@'],
        'e': ['e', '3'],
        'E': ['E', '3'],
        'i': ['i', '1'],
        'I': ['I', '1'],
        'o': ['o', '0'],
        'O': ['O', '0'],
        's': ['s', '$'],
        'S': ['S', '$']
    }

    def get_complex_variations(word):
        """Generate all complex variations based on the replacement rules and symbol combinations."""
        # Generate permutations for uppercase and lowercase letters
        permutations = itertools.product(*[c.lower() + c.upper() for c in word])
        base_word_variations = [''.join(perm) for perm in permutations]
        
        # Add symbol replacements
        variations = set()
        for base in base_word_variations:
            for replacement in itertools.product(*(replacements.get(char, [char]) for char in base)):
                variations.add(''.join(replacement))
        return variations

    def get_base_word_variations(word, complex_mode):
        """Generate variations of the base word based on the mode."""
        if complex_mode:
            return get_complex_variations(word)
        else:
            # Permutations of uppercase and lowercase letters
            permutations = itertools.product(*[c.lower() + c.upper() for c in word])
            return set(''.join(perm) for perm in permutations)

    # Symbols
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

    def add_combinations(word):
        """Adds combinations based on prepend, append, and symbols settings."""
        combinations = set()

        # Apply prepend number
        word_with_number = word
        if prepend_number:
            word_with_number = f"{prepend_number}{word}"

        # Apply prepend symbols
        if prepend_symbols:
            for symbol in symbols:
                combinations.add(f"{symbol}{word_with_number}")

        # Add the word with number to the combinations
        combinations.add(word_with_number)

        # Add year ranges if specified
        if start_year is not None and end_year is not None:
            temp_combinations = set()
            for year in range(start_year, end_year + 1):
                temp_combinations.update({f"{comb}{year}" for comb in combinations})
            combinations = temp_combinations
        elif start_year is not None:
            combinations = {f"{comb}{start_year}" for comb in combinations}

        # Apply middle symbols only if start/end year is used
        if middle_symbols and (start_year is not None or end_year is not None):
            temp_combinations = set()
            for comb in combinations:
                for symbol in symbols:
                    temp_combinations.add(f"{comb[:-4]}{symbol}{comb[-4:]}")  # Adding symbol between base word and year
            combinations = temp_combinations

        # Apply append symbols
        if append_symbols:
            temp_combinations = set()
            for comb in combinations:
                for symbol in symbols:
                    temp_combinations.add(f"{comb}{symbol}")
            combinations = temp_combinations

        # Apply append number
        if append_number:
            combinations = {f"{comb}{append_number}" for comb in combinations}

        return combinations

    # Generate wordlist
    base_word_variations = get_base_word_variations(base_word, complex_mode)
    
    for word in base_word_variations:
        combinations = add_combinations(word)
        wordlist_set.update(combinations)

    return sorted(wordlist_set)

def main():
    # Ask for user input
    base_word = input("Enter the base word (e.g., test): ").strip()
    
    mode = input("simple / complex: ").strip().lower() # Do you want the word to be simple (without symbols - only upper/lowercase) or complex (using all combinations Upper-Lowercase and symbols instead)
    complex_mode = mode == 'complex'
    
    start_year_input = input("Enter the start year for the range (e.g., 2000) or press Enter to skip: ").strip()
    start_year = int(start_year_input) if start_year_input else None
    
    end_year = None
    if start_year is not None:
        end_year_input = input("Enter the end year for the range (e.g., 2010) or press Enter to use the start year: ").strip()
        end_year = int(end_year_input) if end_year_input else start_year
    
    prepend_number = input("Enter a number to prepend to the word (leave empty to skip): ").strip()
    append_number = input("Enter a number to append to the word (leave empty to skip): ").strip()
    
    prepend_symbols = input("Should symbols be added at the beginning of the word (yes/no)? ").strip().lower() == 'yes'
    append_symbols = input("Should symbols be added at the end of the word (yes/no)? ").strip().lower() == 'yes'
    middle_symbols = input("Should symbols be added between the word and the number (yes/no)? ").strip().lower() == 'yes'

    # Generate the wordlist
    wordlist = generate_wordlist(base_word, prepend_number if prepend_number else None, append_number if append_number else None, prepend_symbols, append_symbols, middle_symbols, start_year, end_year, complex_mode)

    # Write the result to a file
    with open('generated_wordlist.txt', 'w') as f:
        for word in wordlist:
            f.write(word + '\n')

    print(f"Wordlist generated and saved to 'generated_wordlist.txt'. Total words: {len(wordlist)}")

if __name__ == "__main__":
    main()
