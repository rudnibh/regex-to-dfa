import sys
from graphviz import Digraph

# add the parent directory to the path
sys.path.append(sys.path[0] + "/..")
from backend.nfa_builder import NFA, State


class DFAState:
    def __init__(self, nfa_states, is_end=False):
        self.nfa_states = nfa_states
        self.is_end = is_end
        self.transitions = {}

    def __eq__(self, other):
        return self.nfa_states == other.nfa_states

    def __hash__(self):
        return hash(frozenset(self.nfa_states))


class DFA:
    def __init__(self, start, states):
        self.start = start
        self.states = states

    def __str__(self):
        s = ""
        q = [self.start]
        visited = {self.start}
        state_names = {self.start: "q0"}
        i = 1
        while q:
            curr = q.pop(0)
            curr_name = state_names[curr]
            if curr.is_end:
                s += f"{curr_name} is end state\n"
            for symbol, state in curr.transitions.items():
                if state not in visited:
                    visited.add(state)
                    q.append(state)
                    state_names[state] = f"q{i}"
                    i += 1
                s += f"{curr_name} -> {state_names[state]} ({symbol})\n"
        return s

    def draw(self):
        dot = Digraph()
        q = [self.start]
        visited = {self.start}
        state_names = {self.start: "q0"}
        i = 1
        while q:
            curr = q.pop(0)
            curr_name = state_names[curr]
            if curr.is_end:
                dot.node(curr_name, shape="doublecircle")
            else:
                dot.node(curr_name, shape="circle")
            for symbol, state in curr.transitions.items():
                if state not in visited:
                    visited.add(state)
                    q.append(state)
                    state_names[state] = f"q{i}"
                    i += 1
                dot.edge(curr_name, state_names[state], label=symbol)
        dot.render("dfa", view=True)


class DFAConverter:
    def __init__(self, nfa):
        self.nfa = nfa
        self.alphabet = self._get_alphabet()
        self.dfa_states = []
        self.start_state = None

    def _get_alphabet(self):
        alphabet = set()
        q = [self.nfa.start]
        visited = {self.nfa.start}
        while q:
            curr = q.pop(0)
            for symbol in curr.transitions:
                alphabet.add(symbol)
            for state in curr.epsilon_transitions:
                if state not in visited:
                    visited.add(state)
                    q.append(state)
            for state in curr.transitions.values():
                if state not in visited:
                    visited.add(state)
                    q.append(state)
        return alphabet

    def _epsilon_closure(self, states):
        closure = set(states)
        q = list(states)
        while q:
            curr = q.pop(0)
            for state in curr.epsilon_transitions:
                if state not in closure:
                    closure.add(state)
                    q.append(state)
        return closure

    def _move(self, states, symbol):
        reachable_states = set()
        for state in states:
            if symbol in state.transitions:
                reachable_states.add(state.transitions[symbol])
        return reachable_states

    def convert(self):
        start_nfa_states = self._epsilon_closure({self.nfa.start})
        self.start_state = DFAState(start_nfa_states)
        self.dfa_states.append(self.start_state)
        q = [self.start_state]
        while q:
            curr_dfa_state = q.pop(0)
            for symbol in self.alphabet:
                next_nfa_states = self._epsilon_closure(
                    self._move(curr_dfa_state.nfa_states, symbol)
                )
                if not next_nfa_states:
                    continue
                # check if dfa state already exists
                new_dfa_state = DFAState(next_nfa_states)
                found = False
                for state in self.dfa_states:
                    if state == new_dfa_state:
                        new_dfa_state = state
                        found = True
                        break
                if not found:
                    self.dfa_states.append(new_dfa_state)
                    q.append(new_dfa_state)
                curr_dfa_state.transitions[symbol] = new_dfa_state
        # set end states
        for state in self.dfa_states:
            for nfa_state in state.nfa_states:
                if nfa_state.is_end:
                    state.is_end = True
                    break
        return DFA(self.start_state, self.dfa_states)


if __name__ == "__main__":
    # get regex from command line
    regex = sys.argv[1]
    from backend.regex_parser import RegexParser

    parser = RegexParser(regex)
    nfa = parser.to_nfa()
    converter = DFAConverter(nfa)
    dfa = converter.convert()
    print(dfa)
    dfa.draw()
