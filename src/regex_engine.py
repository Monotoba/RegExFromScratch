# src/regex_engine.py
from nfa import create_basic_nfa, concatenate_nfa, alternate_nfa, kleene_star_nfa, one_or_more_nfa, zero_or_one_nfa, \
    negate_nfa, NFA
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

def split(pattern, string, alphabet):
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
