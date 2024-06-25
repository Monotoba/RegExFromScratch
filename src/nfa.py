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
    nfa2.accept_state.is_final = False
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
