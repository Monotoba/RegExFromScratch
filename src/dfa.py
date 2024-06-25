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
