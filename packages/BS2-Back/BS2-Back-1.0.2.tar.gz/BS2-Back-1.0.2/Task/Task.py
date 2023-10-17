import socket
import tkinter
import tkinter as tk
import os

def is_connected():
    websites = ['www.google.com', 'www.facebook.com']
    for website in websites:
        try:
            socket.create_connection((website, 80))
            return True
        except OSError:
            pass
    return False

if is_connected():

    Connected = True

    if os.path.exists("participant number.txt"):
        pathnum = True
        
    else:
        
        import tkinter as tk
        import csv
        from tkinter import simpledialog, messagebox
        import os

        class PinSystem:
            def __init__(self, master):
                self.master = master
                self.master.title("PIN Entry")

                screen_width = self.master.winfo_screenwidth()
                screen_height = self.master.winfo_screenheight()

                x = int((screen_width/2) - (600/2))
                y = int((screen_height/2) - (150/2))

                self.master.geometry("600x150+{}+{}".format(x, y))
                
                self.pin_label = tk.Label(self.master, text="Welcome to the task\n\nTo begin, please enter your PIN. This will have been sent to you via email.\n\nEnter your PIN:")
                self.pin_label.pack()
                
                self.pin_entry = tk.Entry(self.master)
                self.pin_entry.pack()
                
                self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_pin)
                self.submit_button.pack(pady=15)
                
                self.pins = {}
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, "pins.csv")
                with open(csv_path) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        self.pins[row[0]] = row[1]
                
            def submit_pin(self):
                pin = self.pin_entry.get()

                if pin in self.pins:
                    participant_num = self.pins[pin]
                    message = f"Correct PIN\n\nYour participant number is {participant_num}.\n\nThe task will now load"
                    with open("participant number.txt", "w") as outfile:
                        outfile.write(participant_num)
                        self.master.destroy() 
                else:
                    message = "Invalid PIN."

                tk.messagebox.showinfo("Result", message)                

        if __name__ == "__main__":

            root = tk.Tk()
            PinSystem(root)
            root.mainloop()
            root.quit()

    import spwf

    print(f'Welcome to the task! Thank you for your interest in the study.\n\nYou are participant number {spwf.participant_number}.\n\nThe task is now loading, it may take a short while to load.')

    import subprocess
    import sys

    pythonpath = sys.executable
    python_path = pythonpath
    os.environ["PATH"] += os.pathsep + python_path

    filename = "participant number.txt"

    with open(filename, "r") as f:
        first_line = f.readline()
        words = first_line.split()
        participant_number = None
        for word in words:
            if word.isdigit():
                participant_number = int(word)
    folder_name = f'Participant {participant_number}'

    try:
        os.mkdir(folder_name)
        print(f"Created folder '{folder_name}'")

    except FileExistsError:
        print("")
    result = subprocess.run(['Suffix.bat'], capture_output=True, text=True)#,creationflags=subprocess.CREATE_NO_WINDOW)
    import Location
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
                
    import spwf
    
    def main():


        import subprocess
        import random
        import platform
        import os
        import sys
        python_path = sys.executable
        
        import spwf
        import tkinter as tk
        import time
        from PIL import Image, ImageTk
        from datetime import datetime
        from tkinter import filedialog
        from tkinter import simpledialog, messagebox
        import Location
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition


        root = tk.Tk()
        screen_height = root.winfo_screenheight()
        screen_width = root.winfo_screenwidth()
        
        dimensions =(f'Dimensions: {screen_width} x {screen_height}')
        position = screen_height // 25
        runcount = 10
        errortext = "We all have our favourites, but this task has been run too many times. \n\nPlease select another task to enjoy."
        
        if glob.glob(folder_name + '/*Consent.txt'):

            USERNAME = spwf.emailadd
            PASSWORD = spwf.password
            
            def emailsupport():
                email_window = tk.Toplevel()
                email_window.title("Compose Email")
                body_label = tk.Label(email_window, text="Please describe your issue/query in as much detail as possible")
                body_label.pack(fill='both', expand=False, side=tk.TOP, padx=5, pady=5)
                body_text = tk.Text(email_window, wrap=tk.WORD)
                body_text.pack(fill='both', expand=False, side=tk.TOP, padx=5, pady=5)

                def send_email(body):
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
                        with open(folder_name + '/Email Errors.txt') as emailerror:
                           emailerrorr.write(e) 
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
            fontsizesmall = ("Helvetica", 12)

            root.attributes("-fullscreen", True)
            root.attributes("-topmost", False)

            def exit_program():
                root.destroy()

            exit_button = tk.Button(root, text="Exit", command=exit_program, font=fontsizesmall)
            exit_button.pack(side="top", anchor="ne", padx=10, pady=5)

            time_label = tk.Label(root, text="", font=fontsize)

            def update_time():
                current_time = time.strftime("%H:%M:%S")
                time_label.config(text=current_time)
                time_label.after(1000, update_time)
                
            time_label.pack(side=tk.TOP, padx=20, pady=0, anchor="nw")

            welcome_frame = tk.Frame(root)
            welcome_frame.pack(side=tk.TOP, fill=tk.X)

            welcome_label = tk.Label(welcome_frame, text="Welcome back!", font=fontsize1)
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
                
            nback = tk.Button(nback_frame, text="N-Back", command=nbrun, font=fontsize, anchor="center")
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
            button3 = tk.Button(button3_frame, text="2-Type Reaction Time", command=consent, font=fontsize, anchor="center")
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
            image_label.place(relx=1, rely=0, anchor="ne", x=-20, y=40)
            update_time()

            subprocess.run([python_path, 'Export.py'], check=True)

            root.mainloop()            

            root.quit()
            
            
        else: 

            subprocess.run([python_path, 'Export.py'], check=True)
            subprocess.run([python_path, file_path], check=True)
        
    main()

else:
    import tkinter as tk
    errortext = "Your device is not connected to the internet, please connect to the internet to continue the task\n\nThe task must ensure that you have the correct files installed, which requires an active internet connection"

    fontsize = ("Helvetica", 18)
    fontsize1 = ("Helvetica", 22)
    fontsize2 = ("Helvetica", 12)

    from tkinter import simpledialog, messagebox

    messagebox.showerror("Error", errortext)
