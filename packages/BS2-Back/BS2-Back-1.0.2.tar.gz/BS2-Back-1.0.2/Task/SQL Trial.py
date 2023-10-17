import sqlite3
import spwf

participant_number = spwf.participant_number  # Make sure to import or define spwf.participant_number correctly
filename = f'Participant {str(participant_number)}.db'
con = sqlite3.connect(filename)
cur = con.cursor()

name = input("Name: ")
age = input("Age: ")
email = input("Email: ")

#cur.execute('''CREATE TABLE Participant(id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT)''')

#cur.execute("DROP TABLE '{filename}'")

insert = f"INSERT INTO Participant (Name, Age, Email) VALUES (?,?,?)"

data = {
    "Name": name,
    "Age": age,
    "Email": email
}

datavalues = (data["Name"], data["Age"], data["Email"])

cur.execute(insert, datavalues)

con.commit()
