import pygame, sys
from pygame.locals import *
import random, time
import os
import csv
import pandas as pd
import subprocess
import datetime
import spwf
import sqlite3

count_file = 'Switch Count.txt'

if os.path.exists(count_file):
    with open(count_file, 'r') as f:
        count = int(f.read())
else:
    count = 0

count += 1

with open(count_file, 'w') as f:
    f.write(str(count))

python_path = sys.executable 


participant_number = spwf.participant_number

filename = os.path.join(spwf.folder_name, f"{participant_number} - Switching Score.csv")
filename2 = os.path.join(spwf.folder_name, f"{participant_number} - Switching Reaction Times.csv")
filename3 = os.path.join(spwf.folder_name, f"{participant_number} - Combined Reaction Times.csv")
filename4 = os.path.join(spwf.folder_name, f"{participant_number} - Combined Scores.csv")

sqlfile = os.path.join(spwf.folder_name, f"{participant_number} - Combined Scores.db")
con = sqlite3.connect(sqlfile)
cur = con.cursor()
#cur.execute("CREATE TABLE Participant(id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT)")
#cur.execute("CREATE TABLE Data(Date TEXT, Iteration INTEGER, Score TEXT, RT TEXT, Trial TEXT)")

now = datetime.datetime.now()

date_time_string = now.strftime("%d-%m-%y")
outputtime = now.strftime("%H:%M")
dir_path = os.path.dirname(os.path.realpath(__file__))

file_path = filename
file_path2 = filename2


def fileremoval():
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Skipping deletion.")

    try:
        os.remove(file_path2)
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Skipping deletion.")
    
if participant_number < 10:
    trialtype = 'Pilot'
else:
    trialtype = 'Experimental'

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h,
)

pygame.font.init()

FONT = pygame.font.Font(None, 100)

size = [SCREEN_WIDTH, SCREEN_HEIGHT - 50]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

screen.fill(WHITE)

pygame.display.set_caption("Task")


def intro():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    score = 0

    done = False
    start_time = pygame.time.get_ticks()


    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 32)

    display_instructions = True
    instruction_page = 1

    DISPLAYSURF = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
    )

    # DISPLAYSURF.fill(WHITE)

    order = 1

    Game_Running = True

    starterRT = time.time()

    while Game_Running:

        screen.fill(WHITE)

        if order == 4:
            ImageSample = pygame.image.load("Front_Right.png")
        if order == 1:
            ImageSample = pygame.image.load("Inverse_Back_Left.png")
        if order == 3:
            ImageSample = pygame.image.load("Front_Right.png")
        if order == 2:
            ImageSample = pygame.image.load("Back_Right.png")

        ImageSample_rect = ImageSample.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        )
        screen.blit(ImageSample, ImageSample_rect)

        text = font.render(
            "You will see a manikin holding a ball, the man can appear facing front, facing back, upright or upside-down.",
            True,
            BLACK,
        )
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 40))
        screen.blit(text, text_rect)

        text = font.render(
            "Use the key 'F' to indicate the ball is on the left hand, and key 'J' to indicate the ball is on the right hand",
            True,
            BLACK,
        )
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 120))
        screen.blit(text, text_rect)

        
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        # Subtract the elapsed time from 60 to get the remaining time
        duration = 60

        remaining_time = duration - elapsed_time
        if remaining_time < 0:
            remaining_time = 0

        # Create a text surface with the remaining time
        text2 = font.render(str(remaining_time), True, BLACK)
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 450))
        screen.blit(text2, text2_rect)


        incorrectinterval = pygame.image.load("redcross.png")
        incorrectintervaldimensions = incorrectinterval.get_rect(
            center=screen.get_rect().center
        )

        correctinterval = pygame.image.load("greentick.png")
        correctintervaldimensions = correctinterval.get_rect(
            center=screen.get_rect().center
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game_Running = False
            pygame.event.pump()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and order == 1:
                    endRT = time.time()
                    screen.fill(WHITE)
                    score += 1
                    screen.blit(correctinterval, correctintervaldimensions)
                    pygame.time.wait(1000)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    Game_Running = False

                else:  # if incorrect key was pressed
                    endRT = time.time()
                    screen.fill(WHITE)
                    screen.blit(incorrectinterval, incorrectintervaldimensions)
                    pygame.time.wait(1000)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    Game_Running = False

        pygame.display.update()
        pygame.time.delay(500)

def introR():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    score = 0
    start_time = pygame.time.get_ticks()


    # Loop until the user clicks the close button.
    done = False

    clock = pygame.time.Clock()

    # Starting position of the silhouette
    rect_x = 50
    rect_y = 50

    # Speed and direction of rectangle
    rect_change_x = 5
    rect_change_y = 5

    # font
    font = pygame.font.Font(None, 32)

    display_instructions = True
    instruction_page = 1

    DISPLAYSURF = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
    )

    # DISPLAYSURF.fill(WHITE)

    order = 2

    Game_Running = True

    starterRT = time.time()

    while Game_Running:
        # Set the screen background
        screen.fill(WHITE)

        if order == 1:
            ImageSample = pygame.image.load("Front_Right.png")

        if order == 2:
            ImageSample = pygame.image.load("Back_Right.png")

        ImageSample_rect = ImageSample.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        )
        screen.blit(ImageSample, ImageSample_rect)

        text = font.render(
            "You will see a mannequin holding a ball, the man can appear facing front, facing back, upright or upside-down.",
            True,
            BLACK,
        )
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 40))
        screen.blit(text, text_rect)

        text = font.render(
            "Use the key 'F' to indicate the ball is on the left hand, and key 'J' to indicate the ball is on the right hand",
            True,
            BLACK,
        )
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 120))
        screen.blit(text, text_rect)

        
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        # Subtract the elapsed time from 60 to get the remaining time
        duration = 60

        remaining_time = duration - elapsed_time
        if remaining_time < 0:
            remaining_time = 0

        # Create a text surface with the remaining time
        text2 = font.render(str(remaining_time), True, BLACK)
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 450))
        screen.blit(text2, text2_rect)
        screen.blit(text, text_rect)

        incorrectinterval = pygame.image.load("redcross.png")
        incorrectintervaldimensions = incorrectinterval.get_rect(
            center=screen.get_rect().center
        )

        correctinterval = pygame.image.load("greentick.png")
        correctintervaldimensions = correctinterval.get_rect(
            center=screen.get_rect().center
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game_Running = False
            pygame.event.pump()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j and order == 2:
                    endRT = time.time()
                    screen.fill(WHITE)
                    score += 1
                    screen.blit(correctinterval, correctintervaldimensions)
                    pygame.time.wait(1000)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    Game_Running = False

                else:
                    endRT = time.time()
                    screen.fill(WHITE)
                    screen.blit(incorrectinterval, incorrectintervaldimensions)
                    pygame.time.wait(1000)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    Game_Running = False

        pygame.display.update()
        pygame.time.delay(500)


def mathsintro():
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
    text = font.render(
        "You will see a simple maths problem, of two numbers.", True, BLACK
    )

    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    incorrectinterval = pygame.image.load("redcross.png")
    incorrectintervaldimensions = incorrectinterval.get_rect(
        center=screen.get_rect().center
    )

    correctinterval = pygame.image.load("greentick.png")
    correctintervaldimensions = correctinterval.get_rect(
        center=screen.get_rect().center
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:

                    screen.blit(correctinterval, correctintervaldimensions)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    running = False

                if event.key == pygame.K_j:

                    screen.blit(incorrectinterval, incorrectintervaldimensions)
                    pygame.display.update()
                    pygame.time.wait(2000)

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        # Subtract the elapsed time from 60 to get the remaining time
        duration = 60

        remaining_time = duration - elapsed_time
        if remaining_time < 0:
            remaining_time = 0

        # Create a text surface with the remaining time
        text2 = font.render(str(remaining_time), True, BLACK)
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))

        # Fill the screen with white
        screen.fill(WHITE)

        text2 = font.render(
            "You will see a simple maths problem, of two numbers.", True, BLACK
        )
        text2_rect = text2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 300))

        text12 = font.render(
            "This is an example: 5 + 9 = ? which would equal 14, requiring a 'J' key.",
            True,
            BLACK,
        )
        text12_rect = text12.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
        )

        text5 = font.render(
            "Use the key 'F' when the result is lower than 5 and the key 'J' when the result is higher than 5.",
            True,
            BLACK,
        )
        text5_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))

        text = font.render(
            "5 - 2 = ? would require which response? Practice now, press either the 'F' or 'J' key now'",
            True,
            BLACK,
        )
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        screen.blit(text2, text2_rect)
        screen.blit(text5, text5_rect)
        screen.blit(text, text_rect)
        screen.blit(text12, text12_rect)

        timerfont = pygame.font.Font(None, 50)
        text3 = timerfont.render(str(remaining_time), True, BLACK)
        text3_rect = text3.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 300))

        screen.blit(text3, text3_rect)

        pygame.display.update()

    pygame.time.wait(duration)

    pygame.display.update()


def show_welcome_screen():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    score = 0

    # font
    font = pygame.font.Font(None, 64)

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

    timeout = 5

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

global lowercount
global highercount
lowercount = 0
highercount = 0

def maths():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    score = 0
    global lowercount
    global highercount

    # font
    font = pygame.font.Font(None, 48)

    order = 1

    a = random.randint(1, 10)
    b = random.randint(1, 10)
    op = random.choice(["+", "-"])
    if op == "+":
        result = a + b
    else:
        result = a - b

    if result > 5:
        highercount += 1

    if result < 5:
        lowercount += 1

    Game_Running = True

    starterRT = time.time()

    while Game_Running:
        # Set the screen background
        screen.fill(WHITE)

        starterRT = time.time()

        # Generate random addition or subtraction problem


        # Display problem on the screen
        screen.fill(WHITE)
        problem_text = f" {a} {op} {b}?"
        text = font.render(problem_text, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 80))
        screen.blit(text, text_rect)
        pygame.display.update()

        # Get user input
        user_input = None
        while user_input not in ["f", "j"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        user_input = "f"
                    elif event.key == pygame.K_j:
                        user_input = "j"

        incorrectinterval = pygame.image.load("redcross.png")
        incorrectintervaldimensions = incorrectinterval.get_rect(
            center=screen.get_rect().center
        )

        correctinterval = pygame.image.load("greentick.png")
        correctintervaldimensions = correctinterval.get_rect(
            center=screen.get_rect().center
        )

        '''score_text = f"Score: {score}"
        text = font.render(score_text, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 400))
        screen.blit(text, text_rect)
        pygame.display.update()'''

        if (user_input == "f" and result < 5) or (user_input == "j" and result > 5):
            endRT = time.time()
            RT = endRT - starterRT
            screen.blit(correctinterval, correctintervaldimensions)
            pygame.display.update()
            pygame.time.wait(1000)
            score += 1
        else:
            endRT = time.time()
            RT = endRT - starterRT
            screen.blit(incorrectinterval, incorrectintervaldimensions)
            pygame.display.update()
            pygame.time.wait(1000)
            score = 0

        Game_Running = False

    pygame.display.update()
    screen.fill(WHITE)
    pygame.display.update()

    with open(str(participant_number) + " - N-Back Score Output.csv", mode="a+") as file:
        file.write(date_time_string + ',' + str(score))
        file.write("\n")

    with open(str(participant_number) + " - N-Back RT Output.csv", mode="a+") as file:
        file.write(date_time_string + ',' + str(RT))
        file.write("\n")

    with open(str(participant_number) + " - Combined Score Output.csv", mode="a+") as file:
        file.write(date_time_string + ',' + str(score) + ',' + str("Reaction Time"))
        file.write("\n")

    with open(str(participant_number) + " - Combined RT Output.csv", mode="a+") as file:
        file.write(date_time_string + ',' + str(RT) + ',' + str("Reaction Time"))
        file.write("\n")

global ballcount
global FL
global FR
global BL
global BR
global UFL
global UFR
global UBL
global UBR

FL = 0
FR = 0
BL = 0
BR = 0
UFL = 0
UFR = 0
UBL = 0
UBR = 0
ballcount = 0

def ball():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    global ballcount
    global FL
    global FR
    global BL
    global BR
    global UFL
    global UFR
    global UBL
    global UBR    


    
    score = 0

    # Loop until the user clicks the close button.
    done = False

    clock = pygame.time.Clock()

    # Starting position of the silhouette
    rect_x = 50
    rect_y = 50

    # Speed and direction of rectangle
    rect_change_x = 5
    rect_change_y = 5

    # font
    font = pygame.font.Font(None, 32)

    display_instructions = True
    instruction_page = 1

    DISPLAYSURF = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN
    )

    import random

    available_orders = []

    if UFR < 8:
        available_orders.append(1)
        available_orders.append(1)
        available_orders.append(1)
        available_orders.append(1)        

    if UFL < 8:
        available_orders.append(2)
        available_orders.append(2)
        available_orders.append(2)
        available_orders.append(2)

    if UBR < 8:
        available_orders.append(3)
        available_orders.append(3)
        available_orders.append(3)
        available_orders.append(3)


    if UBL < 8:
        available_orders.append(4)
        available_orders.append(4)
        available_orders.append(4)
        available_orders.append(4)


    if FR < 8:
        available_orders.append(5)
        available_orders.append(5)
        available_orders.append(5)
        available_orders.append(5)


    if FL < 8:
        available_orders.append(6)
        available_orders.append(6)
        available_orders.append(6)
        available_orders.append(6)


    if BR < 8:
        available_orders.append(7)
        available_orders.append(7)
        available_orders.append(7)
        available_orders.append(7)

    if BL < 8:
        available_orders.append(8)
        available_orders.append(8)
        available_orders.append(8)
        available_orders.append(8)
        

    print(available_orders)

    if available_orders:
        order = random.choice(available_orders)

        if order == 1:
            ImageSample = pygame.image.load("UFR.png")
            UFR += 1
        elif order == 2:
            ImageSample = pygame.image.load("UFL.png")
            UFL += 1
        elif order == 3:
            ImageSample = pygame.image.load("UBR.png")
            UBR += 1
        elif order == 4:
            ImageSample = pygame.image.load("UBL.png")
            UBL += 1
        elif order == 5:
            ImageSample = pygame.image.load("FR.png")
            FR += 1
        elif order == 6:
            ImageSample = pygame.image.load("FL.png")
            FL += 1
        elif order == 7:
            ImageSample = pygame.image.load("BR.png")
            BR += 1
        elif order == 8:
            ImageSample = pygame.image.load("BL.png")
            BL += 1

        if UFR > 8:
            available_orders.remove(1)

        if UFL > 8:
            available_orders.remove(2)

        if UBR > 8:
            available_orders.remove(3)

        if UBL > 8:
            available_orders.remove(4)

        if FR > 8:
            available_orders.remove(5)

        if FL > 8:
            available_orders.remove(6)

        if BR > 8:
            available_orders.remove(7)

        if BL > 8:
            available_orders.remove(8)

    else:
        ImageSample = pygame.Surface((0, 0))

    Game_Running = True

    starterRT = time.time()

    timeout = 3

    while Game_Running:

        timenow = time.time()
        
        screen.fill(WHITE)
        
        ImageSample_rect = ImageSample.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
        )
        screen.blit(ImageSample, ImageSample_rect)

        incorrectinterval = pygame.image.load("redcross.png")
        incorrectintervaldimensions = incorrectinterval.get_rect(
            center=screen.get_rect().center
        )

        correctinterval = pygame.image.load("greentick.png")
        correctintervaldimensions = correctinterval.get_rect(
            center=screen.get_rect().center
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game_Running = False
                
            pygame.event.pump()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and order in (2,4,6,8):
                    endRT = time.time()
                    RT = endRT - starterRT

                    screen.fill(WHITE)
                    score += 1
                    screen.blit(correctinterval, correctintervaldimensions)
                    pygame.time.wait(1000)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    Game_Running = False

                elif event.key == pygame.K_j and order in (1,3,5,7):
                    endRT = time.time()
                    RT = endRT - starterRT

                    screen.fill(WHITE)
                    score += 1
                    screen.blit(correctinterval, correctintervaldimensions)
                    pygame.time.wait(1000)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    Game_Running = False

                elif event.key == pygame.K_f and order in (1,3,5,7) or event.key == pygame.K_j and order in (2,4,6,8):
                    endRT = time.time()
                    RT = endRT - starterRT
                    screen.fill(WHITE)
                    screen.blit(incorrectinterval, incorrectintervaldimensions)
                    pygame.time.wait(1000)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    Game_Running = False

        overalltime = timenow - starterRT
        
        print(overalltime)

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
        
        pygame.display.update()
        pygame.time.delay(500)

    with open(filename, mode="a+") as file:
        file.write(f"{date_time_string}, {count}, {score}, Switching\n")

    with open(filename2, mode="a+") as file:
        file.write(f"{date_time_string}, {count}, {RT}, Switching\n")

    with open(filename4, mode="a+") as file:
        file.write(f"{date_time_string}, {count}, {score}, Switching\n")

    with open(filename3, mode="a+") as file:
        file.write(f"{date_time_string}, {count}, {RT}, Switching\n")

    insert = f"INSERT INTO Data (Date, Iteration, Score, RT, Trial) VALUES (?,?,?,?,?)"

    data = {
        "Date": date_time_string,
        "Iteration": count,
        "Score": score,
        "RT": RT,
        "Trial": "Switching"
        
    }

    datavalues = (data["Date"], data["Iteration"], data["Score"], data["RT"], data["Trial"])

    cur.execute(insert, datavalues)

    con.commit()


    ballcount += 1

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
    #print(formatted_num)


    totalscore = accuracydf.sum().values[0]

    #print(totalscore,counter)
    finalscore = totalscore / counter * 100
    #print("Percentage" , finalscore)

    formatted_acc = "{:.1f}".format(finalscore)
    #print(formatted_acc)
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

def trialorder():
    for i in range(0, 46):
        torder = random.randint(1, 2)
        if torder == 1:
            maths()
            print("Lower Count: ",lowercount)
            print("Higher Count: ",highercount)
            
        else:
            ball()

            print("Total Count ",ballcount)
            print("Front Left ", FL)
            print("Front Right ", FR)
            print("Back Left", BL)
            print("Back Right ",BR)
            print("Upside Front Left ",UFL)
            print("Upside Front Right ",UFR) 
            print("Upside Back Left ",UBL)
            print("Upside Back Right ", UBR)
            print("\n\n")


 
trialcounter = 0

fileremoval()
'''show_welcome_screen()
intro()
introR()
mathsintro()
intertrial()'''
trialorder()
exitscreen()
import Export
pygame.quit()
