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
import glob


USERNAME = spwf.emailadd
PASSWORD = spwf.password

file_path = "Dependency Installation.py"

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

root = tk.Tk()
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

dimensions =(f'Dimensions: {screen_width} x {screen_height}')
position = screen_height // 25
runcount = 7
errortext = "We all have our favourites, but this task has been run too many times. \n\nPlease select another task to enjoy."

def emailsupport():
    email_window = tk.Toplevel()
    email_window.title("Compose Email")
    body_label = tk.Label(email_window, text="Please describe your issue/query in as much detail as possible")
    body_label.pack(fill='both', expand=False, side=tk.TOP, padx=5, pady=5)
    body_text = tk.Text(email_window, wrap=tk.WORD)
    body_text.pack(fill='both', expand=False, side=tk.TOP, padx=5, pady=5)

    def send_email(body):
        print("Send called")
        sg = SendGridAPIClient(api_key=spwf.key)
        message = Mail(
            from_email=spwf.output,
            to_emails=spwf.output,
            subject=f'Email from Participant {spwf.participant_number}',
            html_content=f'<strong>{body}</strong>'
        )

        try:
            response = sg.send(message)
            email_window.destroy()
        except Exception as e:
            print(e)
        email_window.destroy()

    submit_button = tk.Button(email_window, text="Send", command=lambda: send_email(body_text.get("1.0", tk.END)))
    submit_button.pack(expand=False, side=tk.TOP, padx=5, pady=5)

def pis():
    if scount > runcount:
        messagebox.showerror("Error", errortext)
    else:
        file_path = "Switching.py"
        subprocess.run([python_path, file_path], check=True)
        subprocess.run([python_path, 'Export.py'], check=True)            

fontsize = ("Helvetica", 18)
fontsize1 = ("Helvetica", 22)
fontsize2 = ("Helvetica", 12)

root.attributes('-fullscreen', True)

time_label = tk.Label(root, text="", font=fontsize)

def update_time():
    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=current_time)
    time_label.after(1000, update_time)
    
time_label.pack(side=tk.TOP, padx=20, pady=10, anchor="nw")

welcome_frame = tk.Frame(root)
welcome_frame.pack(side=tk.TOP, fill=tk.X)

welcome_label = tk.Label(welcome_frame, text="Welcome to the task menu", font=fontsize1)
welcome_label.pack(pady=position)

text_frame = tk.Frame(root)
text_frame.pack(side=tk.TOP, fill=tk.X)

text_label = tk.Label(welcome_frame, text=f"Please now select a task to perform", font=fontsize)
text_label.pack(pady=position)

nback_frame = tk.Frame(root)
nback_frame.pack(side=tk.TOP, padx=30, pady=5, anchor="center")

def nbrun():

    if nbcount > runcount:
        messagebox.showerror("Error", errortext)
        subprocess.run([python_path, 'Export.py'], check=True)
    else:
        file_path = "N-Back.py"
        subprocess.run([python_path, file_path], check=True)
        subprocess.run([python_path, 'Export.py'], check=True)
    
nback = tk.Button(nback_frame, text="2-Back", command=nbrun, font=fontsize, anchor="center")
nback.pack(side=tk.TOP, pady=5)

if nbcount == 1:
    text = f"You have completed this {nbcount} time so far"
else:
    text = f"You have completed this {nbcount} times so far"
nback_label = tk.Label(nback_frame, text=text, font=fontsize2)
nback_label.pack(side=tk.TOP, pady=5, anchor='center')


button1_frame = tk.Frame(root)
button1_frame.pack(side=tk.TOP, padx=30, pady=5, anchor="center")

button2_frame = tk.Frame(root)
button2_frame.pack(side=tk.TOP, padx=30, pady=5, anchor="center")

button2 = tk.Button(button2_frame, text="Switching Task", command=pis, font=fontsize, anchor="center")
button2.pack(side=tk.TOP, pady=5)

if scount == 1:
    text = f"You have completed this {scount} time so far"
else:
    text = f"You have completed this {scount} times so far"
button2_label = tk.Label(button2_frame, text=text, font=fontsize2)
button2_label.pack(side=tk.TOP, pady=5)

def consent():

    if rtcount > runcount:
        messagebox.showerror("Error", errortext)
        subprocess.run([python_path, 'Export.py'], check=True)
    else:
        file_path = "Reaction Time Task - Copy.py"
        subprocess.run([python_path, file_path], check=True)
        subprocess.run([python_path, 'Export.py'], check=True)

button3_frame = tk.Frame(root)
button3_frame.pack(side=tk.TOP, padx=30, pady=10, anchor="center")
button3 = tk.Button(button3_frame, text="2-Choice Reaction Time", command=consent, font=fontsize, anchor="center")
button3.pack(side=tk.TOP, pady=5)

if rtcount == 1:
    text = f"You have completed this {rtcount} time so far"
else:
    text = f"You have completed this {rtcount} times so far"
button3_label = tk.Label(button3_frame, text=text, font=fontsize2)
button3_label.pack(side=tk.TOP, pady=5, anchor='center')

button12_frame = tk.Frame(root)
button12_frame.pack(side=tk.BOTTOM, padx=30, pady=20, anchor="sw")

button12 = tk.Button(button12_frame, text="Email for assistance or queries", command=emailsupport, font=fontsize)
button12.pack(side=tk.LEFT, pady=10)

image_file = Image.open("uop.png")
image2 = ImageTk.PhotoImage(image_file)
image_label = tk.Label(root, image=image2)
image_label.place(relx=1, rely=0, anchor="ne", x=-20, y=20)
update_time()   

root.mainloop()            

root.quit()

subprocess.run([python_path, 'Export.py'], check=True)
