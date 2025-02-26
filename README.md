### Evil Hangman
## Overview
This project is an implementation of Evil Hangman, an adversarial version of the classic Hangman game, where the word-maker dynamically chooses a word as late as possible to maximize the difficulty for the word-guesser. The challenge revolves around selecting efficient data structures and implementing algorithmic strategies to delay revealing the target word while adhering to the rules of the game.

## Highlights
- Efficient Data Structures: The implementation leverages hash tables (dictionaries) to efficiently manage sets of potential words and quickly determine the best response to a guess.
- Dynamic Word Selection: Instead of picking a fixed word at the start, the algorithm dynamically chooses the largest remaining subset of words after each guess, minimizing information given to the player.
- Optimized Partitioning Strategy: Words are grouped based on letter positions rather than just frequency, improving adversarial performance.
- Preprocessing for Speed: The dictionary is preprocessed so that resetting the game can be done in O(1) time.
- Game API Implementation: Implemented core functions like:
  - guess(): Determines the optimal response to a guessed letter.
  - get_valid_word(): Returns a word from the remaining possibilities.
  - get_amount_of_valid_words(): Outputs the current size of the possible word set.
  - get_letter_positions_in_word(): Extracts positions of a letter within a word.

## Applications
- AI Game Development: Showcases the ability to design adversarial AI for games.
- Algorithm Optimization: Demonstrates strategic word selection and efficient set partitioning.
- Data Structures Expertise: Highlights real-world application of hash maps, sets, and dynamic programming.
