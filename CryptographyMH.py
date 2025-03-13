import numpy as np
import pandas as pd
import random

class CryptographyMH:
    alphabet = " abcdefghijklmnopqrstuvwxyz"

    def __init__(self, input_message, alphabet):
        """
        Initializes the Crypt3 class with the input message and alphabet.
        
        Args:
            input_message (str): The message to be encoded or decoded.
            alphabet (str): The alphabet used for encoding and decoding.
        """
        self.input_message = input_message
        self.coding_function_initial = {char: char for char in alphabet}
        self.proposed_coding_function = self.coding_function_initial.copy()
        self.M = pd.read_csv('matrix-spacefirst.csv', header=None)
        self.M_copy = self.M.copy()
        self.M_copy.index = range(27)
        self.M_copy.columns = range(27)
        self.letter_1 = None
        self.letter_2 = None
        self.change_point_flag = False
        self.change_points_indices = []
        self.value1 = None
        self.value2 = None

    def generate_coding_function(self):
        """
        Generates a new coding function by swapping two random letters in the alphabet.
        """
        self.proposed_coding_function = self.coding_function_initial.copy()
        self.letter_1, self.letter_2 = random.sample(self.alphabet, 2)
        self.value1 = self.proposed_coding_function[self.letter_1]
        self.value2 = self.proposed_coding_function[self.letter_2]
        self.proposed_coding_function[self.letter_1] = self.value2
        self.proposed_coding_function[self.letter_2] = self.value1

    def get_change_point_flag(self, coding_function):
        """
        Sets the change_point_flag based on whether the proposed coding function affects the decoded message.
        
        Args:
            coding_function (dict): The coding function to be evaluated.
        """
        self.change_point_flag = False
        decoded = self.get_decoded_message(coding_function)
        if self.value1 in decoded or self.value2 in decoded:
            self.change_point_flag = True

    def get_change_points_indices(self, coding_function):
        """
        Identifies the indices of change points in the decoded message based on the proposed coding function.
        
        Args:
            coding_function (dict): The coding function to be evaluated.
        """
        self.change_points_indices = []
        decoded = self.get_decoded_message(coding_function)
        for i in range(len(decoded)):
            if decoded[i] == self.value1 or decoded[i] == self.value2:
                self.change_points_indices.append(i)

    def acceptance_function(self):
        """
        Determines whether to accept the proposed coding function based on the acceptance ratio.
        """
        self.get_change_point_flag(self.proposed_coding_function)
        if self.change_point_flag:
            self.get_change_points_indices(self.proposed_coding_function)
            acceptance_difference = np.array(self.partial_score(self.proposed_coding_function) - self.partial_score(self.coding_function_initial))
        else:
            acceptance_difference = 0
        acceptance_difference_exp = np.exp(acceptance_difference)
        acceptance_min = min(1.0, acceptance_difference_exp)
        u = np.random.uniform(0.0, 1.0)
        if u < acceptance_min:
            self.coding_function_initial = self.proposed_coding_function

    def partial_score(self, coding_function):
        """
        Computes the partial score of the coding function based on change points.
        
        Args:
            coding_function (dict): The coding function to be evaluated.
        
        Returns:
            float: The partial score of the coding function.
        """
        partial_score = 0.0
        decoded = self.get_decoded_message(coding_function)
        for index_value in self.change_points_indices:
            if index_value > 0:
                index_value_minus = index_value - 1
                M_loc_i = ord(decoded[index_value]) - 96 if 97 <= ord(decoded[index_value]) <= 122 else 0
                M_loc_i_minus = ord(decoded[index_value_minus]) - 96 if 97 <= ord(decoded[index_value_minus]) <= 122 else 0
                M_value = self.M_copy.iloc[M_loc_i_minus, M_loc_i]
                partial_score += np.log(M_value)
            if index_value < len(decoded) - 1:
                index_value_plus = index_value + 1
                M_loc_i = ord(decoded[index_value]) - 96 if 97 <= ord(decoded[index_value]) <= 122 else 0
                M_loc_i_plus = ord(decoded[index_value_plus]) - 96 if 97 <= ord(decoded[index_value_plus]) <= 122 else 0
                M_value = self.M_copy.iloc[M_loc_i, M_loc_i_plus]
                partial_score += np.log(M_value)
        return partial_score

    def get_decoded_message(self, coding_function):
        """
        Decodes the input message using the given coding function.
        
        Args:
            coding_function (dict): The coding function to be used for decoding.
        
        Returns:
            str: The decoded message.
        """
        return ''.join(coding_function[char] for char in self.input_message)

def main():
    """
    Main function to run the Crypt3 encoding/decoding process.
    Prompts the user for an input message or uses a default message from 'test_input.txt'.
    Iteratively applies the Crypt3 algorithm and checks for convergence.
    """
    user_choice = input("Enter your own message or type 'default' to use the message from 'test_input.txt': ").strip().lower()

    if user_choice == 'default':
        input_file = 'test_input.txt'
        try:
            with open(input_file, 'r') as file:
                input_message = file.read().strip().lower()
                print("Using default input from file.")
                print(input_message)
        except FileNotFoundError:
            print(f"Error: The file '{input_file}' was not found.")
            return
    else:
        input_message = user_choice.lower()

    alphabet = " abcdefghijklmnopqrstuvwxyz"
    crypto = CryptographyMH(input_message, alphabet)

    prev_decoded_message = None
    no_change_count = 0
    early_stop_threshold = 8

    for l in range(6000):
        crypto.generate_coding_function()
        crypto.acceptance_function()

        if l % 100 == 0:
            decoded_message = crypto.get_decoded_message(crypto.coding_function_initial)
            print(f"Iteration {l}: {decoded_message[:100]}...")

            if decoded_message == prev_decoded_message:
                no_change_count += 1
                if no_change_count >= early_stop_threshold:
                    print(f"Early stopping at iteration {l} (no change in {early_stop_threshold} consecutive checks).")
                    break
            else:
                no_change_count = 0

            prev_decoded_message = decoded_message

if __name__ == "__main__":
    main()
