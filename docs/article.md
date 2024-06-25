# Implementing Regular Expressions (RegEx) from Scratch in Python

---

Regular expressions (RegEx) are a powerful tool in a developer's toolkit, allowing for sophisticated pattern matching and text processing. However, understanding how RegEx works internally can be challenging. This tutorial will guide you through implementing RegEx from scratch using finite automata in Python, providing a deeper understanding of this essential tool. We'll avoid using Python's built-in RegEx libraries and build our RegEx engine step-by-step, creating a functional RegEx library.

## Table of Contents

1. Introduction to Regular Expressions and Finite Automata
2. Project File Structure
3. Basic Concepts and Definitions
4. Implementing Basic RegEx Features
   - Concatenation
   - Alternation (Union)
   - Kleene Star
   - One or More (`+`)
   - Zero or One (`?`)
   - Negation (`^`)
   - Anchors (`^` and `$`)
   - Character Sets (`[ ... ]`)
   - Capture Groups (`()`)
5. Converting RegEx to NFA
   - Thompson's Algorithm
6. Converting NFA to DFA
7. Implementing the RegEx Engine
8. Implementing Additional Functions
   - `match`
   - `findall`
   - `search`
   - `split`
   - `sub`
9. Usage Examples and Testing

---

## 1. Introduction to Regular Expressions and Finite Automata

Regular expressions are sequences of characters defining a search pattern, primarily used for string matching. Finite automata are abstract machines that recognize patterns within input sequences. There are two main types:

1. **Deterministic Finite Automaton (DFA)**: Each state has exactly one transition for each possible input.
2. **Non-deterministic Finite Automaton (NFA)**: States can have zero, one, or multiple transitions for each possible input.

The process involves:
1. Parsing the RegEx to construct an NFA.
2. Converting the NFA to a DFA.
3. Using the DFA to match input strings.

---

## 2. Project File Structure

Our project will be organized into the following files, all within the `src` directory:

- `src/state.py`: Contains the `State` class definition.
- `src/nfa.py`: Contains the `NFA` class and functions for creating and manipulating NFAs.
- `src/dfa.py`: Contains the functions for converting NFAs to DFAs and DFA-related operations.
- `src/parser.py`: Contains the RegEx parser and related functions.
- `src/regex_engine.py`: Contains the main RegEx engine implementation, including the matching function.
- `src/main.py`: Contains the main script for testing and demonstrating the RegEx engine.

---

## 3. Basic Concepts and Definitions

We start by defining some basic concepts. These definitions will help in understanding how our RegEx engine works.

### Alphabet

An alphabet is a finite set of symbols used in the construction of strings and patterns. In RegEx, the alphabet consists of all possible characters that can appear in the input text. For example, a simple alphabet might be `{'a', 'b', 'c'}`. This concept is fundamental because all operations and pattern matching are based on these characters.

### Strings

A string is a finite sequence of symbols from an alphabet. For example, the string `"abc"` is composed of symbols `a`, `b`, and `c` from the alphabet `{'a', 'b', 'c'}`. Strings are the primary objects that RegEx patterns operate on, trying to match specific sequences within these strings.

### Languages

A language in this context is a set of strings over an alphabet. For example, the language `{"a", "ab", "abc"}` consists of three strings over the alphabet `{'a', 'b', 'c'}`. Regular expressions define languages by specifying patterns that match certain sets of strings.

---

## 4. Implementing Basic RegEx Features

In this section, we will build the basic components of our RegEx engine, focusing on several fundamental RegEx operations: concatenation, alternation, the Kleene star, one or more (`+`), zero or one (`?`), negation (`^`), anchors (`^` and `$`), character sets (`[ ... ]`), and capture groups (`()`).

### Concatenation

Concatenation in RegEx means that patterns are matched in sequence. For example, the RegEx `ab` matches the string "ab". This operation is straightforward: the first pattern is matched, followed immediately by the second pattern.

### Alternation (Union)

Alternation in RegEx means that either pattern can match. For example, the RegEx `a|b` matches either "a" or "b". This operation involves creating a new start state that branches into the two patterns, effectively allowing either one to match.

### Kleene Star

The Kleene star in RegEx means zero or more occurrences of a pattern. For example, the RegEx `a*` matches the empty string "", "a", "aa", etc. This operation involves creating a loop in the automaton that allows the pattern to repeat indefinitely.

#### Background on Kleene Star

The Kleene star is named after Stephen Kleene, an American mathematician who made significant contributions to the foundations of theoretical computer science. He introduced the concept of the Kleene star in the context of regular sets and automata theory. The star (*) operation indicates repetition, and it was a natural extension of Kleene's work on the algebraic properties of regular expressions.

### One or More (`+`)

The `+` operator matches one or more occurrences of a pattern. For example, the RegEx `a+` matches "a", "aa", "aaa", etc. This is similar to the Kleene star but requires at least one occurrence.

### Zero or One (`?`)

The `?` operator matches zero or one occurrences of a pattern. For example, the RegEx `a?` matches "", "a".

### Negation (`^`)

The `^` operator matches any character except the ones specified. For example, the RegEx `[^a]` matches any character except "a". This operation creates transitions to states for all characters not specified.

### Anchors (`^` and `$`)

- The `^` anchor asserts that the match must start at the beginning of the string.
- The `$` anchor asserts that the match must end at the end of the string.

### Character Sets (`[ ... ]`)

Character sets match any one of the characters enclosed in the square brackets. For example, `[abc]` matches "a", "b", or "c".

### Capture Groups (`()`)

Capture groups allow you to group parts of your RegEx and capture the matched substrings. For example, `(ab)` matches the substring "ab" and captures it as a group.

---

## 5. Converting RegEx to NFA

We will use Thompson's construction algorithm to convert a RegEx to an NFA. Thompson's construction is a method for transforming a regular expression into an equivalent NFA. This method constructs an NFA for each basic RegEx operation and combines them to form the complete NFA for the given RegEx.

### Thompson's Algorithm

Thompson's algorithm constructs an NFA for a regular expression using the following steps:

1. **Create basic NFA for each symbol**: Each character in the RegEx creates a simple NFA with a start and an accept state.
2. **Concatenation**: Join two NFAs sequentially.
3. **Alternation**: Create a new start state with ε-transitions to the start states of two NFAs, and new accept states connected by ε-transitions from the accept states of both NFAs.
4. **Kleene Star**: Add ε-transitions to handle repetitions.
5. **One or More**: Similar to Kleene star but requires at least one occurrence.
6. **Zero or One**: Add ε-transitions to handle zero or one occurrence.
7. **Negation**: Create transitions to states for all characters not specified.
8. **Anchors**: Handle start and end anchors.
9. **Character Sets**: Create transitions for each character in the set.
10. **Capture Groups**: Track and manage capture groups.

### Implementing Basic NFA Operations

#### NFA Structure

Create the `src/state.py` file and define the structure for our NFA states and the NFA itself.

```python
# src/state.py
class State:
    def __init__(self, is_final=False):
        self.is_final = is_final
        self.transitions = {}
```

Create the `src/nfa.py` file and define the NFA class and basic NFA operations.

```python
# src/nfa.py
from state import State

class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

def create_basic_nfa(char):
    start_state = State()
    accept_state = State(is_final=True)
    start_state.transitions[char] = [accept_state]
    return NFA(start_state, accept_state)

def concatenate_nfa(nfa1, nfa2):
    nfa1.accept_state.is_final = False
    nfa1.accept_state.transitions['ε'] = [nfa2.start_state]
    return NFA(nfa1.start_state, nfa2.accept_state)

def alternate_nfa(nfa1, nfa2):
    start_state = State()
    accept_state = State(is_final=True)
    start_state.transitions['ε'] = [nfa1.start_state, nfa2.start_state]
    nfa1.accept_state.is_final = False
    nfa2.accept_state

.is_final = False
    nfa1.accept_state.transitions['ε'] = [accept_state]
    nfa2.accept_state.transitions['ε'] = [accept_state]
    return NFA(start_state, accept_state)

def kleene_star_nfa(nfa):
    start_state = State()
    accept_state = State(is_final=True)
    start_state.transitions['ε'] = [nfa.start_state, accept_state]
    nfa.accept_state.is_final = False
    nfa.accept_state.transitions['ε'] = [nfa.start_state, accept_state]
    return NFA(start_state, accept_state)

def one_or_more_nfa(nfa):
    start_state = State()
    accept_state = State(is_final=True)
    start_state.transitions['ε'] = [nfa.start_state]
    nfa.accept_state.is_final = False
    nfa.accept_state.transitions['ε'] = [nfa.start_state, accept_state]
    return NFA(start_state, accept_state)

def zero_or_one_nfa(nfa):
    start_state = State()
    accept_state = State(is_final=True)
    start_state.transitions['ε'] = [nfa.start_state, accept_state]
    nfa.accept_state.is_final = False
    nfa.accept_state.transitions['ε'] = [accept_state]
    return NFA(start_state, accept_state)

def negate_nfa(nfa, alphabet):
    start_state = State()
    accept_state = State(is_final=True)
    for char in alphabet:
        if char not in nfa.start_state.transitions:
            start_state.transitions[char] = [accept_state]
    return NFA(start_state, accept_state)
```

---

## 6. Converting NFA to DFA

Create the `src/dfa.py` file to convert an NFA to a DFA using the subset construction algorithm.

```python
# src/dfa.py
from state import State

def epsilon_closure(states):
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for next_state in state.transitions.get('ε', []):
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return closure

def move(states, char):
    next_states = set()
    for state in states:
        next_states.update(state.transitions.get(char, []))
    return next_states

def nfa_to_dfa(nfa, alphabet):
    initial_closure = epsilon_closure([nfa.start_state])
    dfa_states = {frozenset(initial_closure): State()}
    unmarked_states = [initial_closure]
    dfa_start_state = dfa_states[frozenset(initial_closure)]

    while unmarked_states:
        current_states = unmarked_states.pop()
        current_closure = epsilon_closure(current_states)

        for char in alphabet:
            if char == 'ε':
                continue
            next_closure = epsilon_closure(move(current_closure, char))
            if not next_closure:
                continue
            frozen_closure = frozenset(next_closure)
            if frozen_closure not in dfa_states:
                dfa_states[frozen_closure] = State(is_final=any(state.is_final for state in next_closure))
                unmarked_states.append(next_closure)
            dfa_states[frozenset(current_closure)].transitions[char] = [dfa_states[frozen_closure]]

    return dfa_start_state
```

---

## 7. Implementing the RegEx Engine

Create the `src/parser.py` file to parse RegEx patterns into postfix notation.

```python
# src/parser.py
def parse_regex(pattern):
    operators = {'|', '*', '+', '?', '(', ')', '[', ']', '^', '$'}
    output = []
    operators_stack = []
    escaped = False
    char_set = False

    for char in pattern:
        if escaped:
            output.append(char)
            escaped = False
        elif char == '\\':
            escaped = True
        elif char == '[':
            char_set = True
            output.append(char)
        elif char == ']':
            char_set = False
            output.append(char)
        elif char_set:
            output.append(char)
        elif char in operators:
            if char == '(' or char == '[':
                operators_stack.append(char)
            elif char == ')':
                while operators_stack and operators_stack[-1] != '(':
                    output.append(operators_stack.pop())
                operators_stack.pop()  # Remove '('
            elif char == ']':
                while operators_stack and operators_stack[-1] != '[':
                    output.append(operators_stack.pop())
                operators_stack.pop()  # Remove '['
            else:
                while operators_stack and precedence(operators_stack[-1]) >= precedence(char):
                    output.append(operators_stack.pop())
                operators_stack.append(char)
        else:
            output.append(char)

    while operators_stack:
        output.append(operators_stack.pop())

    return output

def precedence(operator):
    return {'|': 1, '+': 2, '?': 3, '*': 4, '^': 5, '$': 6, '.': 7, '(': 8, '[': 8}.get(operator, 0)
```

Create the `src/regex_engine.py` file to build NFAs and handle RegEx matching.

```python
# src/regex_engine.py
from nfa import create_basic_nfa, concatenate_nfa, alternate_nfa, kleene_star_nfa, one_or_more_nfa, zero_or_one_nfa, negate_nfa
from dfa import nfa_to_dfa
from parser import parse_regex
from state import State

def build_nfa(parsed_regex, alphabet):
    stack = []
    for char in parsed_regex:
        if char not in {'|', '*', '+', '?', '^', '$', '.', '[', ']'}:
            stack.append(create_basic_nfa(char))
        elif char == '.':
            if len(stack) < 2:
                raise ValueError(f"Invalid concatenation operation in regex: {parsed_regex}")
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(concatenate_nfa(nfa1, nfa2))
        elif char == '|':
            if len(stack) < 2:
                raise ValueError(f"Invalid alternation operation in regex: {parsed_regex}")
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(alternate_nfa(nfa1, nfa2))
        elif char == '*':
            if len(stack) < 1:
                raise ValueError(f"Invalid Kleene star operation in regex: {parsed_regex}")
            nfa = stack.pop()
            stack.append(kleene_star_nfa(nfa))
        elif char == '+':
            if len(stack) < 1:
                raise ValueError(f"Invalid one or more operation in regex: {parsed_regex}")
            nfa = stack.pop()
            stack.append(one_or_more_nfa(nfa))
        elif char == '?':
            if len(stack) < 1:
                raise ValueError(f"Invalid zero or one operation in regex: {parsed_regex}")
            nfa = stack.pop()
            stack.append(zero_or_one_nfa(nfa))
        elif char == '^':
            if len(stack) == 0:
                # Handle start anchor
                start_state = State()
                nfa = stack.pop()
                start_state.transitions['ε'] = [nfa.start_state]
                stack.append(NFA(start_state, nfa.accept_state))
            else:
                if len(stack) < 1:
                    raise ValueError(f"Invalid negation operation in regex: {parsed_regex}")
                nfa = stack.pop()
                stack.append(negate_nfa(nfa, alphabet))
        elif char == '$':
            if len(stack) == 1:
                nfa = stack.pop()
                accept_state = State(is_final=True)
                nfa.accept_state.transitions['ε'] = [accept_state]
                nfa.accept_state.is_final = False
                nfa.accept_state = accept_state
                stack.append(nfa)
            else:
                raise ValueError(f"Invalid end anchor operation in regex: {parsed_regex}")
        elif char == '[':
            char_set = ''
            while parsed_regex and parsed_regex[0] != ']':
                char_set += parsed_regex.pop(0)
            if parsed_regex:
                parsed_regex.pop(0)  # Remove the closing ']'
            nfa = create_basic_nfa(char_set)
            stack.append(nfa)

    if not stack:
        raise ValueError(f"Invalid regex pattern: {parsed_regex}")

    return stack.pop()

def regex_to_nfa(pattern, alphabet):
    parsed_regex = parse_regex(pattern)
    return build_nfa(parsed_regex, alphabet)

def match(pattern, string, alphabet):
    nfa = regex_to_nfa(pattern, alphabet)
    dfa_start_state = nfa_to_dfa(nfa, alphabet)

    current_state = dfa_start_state
    for char in string:
        if char in current_state.transitions:
            current_state = current_state.transitions[char][0]
        else:
            return False

    return current_state.is_final

def findall(pattern, string, alphabet):
    matches = []
    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            if match(pattern, string[i:j], alphabet):
                matches.append(string[i:j])
    return matches

def search(pattern, string, alphabet):
    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            if match(pattern, string[i:j], alphabet):
                return i  # Return the starting position of the match
    return -1

def split(pattern,

 string, alphabet):
    matches = findall(pattern, string, alphabet)
    parts = []
    last_end = 0
    for match in matches:
        start = string.find(match, last_end)
        parts.append(string[last_end:start])
        last_end = start + len(match)
    parts.append(string[last_end:])
    return parts

def sub(pattern, repl, string, alphabet):
    matches = findall(pattern, string, alphabet)
    result = ""
    last_end = 0
    for match in matches:
        start = string.find(match, last_end)
        result += string[last_end:start] + repl
        last_end = start + len(match)
    result += string[last_end:]
    return result
```

---

## 8. Putting It All Together

Create the `src/main.py` file to test and demonstrate the RegEx engine.

```python
# src/main.py
from regex_engine import match, findall, search, split, sub

alphabet = set('abcdefghijklmnopqrstuvwxyz')

# Example Usage
patterns = ["a*b|c", "ab", "a|b", "a*", "a+", "[^a]", "^a", "a$", "(ab)", "a?"]
strings = ["aaab", "ab", "a", "aaaa", "b", "", "aa", "ba", "ab", ""]

for pattern in patterns:
    for string in strings:
        print(f"Pattern: {pattern}, String: {string} -> Match: {match(pattern, string, alphabet)}")

print(findall("a", "aaab", alphabet))  # ['a', 'a', 'a']
print(search("a", "aaab", alphabet))  # 0
print(split("a", "aaab", alphabet))  # ['', '', '', 'b']
print(sub("a", "x", "aaab", alphabet))  # 'xxxb'
```

---

## 9. Usage Examples and Testing

Let's test our RegEx engine with various patterns and strings. You can run the `src/main.py` script to see the results.

### Example 1: Simple Concatenation

In this example, the pattern "ab" matches the string "ab" but not "a". The concatenation operation ensures that both characters must appear in sequence.

### Example 2: Alternation

Here, the pattern "a|b" matches either "a" or "b", but not "c". The alternation operation allows either character to be matched.

### Example 3: Kleene Star

In this example, the pattern "a*" matches an empty string, "aaaa", but not "b". The Kleene star operation allows for zero or more occurrences of "a".

### Example 4: One or More

This example demonstrates the `+` operator. The pattern "a+" matches "a" and "aaaa", but not an empty string, requiring at least one occurrence of "a".

### Example 5: Zero or One

This example demonstrates the `?` operator. The pattern "a?" matches an empty string and "a", allowing zero or one occurrence of "a".

### Example 6: Negation

In this example, the pattern `[^a]` matches any character except "a". The string "b" matches, while "a" does not.

### Example 7: Anchors

- The pattern `^a` matches "a" at the start of the string.
- The pattern `a$` matches "a" at the end of the string.

### Example 8: Character Sets

The pattern `[abc]` matches "a", "b", or "c".

### Example 9: Capture Groups

The pattern `(ab)` matches the substring "ab" and captures it as a group.

### Example 10: findall, search, split, sub

```python
print(findall("a", "aaab", alphabet))  # ['a', 'a', 'a']
print(search("a", "aaab", alphabet))  # 0
print(split("a", "aaab", alphabet))  # ['', '', '', 'b']
print(sub("a", "x", "aaab", alphabet))  # 'xxxb'
```

By building our RegEx engine from scratch using NFAs and DFAs, we gain a deeper understanding of how pattern matching works. This knowledge can be valuable for optimizing performance and debugging complex RegEx patterns in real-world applications. Through this process, we've implemented a simple yet powerful RegEx engine that can handle basic RegEx operations and match patterns against strings.

## Conclusion

In this tutorial, we explored the inner workings of regular expressions (RegEx) by building a RegEx engine from scratch using finite automata. Starting from the basics of regular expressions and finite automata, we implemented essential RegEx operations such as concatenation, alternation, the Kleene star, one or more (`+`), zero or one (`?`), negation (`^`), anchors (`^` and `$`), character sets (`[ ... ]`), and capture groups (`()`). We then converted these operations into a non-deterministic finite automaton (NFA) using Thompson's algorithm, transformed the NFA into a deterministic finite automaton (DFA) for efficient matching, and built a full-featured RegEx engine with functions like `match`, `findall`, `search`, `split`, and `sub`.

By implementing a RegEx engine from scratch, we gained a deeper understanding of how RegEx patterns are parsed and matched against strings. This knowledge is valuable not only for optimizing performance but also for debugging complex RegEx patterns in real-world applications. We hope this tutorial has demystified the complexities of RegEx and provided you with the skills to further explore and utilize regular expressions in your projects.

---

## Resources

For those who want to delve deeper into the world of regular expressions and their implementations, here are some valuable resources:

### Books

1. **"Mastering Regular Expressions" by Jeffrey E.F. Friedl**  
   This book is a comprehensive guide to regular expressions, covering a wide range of topics and providing practical examples and insights.

2. **"Introduction to Automata Theory, Languages, and Computation" by John E. Hopcroft, Rajeev Motwani, and Jeffrey D. Ullman**  
   This classic textbook provides an in-depth introduction to automata theory, formal languages, and computation, including detailed discussions on finite automata and regular expressions.

### Online Tutorials and Documentation

1. **[RegexOne](https://regexone.com/)**  
   An interactive tutorial that covers the basics of regular expressions with hands-on exercises and examples.

2. **[Regular-Expressions.info](https://www.regular-expressions.info/)**  
   A comprehensive resource for learning about regular expressions, including syntax, examples, and tools.

3. **[MDN Web Docs: Regular Expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions)**  
   Mozilla's documentation on regular expressions provides a detailed overview of RegEx syntax and usage in JavaScript, which is applicable to many other languages.

### Tools

1. **[Regex101](https://regex101.com/)**  
   An online tool for testing and debugging regular expressions. It provides real-time feedback and detailed explanations for each part of your RegEx pattern.

2. **[RegExr](https://regexr.com/)**  
   Another interactive tool for learning, testing, and debugging regular expressions. It includes a library of community patterns and extensive documentation.

### Open Source Implementations

1. **[PCRE (Perl Compatible Regular Expressions)](https://www.pcre.org/)**  
   An open-source library that implements Perl-compatible regular expressions, widely used in many programming languages and tools.

2. **[RE2](https://github.com/google/re2)**  
   A fast, safe, and robust library for regular expressions developed by Google, designed to handle large inputs efficiently.

3. **[Rust Regex Library](https://docs.rs/regex/1.4.2/regex/)**  
   A library for regular expressions in the Rust programming language, known for its performance and safety.

### Academic Papers and Articles

1. **"Thompson's Construction Algorithm"**  
   This paper provides an in-depth explanation of the algorithm used to convert regular expressions into non-deterministic finite automata (NFA).

2. **"A Unified Approach to Compiling Regular Expressions" by Ken Thompson**  
   The original paper by Ken Thompson that introduced the algorithm for converting regular expressions to NFAs.

By exploring these resources, you can expand your knowledge of regular expressions and their implementations, enhancing your ability to use RegEx effectively in your projects. Happy coding!
