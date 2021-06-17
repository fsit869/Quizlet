import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

'''
ReviewQuestionsTopLevel.py

This file contains a NEW toplevel for the user to review his/her questions.
NOTE: Most of the code here is simply copied and pasted from QuestionnaireFrame.py

Ps: Code could be more efficient if QuestionnaireFrame.py & ReviewQuestionsTopLevel.py inherited
from a base class. As two of the files contain mostly same information. Implementing would require
rework of entire QuestionnaireFrame.py thus is not done. 
'''
class ReviewAnswers(tk.Toplevel):
    def __init__(self, questions_answered, root):
        # Confiqure toplevel settings
        super().__init__()
        self.title("Review Answers")
        self.minsize(600, 550)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_exitMenu_button)
        self.grid_columnconfigure(0, minsize=400, weight=1)
        self.grid_columnconfigure(1, minsize=200, weight=1)
        self.rowconfigure(0, weight=1)
        self.grab_set()

        # Important variables
        self.root = root
        self.questions_answered = questions_answered
        self.current_question_number = 1
        self.output_text = {}
        self.current_question_user_answer = tk.StringVar()
        
        ##############
        # Left Frame #
        ##############
        self.left_frame = tk.Frame(self, bg="#E5E7E9")
        self.left_frame.grid(column=0, row=0, sticky="nsew")
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, minsize=250)

        # Question label frame
        self.question_box = tk.LabelFrame(self.left_frame, text="Question", bg="#E5E7E9", fg="blue")
        self.question_box.grid(column=0, row=0, padx=20, pady=20, sticky="nsew")

        # Question itself
        question = tk.StringVar()
        self.output_text["question"] = question
        tk.Label(self.question_box, textvariable=self.output_text["question"],bg="#E5E7E9", wraplength=300, width=50, height=3).pack()

        # Question img
        self.img_label = tk.Label(self.question_box)
        self.img_label.pack()

        # Possible answers label frame
        self.possible_answers_box = tk.LabelFrame(self.left_frame, text="Answers",bg="#E5E7E9", fg="blue")
        self.possible_answers_box.grid(column=0, row=1, padx=20, pady=20, sticky="nsew")
        self.possible_answers_box.grid_columnconfigure(0, weight=1)
        self.possible_answers_box.grid_columnconfigure(1, weight=1)

        # Possible answers widgets
        self.output_text["possible_answer_a"] = tk.StringVar()
        self.output_text["possible_answer_b"] = tk.StringVar()
        self.output_text["possible_answer_c"] = tk.StringVar()
        self.output_text["possible_answer_d"] = tk.StringVar()

        # Radio Buttons TL = Top Left, BR = Bottom Right...
        self.radio_TL = ttk.Radiobutton(self.possible_answers_box, value="a", variable=self.current_question_user_answer, textvariable=self.output_text["possible_answer_a"])
        self.radio_TR = ttk.Radiobutton(self.possible_answers_box, value="b", variable=self.current_question_user_answer, textvariable=self.output_text["possible_answer_b"])
        self.radio_BL = ttk.Radiobutton(self.possible_answers_box, value="c", variable=self.current_question_user_answer, textvariable=self.output_text["possible_answer_c"])
        self.radio_BR = ttk.Radiobutton(self.possible_answers_box, value="d", variable=self.current_question_user_answer, textvariable=self.output_text["possible_answer_d"])
        self.radio_TL.grid(column=0, row=0, sticky="nsew")
        self.radio_TR.grid(column=1, row=0, sticky="nsew")
        self.radio_BL.grid(column=0, row=1, sticky="nsew")
        self.radio_BR.grid(column=1, row=1, sticky="nsew")

        # Label displaying nothing answered
        self.none_answered_label = tk.Label(self.possible_answers_box, text="None answered, Only correct answer displayed", fg="red")
        self.none_answered_label.grid(column=0, row=2, columnspan=2)

        # Confiqure grid settings
        self.possible_answers_box.columnconfigure(0, minsize=150)
        self.possible_answers_box.columnconfigure(1, minsize=150)
        self.possible_answers_box.rowconfigure(0, minsize=60)
        self.possible_answers_box.rowconfigure(1, minsize=60)

        # Disable interaction for all radiobuttons
        for radio_obj in (self.radio_TL, self.radio_TR, self.radio_BL, self.radio_BR):
            radio_obj.bind("<Button-1>", self._disable_events)
            radio_obj.bind("<Enter>", self._disable_events)

        ###############
        # Right Frame #
        ###############
        self.right_frame = tk.Frame(self, width=200, bd=1, relief="sunken")
        self.right_frame.grid(column=1, row=0, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)

        # Label Position
        self.question_position_labelframe = ttk.LabelFrame(self.right_frame, text="Questions")
        self.question_position_labelframe.pack(fill=tk.X, padx=20, pady=(20))
        self.update_question_position()

        # Next / Previous Question
        tk.Button(self.right_frame, text="Previous", command=self.on_previous_button, height=5).pack(fill=tk.X, padx=20)
        tk.Button(self.right_frame, text="Next", command=self.on_next_button, height=5).pack(fill=tk.X, padx=20)
        tk.Button(self.right_frame, text="Return", command=self.on_return_button).pack(fill=tk.BOTH, padx=20,pady=20)

        # Load question information
        self.load_current_question_info()

    def on_next_button(self):
        ''' Called when next button clicked. Changes current question number up. If reached max
        goes back to min'''
        if self.current_question_number + 1 < len(self.questions_answered)+1:
            self.current_question_number += 1
        else:
            self.current_question_number = 1

        self.load_current_question_info()
        self.update_question_position()

    def on_return_button(self):
        ''' Destroys this top level and returns to original toplevel.
        '''
        self.destroy()
        self.root.deiconify()

    def _on_exitMenu_button(self):
        ''' Called when X close button is pressed. Confirms whether user wants to quit program '''
        confirm = self.root.question_msg_frame("Exit", "Are you sure you would like to QUIT the program?\n"
                                                       "Not to be confused with return, Where you can play again")
        if confirm != True:
            return "break"
        else:
            self.destroy()
            self.quit()

    def on_previous_button(self):
        ''' Go back to previous question. If already reached min, Go to max
        :return:
        '''
        if self.current_question_number - 1 == 0:
            self.current_question_number = len(self.questions_answered)
        else:
            self.current_question_number -= 1

        self.load_current_question_info()
        self.update_question_position()

    def load_current_question_info(self):
        ''' Loads the current question number and information and displays it
        :return:
        '''

        # Load current question
        current_question_obj = self.questions_answered[self.current_question_number - 1]

        # Display question
        self.output_text["question"].set(current_question_obj.get_question())

        # Display Image
        self.img_label.configure(image=current_question_obj.get_image())

        # Display possible answers
        possible_answers = current_question_obj.get_possible_answers()
        for i in ("a", "b", "c", "d"):
            self.output_text["possible_answer_" + i].set(possible_answers[i])

        # Set what user answered
        self.current_question_user_answer.set(current_question_obj.get_user_answer())

        # Highlight correct answer radiobutton
        radiobutton_styles = ttk.Style()
        radiobutton_styles.configure("Wrong.TRadiobutton", background="#ffcccb", foreground="black", wraplength=120)
        radiobutton_styles.configure("Right.TRadiobutton", background="#a5d610", foreground="black", wraplength=120)
        radiobutton_styles.configure("Default.TRadiobutton", foreground="black", background="#E5E7E9", wraplength=120)
        for radio_val, radio_obj in (("a", self.radio_TL), ("b", self.radio_TR), ("c", self.radio_BL), ("d", self.radio_BR)):
            if current_question_obj.get_answer_key() == radio_val:
                # Highlight correct key
                radio_obj.config(style="Right.TRadiobutton")
            elif (self.current_question_user_answer.get() != current_question_obj.get_answer_key()) and (self.current_question_user_answer.get() == radio_val):
                # Highlight wrong answer if selected
                radio_obj.config(style="Wrong.TRadiobutton")
            else:
                # Highlight default
                radio_obj.config(style="Default.TRadiobutton")

        # Check if user answered nothing, If true, high label displaying user answered nothing
        if self.current_question_user_answer.get() == "None":
            self.none_answered_label.grid()
        else:
            self.none_answered_label.grid_remove()

    def update_question_position(self):
        ''' Updates the current question display. '''
        for widget in self.question_position_labelframe.winfo_children():
            widget.destroy()

        for nth_question in range(len(self.questions_answered)):
            label = tk.Label(self.question_position_labelframe, text="Question {}".format(nth_question+1))
            label.pack(fill=tk.X)

            if nth_question+1 == self.current_question_number:
                label.config(bg="#949ba6")

    def _disable_events(self, event):
        ''' Disable an event from a widget.
        '''
        return "break"