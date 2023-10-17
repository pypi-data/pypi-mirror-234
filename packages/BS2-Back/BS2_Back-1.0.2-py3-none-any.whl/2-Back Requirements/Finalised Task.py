import subprocess
import pygame, sys, math
from pygame.locals import *
import random, time
import os
import csv
import pandas as pd
from datetime import datetime
import spwf
import sqlite3
#import cdtest
    
#dev = #cdtest.dev
    
def checkstim():

    try:
        global stimtracker_connected
        stimtracker_connected = True

        if stimtracker_connected:
            print("StimTracker is connected")
            #cdtest.stimtest()
            
    except Exception as e:
        import tkinter as tk
        errortext = f"The StimTracker is not connected.\n\nCheck Stim2 for verification of connection to Cedrus\n\nError message:\n\n{e}\n\n\n\nPS I hope you enjoy my error messages;)"

        from tkinter import simpledialog, messagebox

        messagebox.showerror("Error", errortext)
        sys.exit()

checkstim()

stimtracker_connected = False

def test_init():
    print("Initialisation")
    #cdtest.test1()
    
def test_pre():
    print("Pre-Init")
    #cdtest.test1()        


def test_end():
    print("Removal")
    #cdtest.test2()

db_filename = "N-Back.db"

db_connection = sqlite3.connect(db_filename)
db_cursor = db_connection.cursor()

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scores (
        timestamp TEXT,
        participant_number TEXT,
        counter INT,
        score INT,
        task_type TEXT,
        NoResponse TEXT,
        key TEXT
    )
''')

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS ReactionTimes (
        timestamp TEXT,
        participant_number TEXT,
        counter INT,
        reaction_time REAL,
        task_type TEXT,
        NoResponse TEXT,
        key TEXT
    )
''')

db_filename = "N-Back.db"

db_connection = sqlite3.connect(db_filename)
db_cursor = db_connection.cursor()

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scores (
        timestamp TEXT,
        participant_number TEXT,
        counter INT, 
        score INT,
        task_type TEXT,
        NoResponse TEXT,
        key TEXT
    )
''')

db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS ReactionTimes (
        timestamp TEXT,
        participant_number TEXT,
        counter INT,
        reaction_time REAL,
        task_type TEXT
        NoResponse TEXT,
        key TEXT
    )
''')


count_file = 'N-Back count.txt'

if os.path.exists(count_file):
    with open(count_file, 'r') as f:
        count = int(f.read())
else:
    count = 0

count += 1

with open(count_file, 'w') as f:
    f.write(str(count))

def login():
    global participant_number
    while True:
        participant_number = input("\nParticipant Number: ")
        p2 = input(f'Check participant number: {participant_number}. Re-enter participant number: ')
        if p2 == participant_number:
            print("\nCorrect")
            break
        else:
            print("\nIncorrect match of participant number. Re-check the number.\n")

login()

folder_name = f'Participant {participant_number}'

try:
    os.mkdir(folder_name)
    #print(f"Created folder '{folder_name}'")

except FileExistsError:
    print("")

filename = os.path.join(folder_name, f"{participant_number} - N-Back Score.csv")
filename2 = os.path.join(folder_name,  f"{participant_number} - N-Back Reaction Times.csv")
filename3 = os.path.join(folder_name, f"{participant_number} - Combined Reaction Times.csv")
filename4 = os.path.join(folder_name, f"{participant_number} - Combined Scores.csv")

now = datetime.now()

date_time_string = now.strftime("%d-%m-%y")
outputtime = now.strftime("%H:%M:%S")

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h,
)

WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
pygame.display.set_caption("N-Back Game")

pygame.font.init()
FONT_SIZE = 240
font = pygame.font.SysFont('Arial', FONT_SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

KEY_MAPPING = {
    pygame.K_j: True,
    pygame.K_f: False
}

def generate_sequence(length):
    return [random.randint(0, 9) for _ in range(length)]

def play_n_back(n, length):
    sequence = generate_sequence(length)
    #print(f"Sequence: {sequence}")
    #print(f"Starting n-back game with n={n}...")
    for i in range(n, length):
        if sequence[i] == sequence[i - n]:
            print(f"Match! Current digit is {sequence[i]}")
        else:
            print(f"No match. Current digit is {sequence[i]}")
        time.sleep(1)

def tester():
    if pygame.KEYDOWN:
        print(pygame.key.name)
        #cdtest.test()

    pygame.time.wait(2000)


def draw_text(text, position, color):
    """Draw text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)

def introduction():

    skip = None
    pygame.font.init()

    os.environ["SDL_VIDEO_CENTERED"] = "1"


    # font
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

    def nbacktrue():
        text = font.render("Welcome to the Task", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text, text_rect)

    
    correctinterval = pygame.image.load("greentick.png")
    correctintervaldimensions = correctinterval.get_rect(center=screen.get_rect().center) 

    incorrectinterval = pygame.image.load("redcross.png")
    incorrectintervaldimensions = incorrectinterval.get_rect(center=screen.get_rect().center)# Set up the game
    def generate_sequence(length):

        
        nbackno = math.ceil(sequence_length / 3)
        #print(f'Number of N-Backs: {nbackno}')

        sequence = [random.randint(1, 9) for _ in range(length)]
        for _ in range(nbackno):
            index = random.randint(n, length - 1)
            sequence[index] = sequence[index - n]

        return sequence

        db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS Configuration (
            NBacks VAR(255),
            SequenceLength VAR(255)
        )
    ''')

        db_cursor.execute(
        "INSERT INTO Configuration (NBacks, SequenceLength) VALUES (?, ?)",
        (nbackno, sequence_length)
    )

        #print(f'SQL Data: N-Back Number: {nbackno}, Sequence Length: {sequence_length}')    

    n = 2  
    sequence_length = 100
    sequence = generate_sequence(sequence_length)
    #print(sequence)

    current_index = 0
    score = 0
    running = True

    def incorrect():
        incorrectanswer = True
        endRT = time.time()
        screen.fill(WHITE)
        screen.blit(incorrectinterval, incorrectintervaldimensions)
        pygame.time.wait(500)
        pygame.display.update()
        pygame.time.wait(500)
        #print("Scored incorrectly")


    def correct():
        #cdtest.linetest()
        correctanswer = True
        endRT = time.time()
        screen.fill(WHITE)
        screen.blit(correctinterval, correctintervaldimensions)
        pygame.time.wait(500)
        pygame.display.update()
        pygame.time.wait(500)
        score =+ 1

            
    global timer2
    
    timer2 = time.time()

    stim = True

    while running:        
        
        starterRT = time.time()

        keypress = None  

        elapsed = starterRT - timer2

        timer2 = time.time()

        endRT = time.time()
        RT = (endRT - starterRT)

        pygame.time.wait(1000)
        
        #too_slow()

        screen.fill(WHITE)
        pygame.display.update()
        pygame.time.wait(500)
        #cdtest.test1()

        draw_text(str(sequence[current_index]), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2), BLACK)

        starting = pygame.time.get_ticks()

        
        pygame.display.update()
        
        screen.fill(WHITE)

        keyprocessed = False

        score = 0
        
        while True:

            currenttime = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not keyprocessed:
                    key_name = pygame.key.name(event.key)
                    print(f"{key_name} pressed")
                                                    
                    if event.key in KEY_MAPPING:
                        
                        keypress = True
                        keyprocessed = True

                        reactiontime = currenttime - starting

                        if keyprocessed == True:
                            print(f'RT (ms): {reactiontime}')
                            
                        
                        if sequence[current_index] == sequence[current_index - n]:
                            if event.key == pygame.K_j:
                                #cdtest.j()

                                correct()
                                score += 1

                            elif event.key == pygame.K_f:
                                #cdtest.f()

                                incorrect()
               
                        else:
                            if event.key == pygame.K_j:
                                #cdtest.j()

                                incorrect()
                      
                            elif event.key == pygame.K_f:
                                #cdtest.f()

                                correct()
                                score += 1
                
            if currenttime - starting >= 2000:
                if keyprocessed == False:
                    reactiontime = 0
                #cdtest.test()
                screen.fill(WHITE)
                pygame.display.update()

        
                def emptyscorerecord():
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO Scores (timestamp, participant_number, counter, score, task_type, NoResponse) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, "0", "N-Back", "No Response")
                        )
                        
                def emptyrtrecord():
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO ReactionTimes (timestamp, participant_number, counter, reaction_time, task_type, NoResponse) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, "0", "N-Back", "No Response")
                        )
                        
                with open(filename2, mode="a+") as file:
                    file.write(f"{date_time_string}, {count}, {reactiontime}, N-Back\n")

                with open(filename3, mode="a+") as file:
                    file.write(f"{date_time_string}, {count}, {reactiontime}, N-Back\n")
                    db_connection.commit()

                with open(filename, mode="a+") as file:
                    file.write(f"{date_time_string}, {count}, {score}, N-Back\n")
                    
                with open(filename4, mode="a+") as file:
                    file.write(f"{date_time_string}, {count}, {score}, N-Back\n")

                def scorerecord():
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO Scores (timestamp, participant_number, counter, score, task_type, key) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, score, "N-Back", key_name)


                            )
                def rtrecord():
                    with db_connection:
                        db_cursor.execute(
                            "INSERT INTO ReactionTimes (timestamp, participant_number, counter, reaction_time, task_type, key) VALUES (?, ?, ?, ?, ?, ?)",
                            (date_time_string, participant_number, count, reactiontime, "N-Back", key_name)
                            )
                if keyprocessed == True:
                    rtrecord()
                    scorerecord()

                else:
                    emptyrtrecord()
                    emptyscorerecord()

                break

        if sequence[current_index] == sequence[current_index - n]:
            print("\n\nN-Back\n\n")
            nbacktrue()

        current_index += 1
        if current_index >= sequence_length:
            running = False

        now = datetime.now()

        
    pygame.quit()
    
introduction()
