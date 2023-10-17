import tkinter as tk
import spwf
import sys
import Location
import subprocess
pythonpath = sys.executable
python_path = pythonpath
import random
import platform
import tkinter as tk
import time
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import filedialog
from tkinter import simpledialog, messagebox

participant_number = spwf.participant_number

RTcount = "RT count.txt"

with open(RTcount, "r") as f:
    first_line = f.readline()
    words = first_line.split()
    rtcount = None
    for word in words:
        if word.isdigit():
            rtcount = int(word)
            
NBcount = "N-Back count.txt"

with open(NBcount, "r") as f:
    first_line = f.readline()
    words = first_line.split()
    nbcount = None
    for word in words:
        if word.isdigit():
            nbcount = int(word)

switchcount = "Switch count.txt"

with open(switchcount, "r") as f:
    first_line = f.readline()
    words = first_line.split()
    scount = None
    for word in words:
        if word.isdigit():
            scount = int(word)

limit = 7

if int(rtcount) > 7:
    print("Reaction Time Task is over the limit")
    import pandas as pd

    df = pd.read_csv(f'Participant {participant_number}/{participant_number} - Combined Reaction Times.csv')
   # print(df.groupby('RT')['Trial Type'].mean())
    column_4 = df.iloc[:, 3]
    trial_type = '1'
    filtered_df = df[df['Trial Type'] == trial_type]
    average_per_iteration = filtered_df.groupby('RT')['Trial Type'].mean()
    print(average_per_iteration)

    iteration = 18 # Replace with the specific iteration you want to analyze

    mean_rt = filtered_df['RT'].mean()  # Mean RT for the specified trial type and iteration

    previous_iteration = iteration - 1
    print(previous_iteration)
    previous_filtered_df = df[(df['Trial Type'] == trial_type) & (df['RT'] == previous_iteration)]
    previous_mean_rt = previous_filtered_df['RT'].mean()  # Mean RT for the previous iteration
    print(previous_filtered_df)
    print(previous_mean_rt)

    percentage_difference = (mean_rt - previous_mean_rt) / previous_mean_rt * 100

    # Print the percentage difference in RT
    print(f"Percentage difference in RT for iteration {iteration}: {percentage_difference}%")


if int(nbcount) > 7:
    print("2-Back is over the limit")
if int(scount) > 7:
    print("Switching Task is over the limit")
