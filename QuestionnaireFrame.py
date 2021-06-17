import tkinter as tk
from tkinter import ttk
import csv
import FileChecker
from random import choice
from PIL import Image, ImageTk

'''
QuestionnaireFrame.py
    Contains all information for QuestionnaireFrame. This is where the user will read questions
    and answer them.
    
'''

class Question():
    '''Class contains all attributes of a question

        Important Notes:
            possible_answers is in a dict. Dict in format { answer_key : answer }
            answer_key is char (a, b, c, d)
            Can only contain min/max 4 possible answers else exception.
    '''
    def __init__(self, question, possible_answers, correct_answer, image=None):
        '''
        :param question: String. Question to ask
        :param possible_answers:
        :param correct_answer:
        :param image, An optional image
        '''

        self.question = question.strip()
        self.possible_answers = possible_answers
        self.user_answer = None
        self.is_question_answered = False
        self.correct_answer_key = correct_answer.lower().strip()
        self.image = image

    # Methods below are self explanatory
    def get_question(self):
        return self.question

    def get_possible_answers(self):
        return self.possible_answers

    def get_image(self):
        return self.image

    def get_user_answer(self):
        return self.user_answer

    def get_answer_key(self):
        return self.correct_answer_key

    def is_user_correct(self):
        if self.user_answer == self.correct_answer_key:
            return True
        else:
            return False

    def answer_question(self, answer_key):
        self.is_question_answered = True
        self.user_answer = answer_key.lower()

class QuestionnaireFrame(tk.Frame):
    ''' Class QuestionnaireFrame contains the entire frame for the questioning of user'''
    def __init__(self, parent, top_level, *args, **kwargs):
        #Top level config and current frame settings
        super().__init__(parent, *args, **kwargs)
        self.top_level = top_level
        self.top_level.minsize(600, 550)
        self.grid_columnconfigure(0, minsize=400, weight=1)
        self.grid_columnconfigure(1, minsize=200, weight=1)
        self.rowconfigure(0, weight=1)

        ##############IMPORTANT#########
        self.player_settings = None
        self.current_question_number = 0 # 0 - 9
        self.questions_to_display = []
        self.output_text = {}
        self.user_answer = tk.StringVar()
        self.questionnaire_frame_styling = ttk.Style()

        self.questionnaire_frame_styling.configure("Default.TFrame", background="#E5E7E9", )
        self.questionnaire_frame_styling.configure("Default.TRadiobutton", background="#E5E7E9", wraplength=120)

        #######################
        # Left side of window #
        #######################
        self.left_frame = tk.Frame(self, bg="#E5E7E9")
        self.left_frame.grid(column=0, row=0, sticky="nsew")
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, minsize=250)

        # Question label frame. (Box to surround question and image)
        self.question_box = tk.LabelFrame(self.left_frame, text="Question", bg="#E5E7E9", fg="blue")
        self.question_box.grid(column=0, row=0, padx=20, pady=10, ipady=10, sticky="nsew")

        # Question itself
        question = tk.StringVar()
        self.output_text["question"] = question
        tk.Label(self.question_box, textvariable=self.output_text["question"], bg="#E5E7E9", wraplength=300, width=50, height=3).pack()

        # Question image
        self.img_label = tk.Label(self.question_box)
        self.img_label.pack()

        # Label frame for possible answers.
        self.possible_answers_box = tk.LabelFrame(self.left_frame, text="Answers", bg="#E5E7E9", fg="blue")
        self.possible_answers_box.grid(column=0, row=1, padx=20, pady=20, sticky="nsew")
        self.possible_answers_box.grid_columnconfigure(0, weight=1)
        self.possible_answers_box.grid_columnconfigure(1, weight=1)

        # Possible answers widgets
        self.output_text["possible_answer_a"] = tk.StringVar()
        self.output_text["possible_answer_b"] = tk.StringVar()
        self.output_text["possible_answer_c"] = tk.StringVar()
        self.output_text["possible_answer_d"] = tk.StringVar()
        ttk.Radiobutton(self.possible_answers_box, style="Default.TRadiobutton", value="a", variable=self.user_answer, command=self.on_radio_button_selection, textvariable=self.output_text["possible_answer_a"]).grid(column=0, row=0, pady=10, sticky="nsew")
        ttk.Radiobutton(self.possible_answers_box, style="Default.TRadiobutton", value="b", variable=self.user_answer, command=self.on_radio_button_selection, textvariable=self.output_text["possible_answer_b"]).grid(column=1, row=0, pady=10, sticky="nsew")
        ttk.Radiobutton(self.possible_answers_box, style="Default.TRadiobutton", value="c", variable=self.user_answer, command=self.on_radio_button_selection, textvariable=self.output_text["possible_answer_c"]).grid(column=0, row=1, pady=10, sticky="nsew")
        ttk.Radiobutton(self.possible_answers_box, style="Default.TRadiobutton", value="d", variable=self.user_answer, command=self.on_radio_button_selection, textvariable=self.output_text["possible_answer_d"]).grid(column=1, row=1, pady=10, sticky="nsew")
        # Grid configs
        self.possible_answers_box.columnconfigure(0, minsize=150)
        self.possible_answers_box.columnconfigure(1, minsize=150)
        self.possible_answers_box.rowconfigure(0, minsize=60)
        self.possible_answers_box.rowconfigure(1, minsize=60)

        ########################
        # Right side of window #
        ########################
        self.right_frame = tk.Frame(self, width=200, bd=1, relief="sunken")
        self.right_frame.grid(column=1, row=0, sticky="nsew")
        self.right_frame.columnconfigure(0, weight=1)

        # Timer Box
        timer_box = ttk.Frame(self.right_frame, borderwidth=10, relief="ridge", )
        timer_box.grid(column=0, row=0, ipadx=15, padx=20, pady=20, columnspan=2, sticky="nsew")

        # Timer text
        ttk.Label(timer_box, text="Timer:",  anchor=tk.CENTER).pack()
        self.timer_label_intvar = tk.IntVar()
        self.timer_id = None
        self.timer_label_obj = ttk.Label(timer_box, textvariable=self.timer_label_intvar, anchor=tk.CENTER)
        self.timer_label_obj.pack()
        self.timer_disabled_label = ttk.Label(timer_box, text="Timer disabled")

        # Current question box
        self.question_position_labelframe = ttk.LabelFrame(self.right_frame, text="Questions")
        self.question_position_labelframe.grid(column=0, row=1, sticky="nsew")



    def init_quiz(self, player_settings):
        ''' This function should be called upon when frame is raised/displayed.'''
        self.clear_info()
        self.player_settings = player_settings # Set player settings to a "public" variable

        # Check if the question set is from a custom file
        if self.player_settings["custom_file"] != "":
            # Prepare to load question_set from the custom_file type
            question_set = self.player_settings["custom_file"]
            self.player_settings["custom_file"] = "" # Clear for next time
        else:
            # Prepare to laod question_set from default file
            question_set = self.player_settings["quiz_mode"]


        file_checker_info = FileChecker.check_question_set(question_set, 10) # Minimum valid questions to pass check
        '''
        Checks if question set is valid
            FAIL -> An exception returns
            PASS -> Contains a list of the lines that have failed. But there is sufficient questions to continue
        '''
        if type(file_checker_info) in (Exception, ValueError, FileNotFoundError, FileChecker.InsufficientQuestionsError):
            # Failed verification
            self.top_level.show_error_frame("Critical Error", file_checker_info)
            self.top_level.show_frame("IntroductionFrame")
        elif len(file_checker_info) != 0:
            # Pass verification with failed lines
            self.top_level.show_warning_frame("Warning", "Error detected in lines {} in {}.txt\nProgram has sufficient questions and will continue without these questons".format(file_checker_info, question_set))
            self.create_questions_set(question_set, file_checker_info)
            self.next_question()
        else:
            # Pass verfication with NO failed lines
            self.create_questions_set(question_set)
            self.next_question()

    def create_questions_set(self, question_set, rejected_lines=[]):
        '''This function generates all the questions from the question_set chosenin IntroductionFrame. It will then
        choose 10 random questions to be displayed to the quiz. These 10 random questions are stored as self.questions_to_display
        '''
        # Important variables
        all_questions = [] # All question objs that will be created
        file = open(question_set, "r")
        reader = csv.reader(file, delimiter="|")
        current_line = 1 # Current line reading
        failed_images = [] # Items stored in tuple (line, fileName)
        #Also rejected_lines which is from the constructor.

        # Go through each line
        for line in reader:
            if current_line in rejected_lines:
                # If current line in rejected lines, Skip current line
                current_line += 1
                continue
            elif line[0].lower().strip() == "end":
                # If line reads END, stop reading any more from file
                break
            elif line[0] != "END":
                # Successful questions, gather parts of the data
                question = line[0]
                possible_answers = {  # Get possible answers
                    "a" : line[1],
                    "b" : line[2],
                    "c" : line[3],
                    "d" : line[4]
                }
                answer = line[5].lower().strip() # Get answer

                # Get image if avaliable
                rendered_image = ""
                try:
                    if line[6].strip() != "": # Get image if there is one
                        try:
                            # Load image and resize
                            file_name = line[6].strip()
                            load_image = Image.open(file_name)
                            load_image = load_image.resize((300, 300), Image.ANTIALIAS)
                            rendered_image = ImageTk.PhotoImage(load_image)
                        except Exception as e:
                            # If exception occurs, Load a placeholder image. No image avaliable.
                            failed_images.append((current_line, line[6]))
                            load_image = Image.open("images/no_image_avaliable.png")
                            load_image = load_image.resize((300, 300), Image.ANTIALIAS)
                            rendered_image = ImageTk.PhotoImage(load_image)
                    else:
                        # Index error, If there is no 6th column
                        raise IndexError()
                except IndexError:
                    # If there is no 6th column, Load placeholder image.
                    load_image = Image.open("images/no_image_avaliable.png")
                    load_image = load_image.resize((300, 300), Image.ANTIALIAS)
                    rendered_image = ImageTk.PhotoImage(load_image)

                current_line += 1 # Move onto next line
                all_questions.append(Question(question, possible_answers, answer, rendered_image)) # Add new question obj
            else:
                break

        self._display_img_warnings(failed_images) # Display any images that failed to load
        self._select_rand_questions(all_questions, 10) # Amount of questions to display

    def _select_rand_questions(self, all_questions, amt_questions):
        ''' Select amount of questions to display for quiz that are random
        :param all_questions: A list containing random questions to select from
        :param amt_questions: The amount of questions to choose
        :return: None
        '''
        for i in range(amt_questions):
            rand_question = choice(all_questions) # Select random question to add
            self.questions_to_display.append(rand_question) # Add question to display to "public" list
            all_questions.remove(rand_question) # Remove the question added to prevent double ups

    def _display_img_warnings(self, failed_images):
        ''' Display errors of failed images if present
        :param failed_images: The failed images
        :return: None
        '''
        str_to_display = ""
        if len(failed_images) != 0:
            for f_img in failed_images:
                str_to_display = "{}{:8s} : Line {}\n".format(str_to_display, f_img[1], f_img[0])
            self.top_level.show_warning_frame("Error loading images", "Program to failed to load these images \n(Note: Program will continue without these images)\n{}".format(str_to_display))

    def on_radio_button_selection(self):
        ''' Called whenever an answer is pressed
        :return:
        '''
        ans_key = self.user_answer.get()
        question = self.questions_to_display[self.current_question_number-1]
        question.answer_question(ans_key)
        self.next_question()

    def next_question(self):
        ''' When called, Moves to next question. If none, next frame'''
        current_question_number = self.current_question_number

        # Check if timer feature is on
        if self.player_settings["is_timer"] == True:
            # If true, Display timer value and initiate
            self.timer_disabled_label.pack_forget()
            self.timer_label_obj.pack()
            self.init_timer()
        else:
            # If false, set it to deactivated
            self.timer_label_intvar.set("")
            self.timer_label_obj.pack_forget()
            self.timer_disabled_label.pack()

        try: # Try to load next question. If none, Next Frame.
            question_object = self.questions_to_display[current_question_number]
            question = question_object.get_question()
            possible_answers = question_object.get_possible_answers()

            self.output_text["question"].set(question)
            for i in ("a", "b", "c", "d"):
                self.output_text["possible_answer_" + i].set(possible_answers[i])
            self.img_label.configure(image=question_object.get_image())
            self.user_answer.set("")
            self.current_question_number += 1
            self.update_question_position()
        except IndexError:
            self.next_frame()

    def init_timer(self, timer_length=15):
        ''' Check if a timer thread is already activated. If true, cancel it
        :param timer_length: Int
        '''
        self.timer_label_intvar.set(timer_length)
        if self.timer_id != None:
            self.timer_label_obj.after_cancel(self.timer_id)
        self.timer_process()

    def timer_process(self):
        ''' Creates a timer thread, that counts all the way to 0
        :return:
        '''
        current_val = self.timer_label_intvar.get()
        self.timer_label_intvar.set(current_val - 1)
        if self.timer_label_intvar.get() != 0:
            # If timer not 0 yet
            self.timer_id = self.timer_label_obj.after(1000, self.timer_process)
        elif self.timer_label_intvar.get() == 0:
            self.timer_id = None
            self.timer_label_intvar.set("")
            self.next_question()

    def update_question_position(self):
        ''' Updates the label displaying current question.'''

        # Clear treeview
        for widget in self.question_position_labelframe.winfo_children():
            widget.destroy()

        # Create a label for each question
        for nth_question in range(len(self.questions_to_display)):
            label = tk.Label(self.question_position_labelframe, text="Question {}".format(nth_question+1))
            label.pack(fill=tk.X)

            # Highlights current question
            if nth_question+1 == self.current_question_number:
                label.config(bg="#949ba6")

    def clear_info(self):
        ''' Clear all player information'''
        self.player_settings = None
        self.current_question_number = 0
        self.questions_to_display = []
        self.user_answer.set("")

    def next_frame(self):
        ''' Proceeds to next frame, The results frame'''

        # Clear any timer threads if present (Prevents frame from switching)
        if self.timer_id != None:
            self.timer_label_obj.after_cancel(self.timer_id)

        # Proceed to the next frame
        self.top_level.frames["ResultsFrame"].init_results(self.player_settings, self.questions_to_display)
        self.top_level.show_frame("ResultsFrame")

