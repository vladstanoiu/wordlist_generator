# Complex wordlist generator
# written in python by Vlad Stanoiu

import itertools

def apply_replacements(word):
    """Applies all possible replacements for specified characters."""
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
    
    def generate_combinations(word):
        options = []
        for char in word:
            if char in replacements:
                options.append(replacements[char])
            else:
                options.append([char])
        return itertools.product(*options)
    
    return [''.join(comb) for comb in generate_combinations(word)]

def generate_wordlist(base_word, start_year, end_year, prepend_number, append_number, prepend_symbols, append_symbols, between_symbols):
    """Generates the wordlist according to the specifications."""
    wordlist_set = set()  # Use a set to avoid duplicates
    
    # Permutations of uppercase and lowercase letters
    permutations = itertools.product(*[c.lower() + c.upper() for c in base_word])
    base_word_variations = [''.join(perm) for perm in permutations]
    
    # Apply character replacements
    word_variations = []
    for word in base_word_variations:
        word_variations.extend(apply_replacements(word))
    
    # Add base word variations without numbers and symbols
    wordlist_set.update(word_variations)

    # Symbols
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

    def add_combinations(word, year=None):
        """Adds all possible combinations with symbols before, after, and between word and number/year."""
        combinations = set()

        # Base word
        combinations.add(word)
        
        # With prepend_number
        if prepend_number:
            combinations.add(f"{prepend_number}{word}")
            if append_number:
                combinations.add(f"{prepend_number}{word}{append_number}")
            if year:
                combinations.add(f"{prepend_number}{word}{year}")
        
        # With append_number
        if append_number:
            combinations.add(f"{word}{append_number}")
            if year:
                combinations.add(f"{word}{append_number}{year}")

        if year:
            combinations.add(f"{word}{year}")
        
        # Symbols and combinations
        if prepend_symbols:
            for symbol in symbols:
                # Symbol before word
                combinations.add(f"{symbol}{word}")
                if prepend_number:
                    combinations.add(f"{symbol}{prepend_number}{word}")
                if append_number:
                    combinations.add(f"{symbol}{word}{append_number}")
                if year:
                    combinations.add(f"{symbol}{word}{year}")
                
                # Symbol before word with append_number
                if append_number:
                    combinations.add(f"{symbol}{word}{append_number}")
                
                # Symbol before word with year
                if year:
                    combinations.add(f"{symbol}{word}{year}")
                
                # Symbol after word
                combinations.add(f"{word}{symbol}")
                if prepend_number:
                    combinations.add(f"{prepend_number}{word}{symbol}")
                if append_number:
                    combinations.add(f"{word}{append_number}{symbol}")
                if year:
                    combinations.add(f"{word}{year}{symbol}")
                
                # Symbol between word and append_number
                if between_symbols and append_number:
                    combinations.add(f"{word}{symbol}{append_number}")
                
                # Symbol between word and year
                if between_symbols and year:
                    combinations.add(f"{word}{symbol}{year}")
                
                # Symbol before and after word
                combinations.add(f"{symbol}{word}{symbol}")
                if prepend_number:
                    combinations.add(f"{symbol}{prepend_number}{word}{symbol}")
                if append_number:
                    combinations.add(f"{symbol}{word}{append_number}{symbol}")
                if year:
                    combinations.add(f"{symbol}{word}{year}{symbol}")
                
                # Symbol before word and between word and append_number
                if prepend_number and append_number and between_symbols:
                    combinations.add(f"{symbol}{prepend_number}{word}{symbol}{append_number}")
                
                # Symbol before word and between word and year
                if prepend_number and year and between_symbols:
                    combinations.add(f"{symbol}{prepend_number}{word}{symbol}{year}")

                # Symbol after word and between word and append_number
                if append_number and between_symbols:
                    combinations.add(f"{word}{symbol}{append_number}")

                # Symbol after word and between word and year
                if year and between_symbols:
                    combinations.add(f"{word}{symbol}{year}")

        # Handling append_symbols and between_symbols together
        if append_symbols and between_symbols:
            for symbol in symbols:
                combinations.add(f"{word}{symbol}{append_number}")
                if prepend_number:
                    combinations.add(f"{prepend_number}{word}{symbol}{append_number}")
                if year:
                    combinations.add(f"{word}{symbol}{year}")
                if prepend_number and year:
                    combinations.add(f"{prepend_number}{word}{symbol}{year}")

        return combinations

    # Adding variations with years, prepend_number, and append_number
    if start_year is not None and end_year is not None:
        for year in range(start_year, end_year + 1):
            for word in word_variations:
                wordlist_set.update(add_combinations(word, year))
    else:
        for word in word_variations:
            wordlist_set.update(add_combinations(word))

    return sorted(wordlist_set)

def main():
    # Ask for user input
    base_word = input("Enter the base word (e.g., test): ").strip()
    
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
    between_symbols = input("Should symbols be added between the word and the number (yes/no)? ").strip().lower() == 'yes'

    # Generate the wordlist
    wordlist = generate_wordlist(base_word, start_year, end_year, prepend_number if prepend_number else None, append_number if append_number else None, prepend_symbols, append_symbols, between_symbols)

    # Write the result to a file
    with open('generated_wordlist.txt', 'w') as f:
        for word in wordlist:
            f.write(word + '\n')

    print(f"Wordlist generated and saved to 'generated_wordlist.txt'. Total words: {len(wordlist)}")

if __name__ == "__main__":
    main()
