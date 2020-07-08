"""
Hangman - word guessing game
"""

from typing import List

import os
import random
import sys
import time


FILE_WORDS = "./words.txt"
MAX_ATTEMPTS = 8
MAX_IMG_SIZE = 4096


def load_list(filename: str) -> List[str]:
    """
    Load list of strings from files.

    Arguments:
        filename - filename to be loaded

    Returns:
        List of lines

    Raises:
        PermissionError, FileNotFoundError
    """

    with open(filename, encoding="UTF-8") as f:  # pylint: disable=C0103
        return list(f.readlines())


def copy_letter(letter: str, source: str, target: str) -> str:
    """
    Copy letters from source string to same positions to target.

    Arguments:
        letter - copied letter
        source - source string
        target - target string

    Returns:
        Target string with letter copied from source
    """

    low_letter: str = letter.lower()
    result: str = target
    for idx, value in enumerate(source):
        if value.lower() == low_letter:
            result = result[:idx] + letter + result[idx + 1:]
    return result


def clear_screen():
    """
    Clear console screen.
    """

    cmd: str = "cls" if os.name == "nt" else "clear"
    os.system(cmd)


def draw_hangman(misses: int = 0):
    """
    Draw a hangman picture based on number of misses.

    Arguments:
        misses - number of wrong answers so far

    Raises:
        FileNotFoundException
    """

    def _load_img(num: int) -> str:
        result: str = ""
        filename: str = f"images/{num:02}.txt"
        with open(filename) as source_file:
            result = source_file.read(MAX_IMG_SIZE)
        return result

    clear_screen()
    if misses == 0:
        print("\n" * 10)
    else:
        img: str = _load_img(misses)
        print(img)


def hangman_game(secret: str, attempts: int = MAX_ATTEMPTS):
    """
    The Hangman game.
    Player tries to guess a secret words entering a single letter.
    After 8 misses player looses the game.

    Arguments:
        secret - a secret word player tries to guess

    Raises:
        ValueError in case of empty secret
    """

    if len(secret) < 1:
        raise ValueError("Empty secret word")

    guess: str = "-" * len(secret)
    wrong: str = ""

    misses: int = 0
    while misses < attempts:
        print(f"\nSecret word:  {guess}\n")
        print(f"Tried so far: {wrong}\n")
        letter = input("Try to guess a letter: ")

        if not letter.isalpha():
            print("You have to enter a letter. Try again")
        elif letter in guess:
            print("The letter has been already discovered. Try another.")
        elif letter not in secret:
            if letter not in wrong:
                wrong = wrong + letter + " "
            misses += 1
            draw_hangman(misses)
        else:  # Ok
            guess = copy_letter(letter, secret, guess)
            if guess == secret:
                print(f"\nCongratulations!\nYou've succesfully found the secret word '{guess}'.")
                break

    if misses >= attempts:
        print("You've been hanged. What a bad luck!")


def main():
    """
    Main program function.
    """

    print("H A N G M A N\n")
    print(
        "You've been sentenced to death. The only way\n"
        "to save yourself is to guess a secret word.\nGood luck!\n")

    try:
        words: List[str] = load_list(
            sys.argv[1] if len(sys.argv) > 1 else FILE_WORDS
        )

        hangman_game(random.choice(words).strip())
    except FileNotFoundError:
        print("Error: Words could not be loaded.", file=sys.stderr)
    except PermissionError:
        print("Error: You do not have permission to read the words file.", file=sys.stderr)
    except IndexError:
        print("Error: Can't select secret, list is empty.", file=sys.stderr)
    except ValueError:
        print("Error: Secret cannnot be empty.", file=sys.stderr)
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)


main()
