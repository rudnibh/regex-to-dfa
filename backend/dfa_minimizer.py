import sys
from graphviz import Digraph

from dfa_converter import DFA, DFAState


class DFAMinimizer:
    def __init__(self, dfa):
        self.dfa = dfa
        self.alphabet = self._get_alphabet()
        self.partitions = []

    def _get_alphabet(self):
        alphabet = set()
        for state in self.dfa.states:
            for symbol in state.transitions:
                alphabet.add(symbol)
        return alphabet

    def minimize(self):
        # partition 1: non-final states
        # partition 2: final states
        non_final_states = {s for s in self.dfa.states if not s.is_end}
        final_states = {s for s in self.dfa.states if s.is_end}
        self.partitions = [non_final_states, final_states]
        while True:
            new_partitions = []
            for partition in self.partitions:
                if len(partition) <= 1:
                    new_partitions.append(partition)
                    continue
                split_map = {}
                for state in partition:
                    key = []
                    for symbol in self.alphabet:
                        if symbol in state.transitions:
                            dest_state = state.transitions[symbol]
                            for i, p in enumerate(self.partitions):
                                if dest_state in p:
                                    key.append(i)
                                    break
                        else:
                            key.append(-1)
                    key = tuple(key)
                    if key not in split_map:
                        split_map[key] = set()
                    split_map[key].add(state)
                for s in split_map.values():
                    new_partitions.append(s)
            if len(new_partitions) == len(self.partitions):
                break
            self.partitions = new_partitions
        new_states = []
        state_map = {}
        for i, partition in enumerate(self.partitions):
            is_end = False
            for state in partition:
                if state.is_end:
                    is_end = True
                    break
            new_state = DFAState(frozenset(partition), is_end=is_end)
            new_states.append(new_state)
            for state in partition:
                state_map[state] = new_state
        new_start_state = state_map[self.dfa.start]
        for old_state, new_state in state_map.items():
            for symbol, dest_state in old_state.transitions.items():
                new_state.transitions[symbol] = state_map[dest_state]
        return DFA(new_start_state, new_states)


if __name__ == "__main__":
    regex = sys.argv[1]
    from regex_parser import RegexParser
    from dfa_converter import DFAConverter

    parser = RegexParser(regex)
    nfa = parser.to_nfa()
    converter = DFAConverter(nfa)
    dfa = converter.convert()
    minimizer = DFAMinimizer(dfa)
    minimized_dfa = minimizer.minimize()
    print(minimized_dfa)
    minimized_dfa.draw()
