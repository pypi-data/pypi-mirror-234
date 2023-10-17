import tkinter
import tkinter.messagebox
import customtkinter
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import spwf
import Location
import time
from datetime import datetime
import tkinter as tk
import socket
import os
import glob
import subprocess

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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Task Battery", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        def pis():
            subprocess.call(['open','PIS.docx'])

        consentcomplete = False

        def consentform():
            
            consentcomplete = True
            self.sidebar_button_3.configure(state="enabled", text="Start the Task")

            return

        def taskstart():
            print("In start")
            app.quit()
            app.destroy()
            
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=pis)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=consentform)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=taskstart)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=100)

        if consentcomplete == False:
                self.sidebar_button_3.configure(state="disabled", text="Complete consent form")
            
        self.sidebar_button_1.configure(text="Participant Information Sheet")
        self.sidebar_button_2.configure(text="Consent Form")
        self.sidebar_button_3.configure(text="Start the Task")


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
