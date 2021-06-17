import csv
import tkinter as tk
import ReviewQuestionsTopLevel
from tkinter import ttk
''' ResultsFrame.py

This file contains the score of the player. It will also be where the user decides to 
    - Play again
    - Review questions
    - Quit
    
'''

class ResultsFrame(tk.Frame):
    def __init__(self, parent, top_level, *args, **kwargs):
        # Config settings
        super().__init__(parent, *args, **kwargs)
        self.top_level = top_level
        self.top_level.minsize(600, 550)

        # Score text
        ttk.Label(self, text="Your Score", font=("Helvetica", 40, "bold")).pack(pady=(30,10))
        self.score = 0
        self.score_text = tk.StringVar()
        score_label = tk.Label(self, textvariable=self.score_text, bd=1, relief="groove", fg="blue", font=("Helvetica", 40, ))
        score_label.pack(ipadx=20)

        # Information text (Displays whether score will/not be saved)
        self.information_text = tk.StringVar()
        ttk.Label(self, textvariable=self.information_text, ).pack(pady=(30,10))

        # Review questions button
        ttk.Button(self, command=self.on_review_questions_button, text="Review answers").pack(fill=tk.X, ipady=20, padx=30)

        # Play again button
        ttk.Button(self, command=self.on_play_again_button, text="Play Again!").pack(fill=tk.X, ipady=20, padx=30)

    def init_results(self, player_settings, questions_answered):
        ''' This function should be called upon when frame is raised

        :return:
        '''
        # self.clear_info()
        self.player_settings = player_settings
        self.questions_answered = questions_answered

        # Calculate and display score
        self.calculate_score()
        self.display_score()

        # Save score if option was ticked
        if self.if_saved_score_ticked():
            self.information_text.set("Your score WILL be saved if it is a highscore")
            self.write_top_scores()
        else:
            self.information_text.set("Your score will NOT be saved")


    def calculate_score(self):
        ''' Calculates the score of current user from questions answered
        Stored in self.score
        :return: None
        '''
        self.score = 0
        for question in self.questions_answered:
            if question.is_user_correct():
                self.score += 1

    def display_score(self):
        '''

        :return:
        '''
        self.score_text.set("{}/{}".format(self.score, len(self.questions_answered)))

    def if_saved_score_ticked(self):
        ''' Checks if save score option was ticked
        :return: Boolean
        '''
        return self.player_settings["is_record_score"]

    def write_top_scores(self, max_amt_leaderboard=5):
        ''' When called updates leaderboard with current player. If current player not in
        max amt players for leaderboard, person will not be written down.

        int :param max_amt_leaderboard: Max amount ppl in leaderboard
        :return: None
        '''
        # Get game information to store for leader board
        quiz_mode = self.player_settings["quiz_mode"]  # Gets quiz mode
        quiz_mode = quiz_mode.split("_")  # Splits quiz name into parts EG Question_set_maths -> into 3 segments

        # Check if game mode is custom, (Custom tag is different)
        if quiz_mode[0] != "custom":  # Since custom quiz mode is just custom
            quiz_mode = quiz_mode[2][:-4].title()

        # Get player score info
        percentage_correct = int((self.score / len(self.questions_answered) * 100))
        player_score = "{}/{}".format(self.score, len(self.questions_answered))
        current_player_info = [self.player_settings["player_name"], quiz_mode, player_score, percentage_correct]

        # leader board
        leader_board = []
        leader_board.append(current_player_info)

        # Add existing leaderboards
        with open("TopScores.txt", "r") as file:
            reader = csv.reader(file, delimiter="|")
            for line in reader:
                leader_board.append(line)

        # Sort and cut up to max_amt_leaderboard shown
        leader_board.sort(key=self._sort_key, reverse=True)
        with open("TopScores.txt", "w") as file:
            counter = 1
            for player in leader_board:
                if counter < max_amt_leaderboard+1:
                    write_info = "{}|{}|{}|{}\n".format(player[0], player[1], player[2], player[3])
                    file.write(write_info)
                    counter += 1

    def _sort_key(self, value):
        ''' Private function. Used in write_top_scores(), key for sorting list
        :param value:
        :return: value[3]
        '''
        return int(value[3])

    def on_review_questions_button(self):
        ''' Called when on review questions button pressed. Hides current toplevel and creates new toplevel
        where it reviews answers.
        :return:
        '''
        self.top_level.grab_set()
        self.top_level.withdraw()
        Temp = ReviewQuestionsTopLevel.ReviewAnswers(self.questions_answered, self.top_level)
        self.grab_release()

    def on_play_again_button(self):
        ''' called when play again button pressed. Configs the frame
        '''
        self.top_level.frames["IntroductionFrame"].init_contents()
        self.top_level.show_frame("IntroductionFrame")

