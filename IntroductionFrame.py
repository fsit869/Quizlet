import tkinter as tk
import csv
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import FileChecker
'''
IntroductionFrame.py

This file contains all the information for the IntroductionFrame. Also the
frame where the user first sees. Contains all the settings for user to play
the quiz as well as the top scoreboard.

IntroductionFrame extends tk.Frame() 

Constructor:
    String parent; Parent of frame. Where frame will be appended
    String top_level; Top level of GUI. Useful for eg changing frames
    Array args; Extr8a settings for frame
    Hashmap kwargs; Keyworded settings for frame
    
Important variables:
    Dict self.widcet_inputs; Contains all widget INPUTS. {WidgetName : tk.VartypeObj}
    Frame self.left_frame; All contents dealing with left side
    Frame self.right_frame; All contents dealing with right side
        Frame game_settings_frame; Game settings labelFrame
        Frame game_mode_frame; Game mode labelFrame
'''

class IntroductionFrame(tk.Frame):
    def __init__(self, parent, top_level, *args, **kwargs):
        # Top level config and frame settings
        super().__init__(parent, *args, **kwargs)
        self.top_level = top_level
        self.top_level.minsize(600, 550)
        self.grid_columnconfigure(0, minsize=400, weight=1)
        self.grid_columnconfigure(1, minsize=200, weight=1)
        self.rowconfigure(0, weight=1)

        ################### IMPORTANT
        # Inputs dictionary. Contains widget inputs
        self.widget_inputs = {}

        #######################
        # Left side of window #
        #######################
        self.left_frame = tk.Frame(self, bg="#E5E7E9")
        self.left_frame.grid(column=0, row=0, sticky="nsew")
    
        # Text Logo
        text_logo_style = ttk.Style()
        text_logo_style.configure("Title.TLabel", background="#E5E7E9", foreground="black",)
        text_logo = ttk.Label(self.left_frame, style="Title.TLabel", text="Q u i z l e t \n\tM a s t e r",
                              font=("Helvetica", 30, "bold italic"))
        text_logo.pack(pady=30)

        # Treeview scoreboard
        tk.Label(self.left_frame, text="Most Recent Top 5 Scores", bg="#E5E7E9").pack()
        self.tree = ttk.Treeview(self.left_frame, )
        self.tree["columns"] = ("Player", "Subject", "Score", "Percentage")
        self.tree.column("#0", width=72, minwidth=60, stretch=tk.NO)
        self.tree.column("Player", width=72, minwidth=60, stretch=tk.NO)
        self.tree.column("Subject", width=72, minwidth=60, stretch=tk.NO)
        self.tree.column("Score", width=72, minwidth=60, stretch=tk.NO)
        self.tree.column("Percentage", width=72, minwidth=60, stretch=tk.NO)
        self.tree.heading("#0", text="Pos",)
        self.tree.heading("Player", text="Player")
        self.tree.heading("Subject", text="Subject",)
        self.tree.heading("Score", text="Score", )
        self.tree.heading("Percentage", text="%", )
        self.tree.pack()

        # Help notebook
        help_box_style = ttk.Style()
        help_box_style.configure("Default.TFrame", background="#E5E7E9",)
        help_box = ttk.Notebook(self.left_frame, width=360, height=85, style="Default.TFrame")
        help_box.pack(fill=tk.BOTH, padx=20, pady=20)

        # About Tab
        help_box_about = ttk.Frame(help_box, style="Default.TFrame")
        help_box.add(help_box_about, text="About")
        help_box_scrollbar = ttk.Scrollbar(help_box_about)
        help_box_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        help_box_about_text = tk.Text(help_box_about)
        help_box_about_text.insert(tk.END, """This program is a quiz program. The left side is high scores while the right side is the game settings.
    
- Record score: Choose whether you would like you score to be displayed if it is top 5

- 15 Second round timer: Limit each question to only 15 seconds for a greater challenge

- Custom file question set: Select a user created question set. Note the question set will be validated.
        """)
        help_box_about_text.config(state=tk.DISABLED, yscrollcommand=help_box_scrollbar.set, wrap=tk.WORD)
        help_box_scrollbar.config(command=help_box_about_text.yview)
        help_box_about_text.pack(side=tk.LEFT, fill=tk.Y)

        # Copyright tab
        help_box_copyright = tk.Frame(help_box, bg="white", relief="groove", bd=1)
        help_box.add(help_box_copyright, text="Copyright")
        help_box_copyright_text = tk.Text(help_box_copyright)
        help_box_copyright_text.insert(tk.END, """Images loaded PIL (Python Imaging Library)\nImages may be copyrighted, I do not own these images. Used for education purposes\nProgram created by Frank Situ\n2nd September 2019""")
        help_box_copyright_text.configure(state=tk.DISABLED)
        help_box_copyright_text.pack()

        # Settings tab
        help_box_settings = tk.Frame(help_box, bg="white", relief="groove", bd=1)
        help_box.add(help_box_settings, text="Settings")
        ttk.Button(help_box_settings, text="Clear leaderboard data", command=self.on_erase_leaderboard_data_button).pack(side=tk.LEFT, pady=20, padx=20, ipadx=10, ipady=10)


        ########################
        # Right side of window #
        ########################
        self.right_frame = tk.Frame(self, width=200, bd=1, relief="sunken")
        self.right_frame.grid(column=1, row=0, sticky="nsew")

        # Program Logo
        load_image = Image.open("program_logo.ico")
        load_image = load_image.resize((130, 130), Image.ANTIALIAS)
        render_image = ImageTk.PhotoImage(load_image)
        img = tk.Label(self.right_frame, image=render_image)
        img.image = render_image # Prevents Python Garbage collector from deleting img
        img.grid(column=0, row=0, columnspan=3, sticky="nsew", pady=(10, 15), padx=10)

        # Player Name Entry
        self.widget_inputs["player_name"] = tk.StringVar()
        ttk.Label(self.right_frame, text="Name: ").grid(column=0, row=1, padx=(5,0), sticky=tk.W)
        ttk.Entry(self.right_frame, textvariable=self.widget_inputs["player_name"]).grid(column=1, row=1, columnspan=2, ipadx=10, sticky=tk.NSEW,)

        # Game Settings Label Frame
        self.game_settings_frame = ttk.LabelFrame(self.right_frame, text="Quiz Settings")
        self.game_settings_frame.grid(column=0, row=2, columnspan=3, pady=10,  sticky=tk.NSEW)

        # Record Score checkbox
        self.widget_inputs["is_record_score"] = tk.BooleanVar()
        ttk.Checkbutton(self.game_settings_frame, text="Record Score", variable=self.widget_inputs["is_record_score"]).pack(anchor=tk.W, padx=20)

        # 15 sec timer checkbox
        self.widget_inputs["is_timer"] = tk.BooleanVar()
        ttk.Checkbutton(self.game_settings_frame, text="15 Second Round Timer", variable= self.widget_inputs["is_timer"]).pack(anchor=tk.W, padx=20)

        # Game mode choice Frame
        self.game_mode_frame = ttk.LabelFrame(self.right_frame, text="Quiz Mode")
        self.game_mode_frame.grid(column=0, row=3, columnspan=3, sticky=tk.NSEW)

        # Possible quiz modes
        self.widget_inputs["quiz_mode"] = tk.StringVar()
        ttk.Radiobutton(self.game_mode_frame, command=self.on_radio_button, value="question_set_maths.txt", text="Maths", variable=self.widget_inputs["quiz_mode"]).pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(self.game_mode_frame, command=self.on_radio_button, value="question_set_physics.txt", text="Physics", variable=self.widget_inputs["quiz_mode"]).pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(self.game_mode_frame, command=self.on_radio_button, value="question_set_drivingTheory.txt", text="Driving Theory", variable=self.widget_inputs["quiz_mode"]).pack(anchor=tk.W, padx=20)

        # Custom file option
        self.widget_inputs["custom_file"] = tk.StringVar()
        ttk.Radiobutton(self.game_mode_frame, value="custom", variable=self.widget_inputs["quiz_mode"], command=self.on_custom_quiz_mode, text="Custom", ).pack(anchor=tk.W, padx=20)

        # File display label
        self.file_display = tk.Label(self.game_mode_frame, textvariable=self.widget_inputs["quiz_mode"], state="disabled", wraplength=150)
        self.file_display.pack()

        # Play button
        self.right_frame.grid_rowconfigure(4, weight=1)
        ttk.Button(self.right_frame, text="Play!", command=self.on_play_button, ).grid(column=0, row=4, columnspan=3, sticky="nsew", padx=20, pady=20)

        # Init leader board
        self.init_contents()

    def init_contents(self):
        ''' Should be called upon whenever frame is displayed, eg when frame raised. Updates the treeview
        :return: None
        '''
        self.clear_treeview()
        # Display leaderboard from TopScores.txt
        with open("TopScores.txt", "r") as file:
            reader = csv.reader(file, delimiter="|")
            player_pos = 1
            for player in reader:
                self.insert_treeview(player_pos, player[0], player[1], player[2], player[3]+"%")
                player_pos += 1

    def on_erase_leaderboard_data_button(self):
        ''' Called when erase leaderboard button pressed'''
        self.clear_treeview()
        self.erase_leaderboard_file()

    def erase_leaderboard_file(self):
        '''Clears the topscores saved in text file'''
        with open("TopScores.txt", "w"):
            pass

    def on_radio_button(self):
        ''' Called when radiobutton pressed. Updates the file display widget
        :return: None
        '''
        self.widget_inputs["custom_file"].set("")
        self.file_display.config(textvariable=self.widget_inputs["quiz_mode"])

    def on_custom_quiz_mode(self):
        ''' Called when custom radiobutton button selected. Opens a filedialogue for user
        to select custom file.

        :return: String File Location
        '''
        self.top_level.update()
        self.widget_inputs["custom_file"].set("") # Clear custom file var
        file = filedialog.askopenfilename(defaultextension=".txt", title="Load question set") # Get path
        if file == "":
            # Occurs when user presses cancel. Empty path "". Clears path
            self.widget_inputs["quiz_mode"].set("")
            self.file_display.config(textvariable=self.widget_inputs["quiz_mode"]) # Clears file display
        else:
            # Occurs when user selects a path.
            self.widget_inputs["custom_file"].set(file) # Custom file path
            self.file_display.config(textvariable=self.widget_inputs["custom_file"]) # Change file display label
            self.check_custom_file(file) # Def to check custom file

    def check_custom_file(self, file):
        ''' Should be called upon to verify custom file. Rejects file if fails FileChecker, else continues
        :param file: File location
        :return:
        '''
        returnedValue = FileChecker.check_question_set(file, min_valid_questions=10) # Check file. Returned value is failed lines or an exception
        if type(returnedValue) in (Exception, Exception, ValueError, FileNotFoundError, FileChecker.InsufficientQuestionsError):
            # If returned value is any exception, Reject file and get user to choose another set. Clear the path
            self.file_display.config(textvariable=self.widget_inputs["quiz_mode"])
            self.widget_inputs["quiz_mode"].set("")
            self.widget_inputs["custom_file"].set("")
            self.top_level.show_error_frame("Error loading file", "An error occured while loading file\n{}".format(returnedValue))

    def on_play_button(self):
        ''' Called when Play button pressed.

        Is all entries filled
            -> Yes; Continue to questionnaire frame
            -> No; Error msgbox, warn user

        :return: None
        '''
        if self.check_all_entries_filled():
            user_inputs = self.get_inputs()
            self.next_frame()
            self.top_level.frames["QuestionnaireFrame"].init_quiz(user_inputs)
        else:
            self.top_level.show_error_frame("Error!", "Make sure all entries are filled\n- Username\n- Quiz Mode")

    def check_all_entries_filled(self):
        ''' Check if all important widgets are filled. Closely linked with on_play_button()

        Boolean :return:  True, All important widgets filled
        Boolean :return: False, Important widgets not filled.
        '''
        if self.widget_inputs["player_name"].get().strip() != "":
            if self.widget_inputs["quiz_mode"].get() != "":
                return True
        return False

    def clear_treeview(self):
        '''Clears treeview.

        :return: None
        '''
        self.tree.delete(*self.tree.get_children())

    def insert_treeview(self, player_position, player_name, player_subject, player_score, player_percentage):
        ''' Inserts a new row of information for treeview

        String :param player_position: Player position (1st, 2nd...)
        String :param player_name:  Player name
        String :param player_subject: Subject player played. (Maths, Phys...)
        String :param player_score: Player score (20/24, 12/24)
        String :param player_percentage: Player correct % (62% 23%...)
        :return: None
        '''
        self.tree.insert("", "end", text=player_position, values=(player_name, player_subject,
                                                                      player_score, player_percentage))

    def next_frame(self):
        ''' When called moves to questionnaire frame
        :return: None
        '''
        self.top_level.show_frame("QuestionnaireFrame")

    def get_inputs(self):
        ''' Returns dict of values of all input widgets

        Dict :return: {Widget_Name, Value}
        '''
        widget_keys = list(self.widget_inputs.keys())
        widget_info = {}
        for key in widget_keys:
            # player_name must be stripped and title(). Booleans cant do this thus seperate
            if key == "player_name":
                widget_info[key] = self.widget_inputs[key].get().strip().title()
            else:
                widget_info[key] = self.widget_inputs[key].get() # Note StringVar returns. thus need to use get

        return widget_info



