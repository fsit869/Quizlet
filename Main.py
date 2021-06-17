import IntroductionFrame, QuestionnaireFrame, ResultsFrame
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
'''
Main.py

################IMPORTANT:##########
Pillow must be installed in order for program to work
https://pypi.org/project/Pillow/ 
####################################

Contains the entire GUI program itself. (Class Application). 
This file contains the top level of the GUI.
This file also allows user to switch frames
Appliciaton extends tk.Tk()

Important variables:
    dict self.frames; Contains all initilized frames {frameName : FrameObj}
'''
# Validation https://stackoverflow.com/questions/18218401/entry-validation-extra-arguments

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        # Init toplevel config settings
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.title("Quizlet Master")
        self.iconbitmap("program_logo.ico")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Init frames, Allows for switching frames in top level
        self.frames = {}
        self.init_frames(IntroductionFrame.IntroductionFrame,
                         QuestionnaireFrame.QuestionnaireFrame,
                         ResultsFrame.ResultsFrame
                         )

        # Display which frame to show first, Useful for development
        self.show_frame("IntroductionFrame")
        # self.show_frame("QuestionnaireFrame")
        # self.show_frame("ResultsFrame")

    def init_frames(self, *frames_to_init):
        ''' Initlizes frames and packs frames into one area. Allows for one frame to be raised on top

        :param frames_to_init: *frames to init
        :return: None
        '''
        for frame in frames_to_init:
            frame_name = frame.__name__
            frame_object = frame(parent=self, top_level=self) #Create frame obj
            self.frames[frame_name] = frame_object #Store frame for future reference
            frame_object.grid(row=0, column=0, sticky="nsew") #Frames are stacked on top each other

    def show_frame(self, frame_name):
        '''Raises the frame chosen. Used to change frames and let user see top frame
c
        :param page_name: Frame to raise to top.
        :return: None(
        '''
        frame_object = self.frames[frame_name]
        frame_object.tkraise()

    def show_warning_frame(self, title, text):
        '''When called, Shows a msgbox warning type

        :param title: Title of msgbox
        :param text: Text content of msgbox
        :return: None
        '''
        messagebox.showwarning(title, text)

    def show_error_frame(self, title, text):
        '''When called, shows msgbox error type

        :param title: Title of msgbox
        :param text: Text content of msgbox
        :return: None
        '''
        messagebox.showerror(title, text)

    def question_msg_frame(self, title, text):
        answer = messagebox.askyesnocancel(title, text)
        return answer
#Starting point. Main execution
if __name__ == "__main__":
    App = Application()
    App.mainloop()
