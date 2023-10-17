import subprocess
import random
import platform
import os
import sys
python_path = sys.executable
import spwf
import tkinter as tk
import time
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import filedialog
from tkinter import simpledialog, messagebox
import Location
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

location = Location.first_word
if location == 'ECHO':
    outputloc = 'Non-university Device'
elif location == 'uni.ds.port.ac.uk':
    outputloc = 'University Device'

print("Welcome to the task \n\n")
print(f'Connection: {outputloc}')

#print(python_path)
now = datetime.now()
date_time_string = now.strftime("%d-%m-%y")
outputtime = now.strftime("%H:%M")

participant_number = spwf.participant_number

depfile = os.path.join(spwf.folder_name, f"{participant_number} - Dependency Installation.txt")

dir_path = os.path.dirname(os.path.realpath(__file__))

filename = "participant number.txt"      

def startup():
    participant_number = spwf.participant_number
    folder_name = f'Participant {participant_number}'
    USERNAME = spwf.emailadd
    PASSWORD = spwf.password
    
    class ConsentForm:
        def __init__(self, master):
            self.master = master
            master.title("Consent Form")

            self.questions = ["I confirm that I have read and understood the information sheet dated TBD (version TBD) for the above study.", "I have had the opportunity to consider the information, ask questions and have answered these answered satisfactorily.",
                              "I understand that my participation is voluntary and that I am free to withdraw at any time without giving any reason. ",
                              "I understand that data collected during this study will be processed in accordance with data protection law as explained in the Participant Information Sheet (date and version of participant information sheet TBD).",
                              "I understand that the results of this study may be published and / or presented at meetings or academic conferences and may be provided to research commissioners or funders.", "I give my permission for my anonymous data, which does not identify me, to be disseminated in this way.",
                              "I understand that the tests / investigations are designed for the purposes of the research, and I will not receive any personal results relating to my health or well-being."]

            self.instructions = Label(master, text="Please read and tick each box to indicate your consent.", font=fontsize1)
            self.instructions.pack(fill='both', expand=False, pady=10)

            self.checkboxes = [IntVar() for _ in range(len(self.questions))]

            for i, question in enumerate(self.questions):
                checkbox_button = Checkbutton(master, text=question, variable=self.checkboxes[i])
                checkbox_button.pack(fill='both', expand=False, pady=10)


            self.name_label = Label(master, text="Please enter your name:")
            self.name_label.pack(fill='both', expand=False, )

            self.name_entry = Entry(master)
            self.name_entry.pack(expand=False)

            self.date_label = Label(master, text=f"Date: {datetime.now().strftime('%d/%m/%Y')}")
            self.date_label.pack(fill='both', expand=False, )

            self.submit_button = Button(master, text="Submit", command=self.submit_form)
            self.submit_button.pack(expand=False, pady=10)

        def submit_form(self):
            if all(c.get() == 1 for c in self.checkboxes) and self.name_entry.get() != "":
                # All checkboxes are ticked and name is entered
                self.export_answers()
                self.master.destroy()
                # Call your task function here
            else:
                # Not all checkboxes are ticked or name is not entered
                error_message = "Please ensure that all checkboxes are ticked and your name is entered."
                error_label = Label(self.master, text=error_message)
                error_label.pack(fill='both', expand=False, )

        def export_answers(self):
            filename = os.path.join(spwf.folder_name, f"{participant_number} - Consent.txt")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open(filename, "w") as f:
                f.write(f"Participant name: {self.name_entry.get()}\n \n")
                f.write(f"Date and time of consent: {dt_string}\n \n")
                for i, question in enumerate(self.questions):
                    f.write(f"{i+1}. {question}\n")
                    f.write(f"Answer: {'Yes' if self.checkboxes[i].get() == 1 else 'No'}\n \n")
            #print(f"Answers exported to {filename}")

    both_buttons_pressed = False

    dir_path = os.path.dirname(os.path.realpath(__file__))
    dependency_path = os.path.join(dir_path, "Dependency Installation.py")
    path = "Dependency Installation.py"
    filename = "participant number.txt"

    with open(os.path.join(dir_path, filename), "r") as f:
        first_line = f.readline()
        words = first_line.split()
        participant_number = None
        for word in words:
            if word.isdigit():
                participant_number = int(word)

    # create a variable to keep track of whether all buttons have been clicked
    global all_buttons_clicked
    all_buttons_clicked = False

    # modify the command for button2 to set all_buttons_clicked to True
    def emailsupport():
                    email_window = tk.Toplevel()
                    email_window.title("Compose Email")

                    # Email body input
                    body_label = tk.Label(email_window, text="Please describe your issue/query in as much detail as possible")
                    body_label.pack(fill='both', expand=False, side=tk.TOP, padx=5, pady=5)
                    body_text = tk.Text(email_window, wrap=tk.WORD)
                    body_text.pack(fill='both', expand=False, side=tk.TOP, padx=5, pady=5)

                    def send_email(body):
                        print("Send called")
                        # Create attachment object
                        sg = SendGridAPIClient(api_key=spwf.key)
                        message = Mail(
                            from_email=spwf.output,
                            to_emails=spwf.output,
                            subject=f'Email from Participant {spwf.participant_number}',
                            html_content=f'<strong>{body}</strong>'
                        )

                        try:
                            response = sg.send(message)
                            print(f"Email sent with status code: {response.status_code}")
                            email_window.destroy()
                            print("Email window closed")
                        except Exception as e:
                            print(e)
                        email_window.destroy()

                    submit_button = tk.Button(email_window, text="Send", command=lambda: send_email(body_text.get("1.0", tk.END)))
                    submit_button.pack(expand=False, side=tk.TOP, padx=5, pady=5)

    def pis2():
        file_path = "PIS.txt"
        if file_path:
            with open(file_path, "r") as f:
                text = f.read()
                root = tk.Tk()
                root.title("Participant Information Sheet")
                text_widget = tk.Text(root, wrap=tk.WORD)
                text_widget.insert(tk.END, text)
                text_widget.pack(fill='both', expand=False)
                close_button = tk.Button(root, text="Close", command=root.destroy)
                close_button.pack(fill='both', expand=False, side=tk.BOTTOM, pady = 10)
                global all_buttons_clicked
                all_buttons_clicked = True
    def pis():
        os.startfile("PIS.docx")

    def taskstart():
        global all_buttons_clicked
        if all_buttons_clicked == True:
            order = random.randint(1, 2)
            if order == 1:
                file_path = "Reaction Time Task - Copy.py"
            else:
                file_path = "N-Back.py"
            
            subprocess.run([python_path, "Trial.py"], check=True)
            import Export
        
    root = tk.Tk()
    fontsize = ("Helvetica", 16)
    fontsize1 = ("Helvetica", 18)
    fontsizesmall = ("Helvetica", 12)

    root.attributes("-fullscreen", True)
    root.attributes("-topmost", False)

    def exit_program():
        root.destroy()

    exit_button = tk.Button(root, text="Exit", command=exit_program, font=fontsizesmall)
    exit_button.pack(side="top", anchor="ne", padx=10, pady=5)

    ## Set window to full screen
    root.attributes('-fullscreen', True)

    time_label = tk.Label(root, text="", font=fontsize)

    # function to update the time label
    def update_time():
        current_time = time.strftime("%H:%M:%S")
        time_label.config(text=current_time)
        time_label.after(1000, update_time)  # update after 1 second

    # add the time label to the window
    time_label.pack(expand=False, side=tk.TOP, padx=5, pady=10, anchor="nw")
    
    loc_label = tk.Label(root, text="", font=fontsize)
    loc_label.config(text=outputloc)
    loc_label.pack(padx=5, pady=0, anchor="nw")

    # Create welcome label
    welcome_frame = tk.Frame(root)
    welcome_frame.pack(fill='both', expand=False, side=tk.TOP)

    welcome_label = tk.Label(welcome_frame, text="Welcome to the Task!", font=fontsize1)
    welcome_label.pack(expand=False, pady=0)

    text_frame = tk.Frame(root)
    text_frame.pack(fill='both', expand=False, side=tk.TOP)

    text_label = tk.Label(welcome_frame, text=f"Thank you for your interest in the study, your participant number is {participant_number}. \n \n \nBefore you participate, please thoroughly read the Participant Information Sheet and Consent Form. \n \n \n The information sheet and consent form will open as windows, click 'Close' when you are finished. \n \n \n If you experience any issues, or have any queries, please use the box in the bottom-left corner.", font=fontsize)
    text_label.pack(fill='both', expand=False, pady=30)

    # Create buttons and labels
    button1_frame = tk.Frame(root)
    button1_frame.pack(fill='both', expand=False, side=tk.TOP, padx=30, pady=20, anchor="nw")

    button2_frame = tk.Frame(root)
    button2_frame.pack(fill='both', expand=False, side=tk.TOP, padx=30, pady=20, anchor="nw")

    button2 = tk.Button(button2_frame, text="Participant Information Sheet", command=pis, font=fontsize)
    button2.pack(fill='both', expand=False, side=tk.LEFT)
    
    button3_frame = tk.Frame(root)
    button3_frame.pack(fill='both', expand=False, side=tk.TOP, padx=30, pady=10, anchor="nw")

    def consent():
        consent_window = tk.Toplevel(root)
        consent_window.title("Consent Form")
        consent_form = ConsentForm(consent_window)
        button3.config(command=lambda: consent_window.deiconify())
        consent_window.wait_window()

    button3 = tk.Button(button3_frame, text="Consent Form", command=consent, font=fontsize)
    button3.pack(expand=False, side=tk.LEFT)

    button12_frame = tk.Frame(root)
    button12_frame.pack(fill='both', expand=False, side=tk.TOP, padx=30, pady=10, anchor="nw")

    button12 = tk.Button(button12_frame, text="Email for assistance or queries", command=emailsupport, font=fontsize)
    button12.pack(fill='both', expand=False, side=tk.LEFT, pady=0)
    
    button4 = tk.Button(root, text="Start the Task", command=taskstart, font=fontsize)
    button4.pack(expand=False, side=tk.TOP, padx=0, pady=0, anchor="center")

    image_file = Image.open("uop.png")
    image = ImageTk.PhotoImage(image_file)
    image_label = tk.Label(root, image=image)
    image_label.place(relx=1, rely=0, anchor="ne", x=-20, y=40)
    update_time()   

    root.mainloop()

    root.quit()

startup()
