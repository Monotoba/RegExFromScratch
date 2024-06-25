# RegEx from Scratch Documentation:
This project is a Python implementation of a Regular Expression Engine from scratch. It provides functionality to convert regular expressions into Non-Deterministic Finite Automata (NFA), match patterns in strings, find all occurrences, search for patterns, split strings based on patterns, and perform substitutions.

## Source Files Documentation:
1. regex_engine.py:
  - Contains functions to build NFAs from parsed regular expressions, convert regular expressions to NFAs, match patterns in strings, find all occurrences, search for patterns, split strings based on patterns, and perform substitutions.
2. nfa.py:
  - Defines the NFA class and functions to create basic NFAs, concatenate NFAs, alternate NFAs, and apply Kleene star operation to NFAs.
3. main.py:
  - Entry point of the program.
  - Demonstrates the usage of the regex engine functions with example patterns and strings.
  - Imports functions from regex_engine.py for pattern matching, finding all occurrences, searching, splitting, and substitution.
4. parser.py:
  - Contains a function to parse regular expressions into a format suitable for building NFAs.
  - Defines precedence rules for operators in regular expressions.

## Class Documentation:

1. NFA Class:
  - Attributes:
    - start_state: The starting state of the NFA.
    - accept_state: The accepting state of the NFA. 
  - Methods:
    - create_basic_nfa(char): Creates a basic NFA for a single character.
    - concatenate_nfa(nfa1, nfa2): Concatenates two NFAs.
    - alternate_nfa(nfa1, nfa2): Alternates between two NFAs.
    - kleene_star_nfa(nfa): Applies the Kleene star operation to an NFA
2. Parser Functions:
  - parse_regex(pattern): Parses a regular expression into a format suitable for building NFAs.
3. Regex Engine Functions:
    - build_nfa(parsed_regex, alphabet): Builds an NFA from a parsed regular expression.
    - regex_to_nfa(pattern, alphabet): Converts a regular expression to an NFA.
    - match(pattern, string, alphabet): Matches a pattern in a string using an NFA.
    - findall(pattern, string, alphabet): Finds all occurrences of a pattern in a string.
    - search(pattern, string, alphabet): Searches for a pattern in a string.
    - split(pattern, string, alphabet): Splits a string based on a pattern.
    - sub(pattern, replacement, string, alphabet): Performs substitution in a string based on a pattern.

This documentation provides an overview of the project structure, functionality, and individual components for better understanding and usage.

Source: /home/randy/projects/python-3/RegExFromScratch/src/
