# Open the file
with open("Suffix.txt", "r") as f:
    # Read the first line and split it into words
    first_line_words = f.readline().split()
    # Get the first word
    first_word = first_line_words[0]

    if first_word == 'uni.ds.port.ac.uk':
        loc = ("Connected from a University device")

    else:
        loc =("Connected from a non-University device")
