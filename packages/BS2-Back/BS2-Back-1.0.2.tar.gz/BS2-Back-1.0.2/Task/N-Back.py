import subprocess
import pygame
from pygame.locals import *
import random
import time
import os
import csv
import pandas as pd
from datetime import datetime
import spwf
import sqlite3

count_file = 'N-Back count.txt'

count = 0
if os.path.exists(count_file):
    with open(count_file, 'r') as f:
        count = int(f.read())
count += 1
with open(count_file, 'w') as f:
    f.write(str(count))

participant_number = spwf.participant_number
folder_name = spwf.folder_name

filename = os.path.join(folder_name, f"{participant_number} - N-Back Score.csv")
filename2 = os.path.join(folder_name, f"{participant_number} - N-Back Reaction Times.csv")
filename3 = os.path.join(folder_name, f"{participant_number} - Combined Reaction Times.csv")
filename4 = os.path.join(folder_name, f"{participant_number} - Combined Scores.csv")
sqlfile = os.path.join(spwf.folder_name, f"{participant_number} - Combined Scores.db")
con = sqlite3.connect(sqlfile)
cur = con.cursor()
#cur.execute("CREATE TABLE Participant(id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT)")
#cur.execute("CREATE TABLE Data(Date TEXT, Iteration INTEGER, Score TEXT, RT TEXT, Trial TEXT)")

now = datetime.now()
date_time_string = now.strftime("%d-%m-%y")
outputtime = now.strftime("%H:%M:%S")

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("N-Back Game")
pygame.font.init()
FONT_SIZE = 240
font = pygame.font.SysFont('Arial', FONT_SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
KEY_MAPPING = {pygame.K_j: True, pygame.K_f: False}

def show_welcome_screen():
    pygame.font.init()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    score = 0

    # font
    font = pygame.font.Font(None, 32)

    order = 1

    start_time = pygame.time.get_ticks()

    Game_Running = True

    starterRT = time.time()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(WHITE)
    pygame.display.set_caption("Welcome to the Task")
    font = pygame.font.Font(None, 60)
    text = font.render("Welcome to the Task", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)

    timeout = 3

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        # Subtract the elapsed time from 60 to get the remaining time
        remaining_time = timeout - elapsed_time
        if remaining_time < 0:
            running = False
            remaining_time = 0

        # Create a text surface with the remaining time
        text2 = font.render(str(remaining_time), True, BLACK)
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))

        # Fill the screen with white
        screen.fill(WHITE)

        text = font.render("Welcome to the Task!", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        screen.blit(text2, text2_rect)
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.update()

    pygame.display.update()

def instructions():
    pygame.font.init()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    score = 0

    # font
    font = pygame.font.Font(None, 32)

    order = 1

    start_time = pygame.time.get_ticks()

    Game_Running = True

    starterRT = time.time()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(WHITE)
    pygame.display.set_caption("Welcome to the Task")
    font = pygame.font.Font(None, 32)
    text = font.render("Welcome to the Task", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)

    timeout = 60

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        # Subtract the elapsed time from 60 to get the remaining time
        remaining_time = timeout - elapsed_time
        if remaining_time < 0:
            running = False
            remaining_time = 0

        # Create a text surface with the remaining time
        text2 = font.render(str(remaining_time), True, BLACK)
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 300))

        # Fill the screen with white
        screen.fill(WHITE)

        text = font.render("This task is called the N-Back", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-300))

        text11_surface = font.render("It is a cognitive task requiring that you dynamically recall a set of three numbers", True, BLACK)
        text11_rect = text11_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-200))

        text12_surface = font.render("If the third number presented is the same as the first, then press 'J'. If it is not, respond with 'F'.", True, BLACK)
        text12_rect = text12_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-100))

        textexample = font.render("In the example of: 2  4  3  , would this require an 'F' or 'J' response?", True, BLACK)
        textexample_rect = textexample.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        textexample1 = font.render("4", True, BLACK)
        textexample1_rect = text12_surface.get_rect(center=(SCREEN_WIDTH / 2.4, SCREEN_HEIGHT / 2))

        textexample2 = font.render("1", True, BLACK)
        textexample2_rect = text12_surface.get_rect(center=(SCREEN_WIDTH / 2.5, SCREEN_HEIGHT / 2))

        screen.blit(text2, text2_rect)
        screen.blit(text, text_rect)
        screen.blit(text11_surface, text11_rect)
        screen.blit(text12_surface, text12_rect)
        screen.blit(textexample, textexample_rect)
        correctinterval = pygame.image.load("greentick.png")
        correctintervaldimensions = correctinterval.get_rect(center=screen.get_rect().center) 

        incorrectinterval = pygame.image.load("redcross.png")
        incorrectintervaldimensions = incorrectinterval.get_rect(center=screen.get_rect().center)
        
        def right():
            screen.blit(incorrectinterval, incorrectintervaldimensions)
            pygame.time.wait(1000)
            pygame.display.update()
            pygame.time.wait(1000)

        def wrong():
            screen.blit(correctinterval, correctintervaldimensions)
            pygame.time.wait(1000)
            pygame.display.update()
            pygame.time.wait(1000)
            
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        #print("F key pressed")
                        wrong()
                        running=False
                    elif event.key == pygame.K_j:
                        #print("J key pressed")
                        right()
                        running=False
                

        pygame.display.update()

    pygame.display.update()
    
def generate_sequence(length):
    return [random.randint(0, 9) for _ in range(length)]

def play_n_back(n, length):
    sequence = generate_sequence(length)
    for i in range(n, length):
        if sequence[i] == sequence[i - n]:
            print(f"Match! Current digit is {sequence[i]}")
        else:
            print(f"No match. Current digit is {sequence[i]}")
        time.sleep(1)


def draw_text(text, position, color):
    """Draw text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

import pygame
import os
import time
from datetime import datetime
import random

def generate_sequence(length):
    sequence = []
    guaranteed_twobacks = random.sample(range(1, length-1), 2)
    for i in range(length):
        if i in guaranteed_twobacks:
            sequence.append(sequence[i-2]) 
        else:
            sequence.append(random.randint(0, 9))
    return sequence

def introduction():
    pygame.font.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    score = 0
    font = pygame.font.Font(None, 32)
    order = 1
    start_time = pygame.time.get_ticks()
    Game_Running = True
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(WHITE)
    pygame.display.set_caption("Welcome to the Task")
    font = pygame.font.Font(None, 60)
    text = font.render("Welcome to the Task", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
   # screen.blit(text, text_rect)

    correctinterval = pygame.image.load("greentick.png")
    correctintervaldimensions = correctinterval.get_rect(center=screen.get_rect().center) 

    incorrectinterval = pygame.image.load("redcross.png")
    incorrectintervaldimensions = incorrectinterval.get_rect(center=screen.get_rect().center)

    n = 2
    sequence_length = 50
    sequence = generate_sequence(sequence_length)
    current_index = n
    score = 0
    running = True

    def incorrect():
        endRT = time.time()
        screen.fill(WHITE)
        screen.blit(incorrectinterval, incorrectintervaldimensions)
        pygame.display.update()

    def correct():
        endRT = time.time()
        screen.fill(WHITE)
        screen.blit(correctinterval, correctintervaldimensions)
        pygame.display.update()

        score == 1

    while running:
        
        starterRT = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_MAPPING:
                    if sequence[current_index] == sequence[current_index - n]:
                        print("2-Back")
                        if KEY_MAPPING[event.key]:
                            #J - during N-Back
                            print("J - 2-Back")

                            correct()
                            
                        else:
                            #F
                            print("F - 2-Back")
                            incorrect()

                    else:
                        #F
                        if KEY_MAPPING[event.key]:
                            print("J - Non-2-Back")
                            incorrect()
                            
                        else:
                        #J
                            print("F - Non-2-Back")
                            correct()                         

        pygame.display.update()
        screen.fill(WHITE)
        pygame.time.wait(1000)
        screen.fill(WHITE)
        pygame.time.wait(2000)
        

        key_pressed = None
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key in KEY_MAPPING:
                key_pressed = event.key
                break

        if key_pressed is not None:
            if sequence[current_index] == sequence[current_index - n]:
                if KEY_MAPPING[key_pressed]:
                    incorrect()
                    score = 0
                else:
                    correct()
                    score = 1
            else:
                if KEY_MAPPING[key_pressed]:
                    incorrect()
                    score = 0
                else:
                    correct()
                    score = 1

            endRT = time.time()
            RT = (endRT - starterRT)
            overalltime = timenow - starterRT
            
            if overalltime > 3:
                Game_Running = False
                RT = overalltime
                DISPLAYSURF.fill(WHITE)
                pygame.time.wait(500)
                pygame.display.update()
                pygame.time.wait(500)
                end = time.time()
                score = 0
           
            # can bin off any triggers of 16, suggests missed trials
            
            break            

            with open(filename, mode="a+") as file:
                file.write(f"{date_time_string}, {count}, {score}, N-Back\n")

            with open(filename2, mode="a+") as file:
                file.write(f"{date_time_string}, {count}, {RT}, N-Back\n")

            with open(filename4, mode="a+") as file:
                file.write(f"{date_time_string}, {count}, {score}, N-Back\n")

            with open(filename3, mode="a+") as file:
                file.write(f"{date_time_string}, {count}, {RT}, N-Back\n")

            pygame.display.update()
        print(score)

        screen.fill(WHITE)

        draw_text(str(sequence[current_index]), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2), BLACK)
        print(sequence)
        pygame.time.wait(1000)
        now = datetime.now()
        pygame.display.update()

        outputtime = now.strftime("%H:%M:%S")

        current_index += 1
        if current_index >= sequence_length:
            running = False

    print(f'End of introduction')


def main():

    pygame.font.init()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    score = 0

    font = pygame.font.Font(None, 32)

    order = 1

    start_time = pygame.time.get_ticks()

    Game_Running = True

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(WHITE)
    pygame.display.set_caption("Welcome to the Task")
    font = pygame.font.Font(None, 60)
    text = font.render("Welcome to the Task", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    
    correctinterval = pygame.image.load("greentick.png")
    correctintervaldimensions = correctinterval.get_rect(center=screen.get_rect().center) 

    incorrectinterval = pygame.image.load("redcross.png")
    incorrectintervaldimensions = incorrectinterval.get_rect(center=screen.get_rect().center)# Set up the game
    n = 2
    sequence_length = 12
    sequence = generate_sequence(sequence_length)
    current_index = n
    score = 0
    running = True

    def incorrect():
        endRT = time.time()
        draw_text("Incorrect!", (WINDOW_SIZE[0] // 2, FONT_SIZE * 2), BLACK)
        screen.fill(WHITE)
        pygame.time.wait(1000)
        pygame.display.update()
        score = 0

    def correct():
        endRT = time.time()
        draw_text("Incorrect!", (WINDOW_SIZE[0] // 2, FONT_SIZE * 2), BLACK)
        screen.fill(WHITE)
        pygame.time.wait(1000)
        pygame.display.update()
        score = 1

    starterRT = time.time()
    while running:
        timenow = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_MAPPING:
                    if sequence[current_index] == sequence[current_index - n]:
                        print("2-Back")
                        if KEY_MAPPING[event.key]:
                            incorrect()

                        else:
                            correct()
       
                    else:
                        if KEY_MAPPING[event.key]:
                            correct()
              
                        else:
                            incorrect()

                        endRT = time.time()
                        RT = (endRT - starterRT)

                    print(f'Score: {score}')                                        
                    with open(filename, mode="a+") as file:
                        file.write(f"{date_time_string}, {count}, {score}, N-Back\n")

                    with open(filename2, mode="a+") as file:
                        file.write(f"{date_time_string}, {count}, {RT}, N-Back\n")

                    with open(filename4, mode="a+") as file:
                        file.write(f"{date_time_string}, {count}, {score}, N-Back\n")

                    with open(filename3, mode="a+") as file:
                        file.write(f"{date_time_string}, {count}, {RT}, N-Back\n")

                    insert = f"INSERT INTO Data (Date, Iteration, Score, RT, Trial) VALUES (?,?,?,?,?)"

                    data = {
                        "Date": date_time_string,
                        "Iteration": count,
                        "Score": score,
                        "RT": RT,
                        "Trial": "2-Back"
                        
                    }

                    datavalues = (data["Date"], data["Iteration"], data["Score"], data["RT"], data["Trial"])

                    cur.execute(insert, datavalues)

                    con.commit()

        screen.fill(WHITE)
        pygame.time.wait(1000)
        screen.fill(WHITE)
        pygame.display.update()
        pygame.time.wait(2000)

        draw_text(str(sequence[current_index]), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2), BLACK)
        now = datetime.now()

        outputtime = now.strftime("%H:%M:%S")

        pygame.display.update()

        current_index += 1
        if current_index >= sequence_length:
            running = False

    pygame.quit()

def intertrial():
    
    pygame.font.init()

    os.environ["SDL_VIDEO_CENTERED"] = "1"

    score = 0

    font = pygame.font.Font(None, 32)

    order = 1

    start_time = pygame.time.get_ticks()

    Game_Running = True

    starterRT = time.time()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    screen.fill(WHITE)
    pygame.display.set_caption("")
    font = pygame.font.Font(None, 60)
    intertext = "The actual task will start now"
    intertext2 = "Remember to be fast and accurate!"

    timeout = 3

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = timeout - elapsed_time
        if remaining_time < 0:
            running = False
            remaining_time = 0

        text4 = font.render(str(remaining_time), True, BLACK)
        text_rect4 = text4.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 300))
        screen.fill(WHITE)
        text = font.render(intertext, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        text3 = font.render(intertext2, True, BLACK)
        text_rect3 = text3.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2+100))

        screen.blit(text3, text_rect3)
        screen.blit(text, text_rect)
        screen.blit(text4, text_rect4)

        pygame.display.update()

    pygame.time.wait(500)
    pygame.display.update()

def exitscreen():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    df = pd.read_csv(filename2, usecols=[2], header=None)
    mean = df.mean().values[0]

    accuracydf = pd.read_csv(filename, usecols=[2], header=None)
    accuracydf = accuracydf.round(1)

    counter = accuracydf.count().values[0]
    formatted_num = "{:.2f}".format(mean)

    totalscore = accuracydf.sum().values[0]

    ##print(totalscore,counter)
    finalscore = totalscore / counter * 100
    ##print("Percentage" , finalscore)

    formatted_acc = "{:.1f}".format(finalscore)
    ##print(formatted_acc)
    # font
    font = pygame.font.Font(None, 32)

    DISPLAYSURF = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE
    )

    DISPLAYSURF.fill(WHITE)

    text = font.render("The task is now complete, thank you!", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
    screen.blit(text, text_rect)

    text = font.render(
        "Your average reaction time is: " + str(formatted_num) + " seconds", True, BLACK
    )
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)

    text = font.render(
        "Your combined accuracy rate is: " + str(formatted_acc) + "%", True, BLACK
    )
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    screen.blit(text, text_rect)

    pygame.display.update()
    # pygame.time.delay(500)
    pygame.time.delay(10000)

if __name__ == "__main__":
    
    '''show_welcome_screen()
    instructions()
    introduction()
    intertrial()'''
    main()
    exitscreen()
    subprocess.run([python_path, 'Export.py'], check=True)
    subprocess.run([python_path, 'Export.py'], check=True)
    sysexit()
