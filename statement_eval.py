# File: statement_eval.py
# Author: Alex Bae, Galen Forbes-Roberts, Josue Bautista
# Date: 2/4/2021
# Description: Program that reads and interprets a
#    file containing simple expression and assignment
#    statements.
from pathlib import Path
import re  # For regular expressions

class BadLineError(Exception):
    """
    Whenever a line is deemed invalid, 
    this exception is called and the line is skipped.
    """
    pass
        
def interpret_statements(filename):
    """
    Function that reads statements from the file whose
    name is filename, and prints the result of each statement,
    formatted exactly as described in the psa1 problem statement.  
    interpret_statements must use the evaluate_expression function,
    which appears next in this file.
    """
    try:                                        #error handling for opening files, keep track of count, make dictionary, strip away comments, 
        f = open(filename, 'r')                 #turn each line into lists of individual strings, iterate through each line.
    except OSError:
        print("Cannot open file.")
    count = 0
    variables = {}
    for line in f:
        line_nocomment = line[0:line.find('#')].strip()
        count += 1
        line_tokens = line_nocomment.split()
        if len(line_tokens) > 0:
            try:
                if not IsValid(line_tokens):   #Bad Line Exception. 
                    raise BadLineError
                ret_val = interpret_one_statement(line_tokens,variables)                #calls interpret function to get final result for each line, 
                ret_val = '{:.2f}'.format(ret_val)                                      #convert to 2 decimal places, print all results
                if len(line_tokens) == 1:
                    print('Line {}: {} = {}'.format(count, line_tokens[0], ret_val))
                elif line_tokens[1] == '=':
                    print('Line {}: {} = {}'.format(count, line_tokens[0], ret_val))
                else:
                    print('Line {}: {} = {}'.format(count, line_nocomment, ret_val))
            except:
                print("Line {}: Invalid statement".format(count))
 
def IsValid(line_tokens):
    """
    Function determines whether line is valid or invalid. 
    If statement is valid, it is processed. 
    However, if it is invalid, BadLineError is called and line is passed
    """
    if len(line_tokens) == 0:
        return False
    elif len(line_tokens) == 1:
        return True
    elif line_tokens[-1] == '+' or line_tokens[-1] == '-':
        return False
    elif line_tokens[1] != '=':
        return True
    elif re.fullmatch('[a-zA-Z][\w]*', line_tokens[0]) == None:
        return False
    elif len(line_tokens) % 2 == 0:
        return False
    return True

def interpret_one_statement(tokens, variables):
    """
    Function that evaluates an expression represented by tokens.
    tokens is a list of strings that are the tokens of the expression.  
    For example, if the expression is "salary + time - 150", then tokens would be
    ["salary", "+", "time", "-", "150"].  variables is a dictionary that maps 
    previously assigned variables to their floating point values.

    Returns the value that is assigned.

    If the expression is invalid, the BadStatement exception is raised.
    """
    if len(tokens) == 1:                          #Evaluates lines with only 1 element
        try:
            return float(tokens[0]) 
        except ValueError:
            return variables[tokens[0]]
    if tokens[1] != '=':                        #Evaluates lines without assignment. 
        entire_line = ''                          #Entire line is an expression
        for x in tokens:
            entire_line = entire_line + x        #Use to turn entire line to key
        i = 0 
        l = len(tokens)
        ret_val = get_token_value(tokens[0],variables)
        while i < (l-2):            
            if tokens[i+1] == '+':
                ret_val += get_token_value(tokens[i+2],variables)
            elif tokens[i+1] == '-':
                ret_val -= get_token_value(tokens[i+2],variables)
            else:
                raise BadLineError
            i += 2
        variables[entire_line] = ret_val
    else:                                                            #Evaluates lines with assignments.
        ret_val = get_token_value(tokens[2],variables)               #Lines with '=' on index 1 
        i = 3
        while i < len(tokens):
            if tokens[i] == '+':
                ret_val += get_token_value(tokens[i+1],variables)
            elif tokens[i] == '-':
                ret_val -= get_token_value(tokens[i+1],variables)
            else:
                raise BadLineError
            i += 2
        variables[tokens[0]] = ret_val
    return ret_val
 
def get_token_value(token,variables):
    """
    Individual elements of each line is evaluated.
    If it is a variable, it is input as a key into the dictionary 'variables'
    If it is a number, it is converted to be of type float.
    """
    try:
        n = float(token)
        return n
    except ValueError:
        if token in variables:
            return variables[token]
        else:
            raise BadLineError
if __name__ == "__main__":
    file_name = "statements.txt"  # you can create another file with statements
                                  # and change the name of this variable to that
                                  # filename.
    
    interpret_statements(file_name)