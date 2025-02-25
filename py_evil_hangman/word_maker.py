from __future__ import annotations
from collections import defaultdict # You might find this useful
import os

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

class WordMakerHuman():
    def __init__(self, words_file, verbose):
        # we need to prompt the player for a word, then clear the screen so that player 2 doesn't see the word.
        self.verbose = verbose
        self.words = {} # Make sure that you understand dictionaries. They will be extremely useful for this project.
        with open(words_file) as wordfile:
            for line in wordfile:
                word = line.strip()
                if len(word) > 0:
                    self.words[word] = True # I could have made this a set() instead.

    def reset(self, word_length):
        # Your AI code should not call input() or print().
        question = ""
        while True:
            question = input(f"Please type in your word of length {word_length}: ")
            if question in self.words and len(question) == word_length:
                break
            print("Invalid word.")
        if not self.verbose:
            print("\n" * 100) # Clear the screen
        self.word = question

    def get_valid_word(self):
        return self.word

    def get_amount_of_valid_words(self):
        return 1 # the only possible word is self.word

    def guess(self, guess_letter):
        idx = self.word.find(guess_letter)
        ret = []
        while idx != -1:
            ret.append(idx)
            idx = self.word.find(guess_letter, idx + 1)
        return ret




class WordMakerAI():
    """
    A new WordMakerAI is instantiated every time you launch the game with evil_hangman.py.
    (However, the test harness can make multiple instances.)
    Between games, the reset() function is called. This should clear any internal gamestate that you have.
    The number of guesses, input gathering, winning, losing, etc. is all managed by the GameManager, so you don't
     have to prompt the user at all. All you need to do is keep track of the active dictionary of still-valid words
     in this game.

    Do not assume anything about the lengths of the words. You will be tested on dictionaries with extremely long words.
    """
    def __init__(self, words_file: str, verbose=False):
        # This initializer should read in the words into any data structures you see fit
        # The input format is a file of words separated by newlines
        # Use open() to open the file, and remember to split up words by word length!

        # Feel free to use this parameter to toggle extra print statments. Verbose mode can be turned on via the --verbose flag.
        self.verbose = verbose
        self.words_by_length: Dict[int, Set[str]] = defaultdict(set)
        self.active_words = set()

        # Use this code if you like.

        with open(words_file) as file_obj:
            for line in file_obj:
                word = line.strip().lower()
                if word:
                    self.words_by_length[len(word)].add(word)
                # Use word


        pass # TODO: implement this

    def reset(self, word_length: int) -> None:
        # This function starts a new game with a word length of `word_length`. This will always be called before guess() or get_valid_word() are called.
        # You should try to make this function should be O(1). That is, you shouldn't have to process over the entire dictionary here (find somewhere else to preprocess it)
        # Your AI code should not call input() or print().
        self.active_words = self.words_by_length[word_length].copy()
        pass # TODO: implement this

    def get_valid_word(self) -> str:
        # Get a valid word in the active dictionary, to return when you lose
        # Can return any word, as long as it satisfies the previous guesses
        return next(iter(self.active_words))
        pass # TODO: implement this

    def get_amount_of_valid_words(self) -> int:
        # This function gets the total amount of possible words "remaining" (i.e., that satisfy all the guesses since self.reset was last called)
        # This should also be O(1)
        # Note: This is used extensively in the autograder! Be sure to verify that this function works
        # via the provided test cases.
        # You can see this number by running with the verbose flag, i.e. `python3 evil_hangman.py --verbose`
        return len(self.active_words)
        pass # TODO: implement this

    def get_letter_positions_in_word(self, word: str, guess_letter: str) -> tuple[int, ...]:
        # This function should return the positions of guess_letter in word. For instance:
        #  get_letter_positions_in_word("hello", "l") should return (2, 3). The list should
        #  be sorted ascending and 0-indexed.
        # You can assume that word is lowercase with at least length 1 and guess_letter has exactly length 1 and is a lowercase a-z letter.
        return tuple(i for i, char in enumerate(word) if char == guess_letter)
        # Note: to convert from a list to a tuple, call tuple() on the list. For instance:
        # result = []
        # TODO: add letter positions to result
        # return tuple(result)
        

    def guess(self, guess_letter) -> list[int]:
        # This is the meat of the project. This function is called by the GameManager.
        # Using get_letter_positions_in_word, this function should sort all remaining words
        #  into their respective letter families. Then, it should pick the largest family,
        #  resolving ties by picking the set with fewer guess_letters. If the amount of
        #  guess_letter's are equal, then either set can be picked to become the new active
        #  dictionary.
        # This function should return the positions of where a guess_letter should appear.
        # For instance, if you want an "e" to appear in positions 0 and 2, return [0, 2].
        # Make sure the list is sorted.
        families: Dict[Tuple[int, ...], Set[str]] = defaultdict(set)

        for word in self.active_words:
            positions = self.get_letter_positions_in_word(word, guess_letter)
            families[positions].add(word)

        max_family_size = max(len(words) for words in families.values())
        largest_families = [positions for positions, words in families.items() if len(words) == max_family_size]

        if len(largest_families) > 1:
            fewest_occurrences = min(sum(1 for pos in positions if pos != -1) for positions in largest_families)
            largest_families = [positions for positions in largest_families if
                                sum(1 for pos in positions if pos != -1) == fewest_occurrences]

        chosen_family = largest_families[0]

        self.active_words = families[chosen_family]

        return list(chosen_family)
        # Here is an example run of guess():
        #  If the guess is "a" and the words left are ["ah", "ai", "bo"], then we should return [0], because
        #  we are picking the family of words with an "a" in the 0th position. If this function decides that the biggest family
        #  has no a's, then we would have returned [].

        # In the case of a tie (multiple families have the same amount of words), we should pick the set of words with fewer guess_letter's.
        #  That is, if the guess is "a" and the words left are ["ah", "hi"], we should return [] (picking the set ["hi"]), 
        #  since ["hi"] and ["ah"] are equal length and "hi" has fewer a's than "ah".
        # Again, if both sets have an equal number of guess_letter's, then it is ok to pick either.
        #  For example, if the guess is "a" and the words left are ["aha", "haa"], you can return either [0, 2] or [1, 2].

        # The order of the returned list should be sorted. You can assume that 'guess_letter' has not been seen yet since the last call to self.reset(),
        #  and that guess_letter has len of 1 and is a lowercase a-z letter.
        
        pass # TODO: implement this
