# Cerem primul număr de la utilizator
first_number = input("Enter a number: ")  # Se ia ca string

# Verificăm dacă primul număr are 10 cifre
if len(first_number) != 10:
    print("First number needs to have 10 chars")
else:
    # Ultimul număr este cel mai mare posibil cu același număr de cifre (10 cifre)
    last_number = '0799999999'

    # Deschidem fișierul numbers.txt în modul de scriere
    with open("numbers.txt", "w") as file:
        # Generăm numerele de la primul până la ultimul număr posibil
        for number in range(int(first_number), int(last_number) + 1):
            # Scriem fiecare număr pe o linie nouă în fișier
            file.write(f"{number:010}\n")  # Formatăm pentru a avea 10 cifre

    print("Wordlist generated in  numbers.txt")
