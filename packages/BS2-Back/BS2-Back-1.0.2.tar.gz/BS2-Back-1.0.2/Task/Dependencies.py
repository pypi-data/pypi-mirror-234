import subprocess
import platform
from datetime import datetime
import sys
import os

python_path = sys.executable
#print("\n\nChecking that Python is installed...")
#print(f'\n\nPath to Python: {python_path}')
now = datetime.now()
date_time_string = now.strftime("%d-%m-%y")
outputtime = now.strftime("%H:%M:%S")

filename = "participant number.txt"

with open(filename, "r") as f:
    first_line = f.readline()
    words = first_line.split()
    participant_number = None
    for word in words:
        if word.isdigit():
            participant_number = int(word)

folder_name = f'Participant {participant_number}'

import Export

from plyer import notification

notification.notify(
    title='Task Beginning',
    message='The task is now starting, it may take a short while to load and install all of the relevant files',
    app_name='My Python App',
    timeout=10,
)
