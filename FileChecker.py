'''
FileChecker.py

**This file is meant to be imported by other packages.**

The purpose of this file is to provide a validation on the question sets.
If question set passes validation check, Nothing is returned. If fails,
It returns an exception and why it was rejected. This is used in the program
to reject incorrect files to prevent program from crashing.

'''
import csv


class InsufficientQuestionsError(Exception):
    ''' This is an custom Exception created for validation'''
    def __init__(self, expression):
        self.expression = expression


def check_question_set(file_name, min_valid_questions=10):
    ''' Checks question set file that:
            - Each line has 6 or 7 values. (Optional image column)
            - Each value is not empty. (Has a value)
            - Answers column is only a, b, c, d (Capitals do not matter)
            - There is a minimum of 10 successful question in question set
    :param file_name: Full name of text file. EG "question_set_maths.txt"
    :return: list failed_lines -> Returned lines that failed file check. If none, list empty
    :return: ValueError -> If there are <30 successful questions in set
    :return: FileNotFoundError -> If file is not found
    :return: Exception -> An unhandled exception is recieved
    '''
    try:
        # Important variables
        current_line_number = 1 # Current line reading
        successful_questions = 0
        failed_lines = [] # Contains ints of lines that have failed validation chec.

        # Reading question set
        file = open(file_name, "r")
        reader = csv.reader(file, delimiter="|")

        # Analysing each line
        for line in reader:
            if len(line) == 0:
                # If there is an empty line, Add to failed lines and continue scanning
                failed_lines.append(current_line_number)
                continue
            elif line[0].strip().upper() == "END":
                # If read "END" Stop reading more questions.
                break
            elif _rows_not_connect(line):
                # Goes to specified validation method, If fails, add to failed lines. Move on to next line
                failed_lines.append(current_line_number)
                current_line_number += 1
            elif _values_empty(line):
                # Goes to specified validation method, If fails, add to failed lines. Move on to next line
                failed_lines.append(current_line_number)
                current_line_number += 1
            elif _ans_col_incorrect(line):
                # Goes to specified validation method, If fails, add to failed lines. Move on to next line
                failed_lines.append(current_line_number)
                current_line_number +=1
            else:
                # Line has passed all validation checks, add 1 to successful question. Move on to next line
                current_line_number +=1
                successful_questions +=1

        file.close() # Close file

        # Check if there is sufficient questions to play game.
        if successful_questions < min_valid_questions:
            # Not enough, Raise error with msg
            raise InsufficientQuestionsError("Not enough sucessful questions in {}. \nPlease check lines {} for errors in {} and/or add more valid questions\nMinimum {} successful questions ".format(file_name, failed_lines, file_name, min_valid_questions))
        else:
            # Sufficient questions to play game, Return failed lines that will be rejected.
            return failed_lines

    # A bunch exceptions likely to occur to catch
    except FileNotFoundError as e:
        return FileNotFoundError("File not found {}. Remember the .txt\n{}".format(file_name, e))
    except InsufficientQuestionsError as e:
        return InsufficientQuestionsError(e)
    except Exception as e:
        # Unknown error
        return Exception("Error reading file {}, Was it a supported txt file?:\n{}".format(file_name, e))


def _rows_not_connect(line):
    ''' Checks there is only 6 or 7 values in each line. (Image optional)
    :param line: List, Values seperated via list
    :return: True -> Correct amt    False -> Incorrect amt
    '''
    if len(line) in (6, 7):
        return False
    else:
        return True


def _values_empty(line):
    '''Check if values are not empty for question, ans1, ans2, ans3, ans4 and acutal ans.
    Does not check image column as it can be empty
    :param line:
    :return: Boolean
    '''
    for i in range(5):
        if line[i].strip() == "":
            return True
    return False


def _ans_col_incorrect(line):
    '''Checks if answer column is only (a, b, c, d).
    :param line: THe line to check
    :return: Boolean
    '''
    if line[5].lower().strip() in ("a", "b", "c", "d"):
        return False
    else:
        return True




