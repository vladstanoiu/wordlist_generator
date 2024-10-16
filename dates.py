# birthdays - 8 numbers

# input first number
first_number = input("Enter a number: ")  # take a string

# check if  the first number has 8 chars
if len(first_number) != 8:
    print("First number needs to have 8 chars")
else:
    # last number
    last_number = '99999999'

    # open file
    with open("birthdays.txt", "w") as file:
        # write file
        for number in range(int(first_number), int(last_number) + 1):
            # write every number in a new line
            file.write(f"{number:08}\n")  # Format to be 8 chars

    print("Wordlist generated in birthdays.txt")
