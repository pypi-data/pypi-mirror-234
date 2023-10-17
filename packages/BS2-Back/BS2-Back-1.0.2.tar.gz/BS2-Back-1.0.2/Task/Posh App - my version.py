import tkinter
import tkinter.messagebox
import customtkinter
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import Location
import time
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import os
import glob
import subprocess
import spwf
participant_number = spwf.participant_number

folder_name = f'Participant {participant_number}'


def is_connected():
    websites = ['www.google.com', 'www.facebook.com']
    for website in websites:
        try:
            socket.create_connection((website, 80))
            return True
        except OSError:
            pass
    return False

#if is_connected():

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

                self.master.geometry("600x170+{}+{}".format(x, y))
                
                self.pin_label = tk.Label(self.master, text="Welcome to the task\n\nTo begin, please enter your PIN. This will have been sent to you via email.\n\nEnter your PIN:")
                self.pin_label.pack()
                
                #self.pin_entry = tk.Entry(self.master)
                self.pin_entry = customtkinter.CTkEntry(self.master, placeholder_text="")

                self.pin_entry.pack()
                
                #self.submit_button = tk.Button(self.master, text="Submit", command=self.submit_pin)
                self.submit_button = customtkinter.CTkButton(self.master, command=self.submit_pin)
                self.submit_button.configure(text="Submit PIN")


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
        
    if glob.glob(folder_name + '/*Consent.txt'):
        print("Consent")

        customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
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

        class App(customtkinter.CTk):
            def __init__(self):
                super().__init__()

                # configure window
                self.title("Task")
                self.geometry(f"{1100}x{300}")

                # configure grid layout (4x4)
                self.grid_columnconfigure(1, weight=1)
                self.grid_columnconfigure((2, 3), weight=0)
                self.grid_rowconfigure((0, 1, 2), weight=1)

                # create sidebar frame with widgets
                self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
                self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
                self.sidebar_frame.grid_rowconfigure(4, weight=1)
                self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PhD Task", font=customtkinter.CTkFont(size=20, weight="bold"))
                self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
                
                self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
                self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
                self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
                self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
                self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
                self.sidebar_button_3.grid(row=5, column=0, padx=20, pady=10)
                    

                self.sidebar_button_1.configure(text="2-Back")
                self.sidebar_button_2.configure(text="Switching Task")
                self.sidebar_button_3.configure(text="2-Choice Reaction Time Task")

                if rtcount == 1:
                    rttext = f'This has been run {rtcount} time'
                else:
                    rttext = f'This has been run {rtcount} times'
                if scount == 1:
                    stext =  f'This has been run {scount} time'
                else: stext =  f'This has been run {scount} times'
                if nbcount == 1:
                    nbtext =  f'This has been run {nbcount} time'
                else: nbtext =  f'This has been run {nbcount} times'

                self.sidebar_button_1.label = customtkinter.CTkLabel(self.sidebar_frame, text=rttext, anchor="w")

                self.sidebar_button_1.label.grid(row=2, column=0, padx=20, pady=(0, 0))

                self.sidebar_button_2.label = customtkinter.CTkLabel(self.sidebar_frame, text=stext, anchor="w")

                self.sidebar_button_2.label.grid(row=4, column=0, padx=20, pady=(0, 0))

                self.sidebar_button_3.label = customtkinter.CTkLabel(self.sidebar_frame, text=nbtext, anchor="w")

                self.sidebar_button_3.label.grid(row=6, column=0, padx=20, pady=(0, 0))

                runcount = 6
                if rtcount > runcount:
                    self.sidebar_button_3.configure(state="disabled", text="Choose another task")

                if scount > runcount:
                    self.sidebar_button_2.configure(state="disabled", text="Choose another task")

                if nbcount > runcount:
                    self.sidebar_button_1.configure(state="disabled", text="Choose another task")
                    

                    '''self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
                self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
                self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                               command=self.change_appearance_mode_event)
                self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
                self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
                self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
                self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                                       command=self.change_scaling_event)
                self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))'''

                # create main entry and button
                self.entry = customtkinter.CTkEntry(self, placeholder_text="Email Text Here")
                self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

                self.main_button_1 = customtkinter.CTkButton(text="Send Email",master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.send_email)
                self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

                # create textbox
                self.textbox = customtkinter.CTkTextbox(self, width=100)
                self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 100), sticky="nsew")
                self.textbox.configure(wrap="word")
                self.textbox.insert("0.0", "Welcome back to the task\n\nPlease now select a task to perform from the left hand side. If you experience any issues, please use the below email function for support. There is a limit on the number of times each task can be run, where a greyed out button shows that the task has been run too many times.")

                def update_time():
                    current_time = time.strftime("%H:%M:%S")
                    self.textbox2.delete("1.0", tk.END)
                    self.textbox2.configure(wrap="word")

                    self.textbox2.insert(tk.END, f'{current_time}\n\n{Location.loc}')
                    self.after(1000, update_time)

                self.textbox2 = customtkinter.CTkTextbox(self, width=20)
                self.textbox2.grid(row=0, column=3, padx=(20, 20), pady=(20,100), sticky="nsew")
                update_time()


            def open_input_dialog_event(self):
                dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
                print("CTkInputDialog:", dialog.get_input())

            def change_appearance_mode_event(self, new_appearance_mode: str):
                customtkinter.set_appearance_mode(new_appearance_mode)

            def change_scaling_event(self, new_scaling: str):
                new_scaling_float = int(new_scaling.replace("%", "")) / 100
                customtkinter.set_widget_scaling(new_scaling_float)

            def sidebar_button_event(self):
                print("sidebar_button click")

            def send_email(self):
                body = self.entry.get()
                print(body)# Retrieve the text entered in the entry widget
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
                    print("Sent")
                except Exception as e:
                    with open('Email Errors.txt', mode='a+') as f:
                       f.write(str(e))
                       f.write("\n\n")
                    print(e)

        if __name__ == "__main__":
            app = App()
            app.mainloop()
    else:
        subprocess.Popen(['python', 'Consent.py'])

'''else:
    
    errortext = "Your device is not connected to the internet, please connect to the internet to continue the task\n\nThe task must ensure that you have the correct files installed, which requires an active internet connection"

    fontsize = ("Helvetica", 18)
    fontsize1 = ("Helvetica", 22)
    fontsize2 = ("Helvetica", 12)

    messagebox.showerror("Error", errortext)'''

