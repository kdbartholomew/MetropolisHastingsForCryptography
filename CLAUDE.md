# CLAUDE.md

## How to run

```bash
pip install -r requirements.txt
python CryptographyMH.py
```

Interactive prompt: type a ciphertext message or `default` to use `test_input.txt`.

## Architecture

Single-file project (`CryptographyMH.py`) with one class `CryptographyMH` that breaks simple substitution ciphers using Metropolis-Hastings MCMC.

**Module-level constants:**
- `DEFAULT_ALPHABET` — `" abcdefghijklmnopqrstuvwxyz"` (space + a-z)
- `BIGRAM_MATRIX_PATH` — path to the bigram CSV
- `MAX_ITERATIONS` — 6000
- `CHECK_INTERVAL` — 100 (iterations between convergence checks)
- `EARLY_STOP_THRESHOLD` — 8 (consecutive unchanged checks before stopping)

**Algorithm flow:**
1. Start with identity mapping (no decryption)
2. Each iteration: swap two random letters in the cipher key (`generate_coding_function`)
3. Score the swap via `partial_score` using bigram frequencies from `matrix-spacefirst.csv`
4. Accept/reject the swap probabilistically (`acceptance_function`)
5. Run up to `MAX_ITERATIONS`; early-stop after `EARLY_STOP_THRESHOLD` consecutive unchanged checks (every `CHECK_INTERVAL` iterations)

**Data files:**
- `matrix-spacefirst.csv` — 27x27 bigram transition frequency matrix (space + a-z)
- `test_input.txt` — default encrypted message (the Gettysburg Address)

## Key technical details

- **Log-space scoring:** `partial_score` sums `log(M[i,j])` to avoid floating-point underflow; the acceptance function exponentiates the difference
- **Partial scoring optimization:** Only rescores bigrams at positions affected by the two-letter swap (change points), not the entire message
- **`_char_to_index` helper:** Static method converting characters to bigram matrix indices (0=space, 1-26=a-z), replacing inline `ord()` arithmetic
- **Acceptance:** Standard MH ratio `min(1, exp(score_proposed - score_current))` compared against `uniform(0,1)`
- **Type hints:** All methods have type annotations; `from __future__ import annotations` enables `dict[str, str]` syntax on Python 3.9+
