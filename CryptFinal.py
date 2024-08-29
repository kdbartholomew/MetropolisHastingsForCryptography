# metropolis hasting algorithm for crypography
# improved time complexity
# improved score calculation such that we avoid round to 0/ floating point errors
    # log scaling : 
            # take the log then you would add and subtract instead of multiplication and division,
             # and then at the end raise to the power of the final number to convert back to a probability.
    # change points: 
          # iterate thru current decoded message to find where the insances of the 2 letters are.. these are chnage points select i and i-1
            # store chnage point indicies in list
            # calculate score based on that list rather than iterating thru the entire message
            # score of prop/ score of current, consider min
    #using np arrays to vectorize and hopefully handle floating point errors + we can access elements by index instead of iterating over


#input message: NCMXVBICXFVOUEVBF FUVKFOXBVOGCVCMXVNOSPFXBVLXCMGPSVNCXSPVCUVSPHBVICUSHUFUSVOVUFDVUOSHCUVICUIFH FEVHUVQHLFXSKVOUEVEFEHIOSFEVSCVSPFVTXCTCBHSHCUVSPOSVOQQVZFUVOXFVIXFOSFEVFYMOQVUCDVDFVOXFVFUGOGFEVHUVOVGXFOSVIH HQVDOXVSFBSHUGVDPFSPFXVSPOSVUOSHCUVCXVOUKVUOSHCUVBCVICUIFH FEVOUEVBCVEFEHIOSFEVIOUVQCUGVFUEMXFVDFVOXFVZFSVCUVOVGXFOSVLOSSQFNHFQEVCNVSPOSVDOXVDFVPO FVICZFVSCVEFEHIOSFVOVTCXSHCUVCNVSPOSVNHFQEVOBVOVNHUOQVXFBSHUGVTQOIFVNCXVSPCBFVDPCVPFXFVGO FVSPFHXVQH FBVSPOSVSPOSVUOSHCUVZHGPSVQH FVHSVHBVOQSCGFSPFXVNHSSHUGVOUEVTXCTFXVSPOSVDFVBPCMQEVECVSPHBVVLMSVHUVOVQOXGFXVBFUBFVDFVIOUVUCSVEFEHIOSFVDFVIOUVUCSVICUBFIXOSFVDFVIOUVUCSVPOQQCDVSPHBVGXCMUEVSPFVLXO FVZFUVQH HUGVOUEVEFOEVDPCVBSXMGGQFEVPFXFVPO FVICUBFIXOSFEVHSVNOXVOLC FVCMXVTCCXVTCDFXVSCVOEEVCXVEFSXOISVSPFVDCXQEVDHQQVQHSSQFVUCSFVUCXVQCUGVXFZFZLFXVDPOSVDFVBOKVPFXFVLMSVHSVIOUVUF FXVNCXGFSVDPOSVSPFKVEHEVPFXFVHSVHBVNCXVMBVSPFVQH HUGVXOSPFXVSCVLFVEFEHIOSFEVPFXFVSCVSPFVMUNHUHBPFEVDCXAVDPHIPVSPFKVDPCVNCMGPSVPFXFVPO FVSPMBVNOXVBCVUCLQKVOE OUIFEVHSVHBVXOSPFXVNCXVMBVSCVLFVPFXFVEFEHIOSFEVSCVSPFVGXFOSVSOBAVXFZOHUHUGVLFNCXFVMBVSPOSVNXCZVSPFBFVPCUCXFEVEFOEVDFVSOAFVHUIXFOBFEVEF CSHCUVSCVSPOSVIOMBFVNCXVDPHIPVSPFKVGO FVSPFVQOBSVNMQQVZFOBMXFVCNVEF CSHCUVSPOSVDFVPFXFVPHGPQKVXFBCQ FVSPOSVSPFBFVEFOEVBPOQQVUCSVPO FVEHFEVHUV OHUVSPOSVSPHBVUOSHCUVMUEFXVGCEVBPOQQVPO FVOVUFDVLHXSPVCNVNXFFECZVOUEVSPOSVGC FXUZFUSVCNVSPFVTFCTQFVLKVSPFVTFCTQFVNCXVSPFVTFCTQFVBPOQQVUCSVTFXHBPVNXCZVSPFVFOXSP
#should spit out gettysburg address... tho its a random hill climber and might climb the wrong hill due to randomness; run again
import numpy as np
import math
import pandas as pd
import random

class Crypt3:
    alphabet = " abcdefghijklmnopqrstuvwxyz"
    # initializes coding function so that every letter of the alphabet maps to itself
    def __init__(self,input_message, alphabet):
        self.input_message = input_message
        self.coding_function_initial = {char: char for char in alphabet}
        self.proposed_coding_function = self.coding_function_initial.copy()
        self.M = pd.read_csv('/Users/catalinabartholomew/Desktop/matrix-spacefirst.csv', header=None)  # put this in constructor?
        self.M_copy = self.M.copy()
        #self.M_copy = self.M_copy
        # Rename the index and columns to integers from 0 to 26
        self.M_copy.index = range(27)
        self.M_copy.columns = range(27)
        self.letter_1 = None
        self.letter_2 = None
        self.change_point_flag = False
        self.change_points_indices = []
        self.value1 = None
        self.value2 = None


    def generate_coding_function(self):
        # Start with the initial coding function
        self.proposed_coding_function = self.coding_function_initial.copy()
        #print("in coding function; initial: ", self.proposed_coding_function)
        #letter 1 and letter 2 should be the values inside the dict that need to be swapped
        self.letter_1, self.letter_2 = random.sample(self.alphabet, 2)  #random.sample ensure distinct elements
        self.value1 = self.proposed_coding_function[self.letter_1]
        self.value2 = self.proposed_coding_function[self.letter_2]
        self.proposed_coding_function[self.letter_1] = self.value2
        self.proposed_coding_function[self.letter_2] = self.value1


    def get_change_point_flag(self, coding_function):
        #reset flag to false
        self.change_point_flag = False
        decoded = self.get_decoded_message(coding_function)
        if self.value1 in decoded or self.value2 in decoded:
            self.change_point_flag = True
        else:
            self.change_point_flag = False
        #return self.change_point_flag

    def get_change_points_indices(self, coding_function):
        #clear change points first
        self.change_points_indices = []
        decoded = self.get_decoded_message(coding_function)
        for i in range(len(decoded)): #needs tosee last letter
            if decoded[i] == self.value1 or decoded[i] == self.value2:
                # found a chnage point
                self.change_points_indices.append(i)

                # #we re trying  to add only the n-1 term if n is change point so we dont run out of bounds in score
                # if i != (len(decoded)-1) and i not in self.change_points_indices: #prevents dupliates in cpi
                #     self.change_points_indices.append(i)
                # if i != 0 and (i - 1) not in self.change_points_indices:
                #     self.change_points_indices.append(i - 1)

#change point indicies will be the same for both proposed adn initial becaus eif the swap was present then at least one of them is in each

    def acceptance_function(self):
        self.get_change_point_flag(self.proposed_coding_function)
        #print(self.change_point_flag)
        if self.change_point_flag == True: # flags wont work because acceptance is called before score and the flags will always be false
            #consider partial score
            #get change point indices
            self.get_change_points_indices(self.proposed_coding_function)#can be either coding function
            acceptance_difference = np.array((self.partial_score(self.proposed_coding_function)) - (self.partial_score(self.coding_function_initial)))
        else: #no change points therefore acceptance ratio is 1... #if score is None
            acceptance_difference = 0 #recall e ^0 is 1
        acceptance_difference_exp = np.exp(acceptance_difference)
        acceptance_min = min(1.0, acceptance_difference_exp)
        u = np.random.uniform(0.0, 1.0)
        if u < acceptance_min:
            # Update the current-best coding function if proposal is accepted
            self.coding_function_initial = self.proposed_coding_function
            #print("in acceptance: Accepted coding function initial: ", self.coding_function_initial)
            #print("accepted!!")
#throws warning: RuntimeWarning: overflow encountered in exp
  #acceptance_difference_exp = np.exp(acceptance_difference)
#calculates aprtial score when there were change points in the proposed... we save the indicies of the changed points and then consider partial score of initial
    def partial_score(self, coding_function):#coding function will always be initial
        partial_score = 0.0  #log scaling
        decoded = self.get_decoded_message(coding_function)
        #print("decoded message: ", decoded)
        #print("value1, value 2: ", self.value1, self.value2)
        #print m location,,

        for index_value in self.change_points_indices:  # generates a list of characters that are chnage points so that we can consider a subset of score
            #gets the index of the chnage points
            #it will enter both if both are true getting all adjacencies
            if index_value > 0: #there is i-1 in bounds
                #get i-1
                index_value_minus = index_value -1
                #compare i -1 and i...; get log of them and add it to partial score
                #error in map... currently undefined.. char list no longer exists... i can access the char of that index by using decoded of index
                #BUT!! decoded[index value] will be different for proposed vs initial,,, BUT!!! WE HANDLE THIS BY PASSING CODING FUNCTION AS AN ARGUMENT!
                #map = np.array([ord(char) - 96 if 97 <= ord(char) <= 122 else 0 for char in char_list])
               # decoded[index value] is not an Mlocation
                M_loc_i = None #is it gonna forget MLoc?
                M_loc_i_minus = None
                M_loc_i_plus = None
                #M_loc need different scope? made a function but im repeating code?
                #doesmtn handle any punctuation. only spaces and lowercase letters
                if ord(decoded[index_value]) >= 97 and ord(decoded[index_value]) <= 122:
                    M_loc_i = ord(decoded[index_value]) -96 #m location of index value
                else:
                    M_loc_i = 0#m location of index value
                if ord(decoded[index_value_minus]) >= 97 and ord(decoded[index_value_minus]) <= 122:
                    M_loc_i_minus = ord(decoded[index_value_minus]) - 96#m location of index value minus
                else:
                    M_loc_i_minus = 0#m location of index value minus
                #print("line 143: mloc minus, m loc i: ", M_loc_i_minus, M_loc_i)
                M_value = self.M_copy.iloc[M_loc_i_minus, M_loc_i]
                M_value_log_scale = np.log(M_value)
                partial_score += M_value_log_scale
            if index_value < len(decoded)-1: # there i s i+1 in bounds
                #get i+1
                index_value_plus = index_value + 1
            # compare i  and i+1...; get log of them and add it to partial score
                if ord(decoded[index_value]) >= 97 and ord(decoded[index_value]) <= 122:
                    M_loc_i = ord(decoded[index_value]) - 96 #m location of i
                else:
                    M_loc_i = 0 #m location of i
                if ord(decoded[index_value_plus]) >= 97 and ord(decoded[index_value_plus]) <= 122:
                    M_loc_i_plus = ord(decoded[index_value_plus]) - 96 #m location of index value plus
                else:
                    M_loc_i_plus = 0 #m location of index value plus
                    #replace decoded[index value with the correct Mloc ... try to re structure to avoid duplicate code.. might need to edit scop of Mvalue
                #print(" line 160: mloc i, m loc i plus: ", M_loc_i, M_loc_i_plus)
                M_value = self.M_copy.iloc[M_loc_i, M_loc_i_plus]
                M_value_log_scale = np.log(M_value)
                partial_score += M_value_log_scale
        return partial_score

    def get_decoded_message(self, coding_function): # can be used to decode any dictionary
        # a dictionary comprehension to map each character in the input message to its corresponding value in the coding function
        # join method converts iterable list into single string
        decoded_message = ''.join(coding_function[char] for char in self.input_message)
        return decoded_message
#main
input_message = str.lower(input("Enter the string you would like to decode: ")) #only considers lower case letters
alphabet = " abcdefghijklmnopqrstuvwxyz"
crypto = Crypt3(input_message, alphabet) # calls constructor and initializes a coding function
string_decoded = ''

for l in range(10000):
    crypto.generate_coding_function()
    crypto.acceptance_function()
    if l % 100 == 0:
        # decode the message using the current coding function
        decoded_message = crypto.get_decoded_message(crypto.coding_function_initial)
        print("Decoded message after", l, "iterations:", decoded_message)
