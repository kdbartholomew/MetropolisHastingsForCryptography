# Metropolis Hastings (Optimized to Converge for Long Input Sequences)

This project contains my novel optimization of the Metropolis Hastings algorithm for decoding messages.
The CryptographyMH algorithm uses a coding function to propose random swaps in the mapping of letters.
The algorithm iteratively considers changes to the coding function and accepts them based on an acceptance function's evaluation of the
partial score of the coding function. If the partial score is above a likelihood threshold, make the proposed change to the coding function.
Else, flip a weighted coin with the probability of the unlikely change and make the proposed change if the coin flips in favor of the unlikely event.

I think it's important to note that occasionally doing the improbable thing is what makes this algo converge.

Traditionally this algo doesn't converge for large input because we consider score (calculated in the acceptance function) as a product of probabilities. As our
input message gets longer so does this product of probabilities and we face float underflow errors very quickly.

I made these modifications in optimizing this algo for long input sequences:
 - I log scaled (natural log) to consider a log sum instead of a product (and I exponentiate back before returning).
 - I only consider change points when evaluating the score. That is to say, I only consider the log sum of the values affected by the most
   recent proposed change.

Input Requirements:
  - Input messages must be generated to ensure a one-to-one (1:1) mapping between characters. Each character, including spaces, must map to only one unique character and cannot have multiple mappings.
  - For example, let a -> c, c -> b, b -> m such that no letter (including space)
     maps to more than one letter.

Early Stopping:
  - The algorithm checks for convergence every 100 iterations and stops after 8 consecutive unchanged checks. This means the output may appear stable for up to 800 iterations before stopping. These extra iterations are intentional — MCMC can plateau at a local optimum for hundreds of iterations before a lucky swap escapes it. A stricter threshold (e.g., 2-3 checks) risks stopping prematurely at a suboptimal decoding. The current threshold of 8 balances patience with efficiency.

Fine Tuning:
  - User might need to increase the early stopping criteria or max iterations for exceedingly long inputs.

---

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd cryptography-mh

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python CryptographyMH.py
```

When prompted, type `default` for the test case long message. Otherwise, enter a novel input message that satisfies the above requirements.

## Methods

- `__init__(self, input_message, alphabet)` — Initializes the CryptographyMH class with the input message and alphabet.
- `generate_coding_function(self)` — Generates a new coding function by swapping two random letters in the alphabet.
- `get_change_point_flag(self, coding_function)` — Sets the `change_point_flag` based on whether the proposed coding function affects the decoded message.
- `get_change_points_indices(self, coding_function)` — Identifies the indices of change points in the decoded message based on the proposed coding function.
- `acceptance_function(self)` — Determines whether to accept the proposed coding function based on the acceptance ratio.
- `partial_score(self, coding_function)` — Computes the partial score of the coding function based on change points.
- `get_decoded_message(self, coding_function)` — Decodes the input message using the given coding function.

### Main Function

The `main()` function runs the CryptographyMH encoding/decoding process. It prompts the user for an input message or uses a default message from `test_input.txt`. It iteratively applies the CryptographyMH algorithm and checks for convergence.
