from cryptography.fernet import Fernet

with open('spwfoutput.txt', 'rb') as f:
    key = f.read()

fernet = Fernet(key)

with open('spwfvalue.txt', 'rb') as f:
    encrypted_password = f.read()

password = fernet.decrypt(encrypted_password)

password = password.decode()

gituser = "benstocker07@gmail.com"
gitpass = "Boeing20201-"

emailadd = "up849864@myport.ac.uk"
output = "up849864@myport.ac.uk"

filename = "participant number.txt"

with open(filename, "r") as f:
    first_line = f.readline()
    words = first_line.split()
    participant_number = None
    for word in words:
        if word.isdigit():
            participant_number = int(word)

folder_name = f'Participant {participant_number}'
