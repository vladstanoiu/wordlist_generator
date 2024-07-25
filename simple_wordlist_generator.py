# Simple wordlist generator
# written in python by Vlad Stanoiu

import itertools

def generate_wordlist(base_word, start_year, end_year, prepend_number, append_number, prepend_symbols, append_symbols, between_symbols):
    """Generates the wordlist according to the specifications."""
    wordlist_set = set()  # Use a set to avoid duplicates
    
    # Permutations of uppercase and lowercase letters
    permutations = itertools.product(*[c.lower() + c.upper() for c in base_word])
    base_word_variations = [''.join(perm) for perm in permutations]
    
    # Add simple words without numbers and symbols
    wordlist_set.update(base_word_variations)

    # Symbols and years
    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
    
    def add_combinations(word, prepend_symbols, append_symbols, between_symbols, year):
        """Adds all possible combinations with symbols before, after, and between word and number."""
        combinations = [word]
        
        if prepend_symbols:
            for symbol in symbols:
                combinations.append(f"{symbol}{word}")
        
        if append_symbols and year is not None:
            temp_combinations = []
            for comb in combinations:
                for symbol in symbols:
                    temp_combinations.append(f"{comb}{year}{symbol}")
            combinations = temp_combinations
        elif year is not None:
            combinations = [f"{comb}{year}" for comb in combinations]
        
        if between_symbols and year is not None:
            temp_combinations = []
            for comb in combinations:
                for symbol in symbols:
                    temp_combinations.append(f"{comb[:-len(str(year))]}{symbol}{year}")
            combinations.extend(temp_combinations)
        
        return combinations

    # Adding years and symbol options
    if start_year is not None and end_year is not None:
        for year in range(start_year, end_year + 1):
            for word in base_word_variations:
                # Version with number at the beginning and/or end
                if prepend_number:
                    wordlist_set.update(add_combinations(f"{prepend_number}{word}", prepend_symbols, append_symbols, between_symbols, year))
                
                if append_number:
                    wordlist_set.update(add_combinations(f"{word}{append_number}", prepend_symbols, append_symbols, between_symbols, year))
                
                if between_symbols:
                    wordlist_set.update(add_combinations(f"{word}", prepend_symbols, append_symbols, between_symbols, year))
                
                # Word with year and without number
                wordlist_set.update(add_combinations(word, prepend_symbols, append_symbols, between_symbols, year))

    elif start_year is not None:
        # If the year range is not specified, add the word without numbers
        for word in base_word_variations:
            if prepend_number:
                wordlist_set.update(add_combinations(f"{prepend_number}{word}", prepend_symbols, append_symbols, between_symbols, None))
            if append_number:
                wordlist_set.update(add_combinations(f"{word}{append_number}", prepend_symbols, append_symbols, between_symbols, None))
            wordlist_set.update(add_combinations(word, prepend_symbols, append_symbols, between_symbols, None))
    else:
        # If no years are specified and no numbers are added, add the base word
        for word in base_word_variations:
            wordlist_set.update(add_combinations(word, prepend_symbols, append_symbols, between_symbols, None))

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
