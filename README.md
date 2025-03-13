# Metropolis Hastings (Optimized to Converge for Large Input)

This project contains my novel optimization of the Metropolis Hastings algorithm for decoding messages. 
The CryptographyMH algorithm uses a coding function to propose random swaps in the mapping of letters.
The algorithm iteratively considers changes to the coding function and accepts them based on an acceptance function's evaluation of the 
partial score of the coding function. If the partial score is above a liklihood threshold, make the proposed change to the coding function. 
Else, flip a weighted coin with the probability of the unlikely change and make the proposed change if the coin flips in favor of the unlikely event.

I think it's important to note that occainanally doing the improbable thing is what makes this algo converge. 

Tranditionally this algo doesnt converge for large input because we consider score (calculated in the acceptance function) as a product of probabilities. As our 
input message gets longer so does this product of probabilities and we face float underflow errors very quickly.

I made these modifications in optimizing this algo for long input sequences:
 - I log scaled (natural log) so we consider a log sum instead of a product (and I exponentiate back before returning).
 - I only consider change points when evaluating the score. That is to say, we only conisder the log sum of the values affected by the most
   recent proposed change.


Input Requirements:
  - Input messages must be generated to ensure a one-to-one (1:1) mapping between characters. Each character, including spaces, must map to only one unique character and cannot have multiple mappings.
  - For example, let a -> c, c -> b, b -> m such that no letter (including space)
     maps to more than one letter.

Fine Tuning:
  - User might need to increase the early stopping criteria or max iterations for exceedingly long inputs.
    
_________________________________________________________________________________________________________________________________________________________

Installation
Step-by-step guide to get the project up and running:


# Clone the repository
git clone https://github.com/your-username/cryptography-mh.git

# Install dependencies
cd cryptography-mh

pip install -r requirements.txt

# How to run the project
python CryptographyMH.py
### When prompted, type 'default' for the test case long message. Else, enter a novel input message such that it satisfies the above requirements.


# Methods
__init__(self, input_message, alphabet)
Initializes the Crypt3 class with the input message and alphabet.

generate_coding_function(self)
Generates a new coding function by swapping two random letters in the alphabet.

get_change_point_flag(self, coding_function)
Sets the change_point_flag based on whether the proposed coding function affects the decoded message.

get_change_points_indices(self, coding_function)
Identifies the indices of change points in the decoded message based on the proposed coding function.

acceptance_function(self)
Determines whether to accept the proposed coding function based on the acceptance ratio.

partial_score(self, coding_function)
Computes the partial score of the coding function based on change points.

get_decoded_message(self, coding_function)
Decodes the input message using the given coding function.

Main Function
The main() function runs the Crypt3 encoding/decoding process. It prompts the user for an input message or uses a default message from test_input.txt. It iteratively applies the Crypt3 algorithm and checks for convergence.
