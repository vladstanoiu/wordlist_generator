# birthdays - 8 numbers

# input first number
first_number = input("Enter a number: ")  # Se ia ca string

# check if  the first number has 10 chars
if len(first_number) != 8:
    print("First number needs to have 10 chars")
else:
    # last number
    last_number = '99999999'

    # open file
    with open("numbers.txt", "w") as file:
        # write file
        for number in range(int(first_number), int(last_number) + 1):
            # write every number in a new line
            file.write(f"{number:08}\n")  # Format to be 10 chars

    print("Wordlist generated in birthdays.txt")
