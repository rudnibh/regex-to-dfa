import sys
from graphviz import Digraph


class State:
    def __init__(self, is_end=False):
        self.is_end = is_end
        self.transitions = {}
        self.epsilon_transitions = []

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.append(state)


class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.end.is_end = True

    def __str__(self):
        s = ""
        # do a bfs to print all the states
        q = [self.start]
        visited = {self.start}
        # map states to names
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
            for state in curr.epsilon_transitions:
                if state not in visited:
                    visited.add(state)
                    q.append(state)
                    state_names[state] = f"q{i}"
                    i += 1
                s += f"{curr_name} -> {state_names[state]} (epsilon)\n"
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
            for state in curr.epsilon_transitions:
                if state not in visited:
                    visited.add(state)
                    q.append(state)
                    state_names[state] = f"q{i}"
                    i += 1
                dot.edge(curr_name, state_names[state], label="ε")
        dot.render("nfa", view=True)


class NFABuilder:
    def __init__(self, postfix_regex):
        self.postfix_regex = postfix_regex
        self.nfa_stack = []

    def _char(self, char):
        start = State()
        end = State(is_end=True)
        start.add_transition(char, end)
        self.nfa_stack.append(NFA(start, end))

    def _concat(self):
        nfa2 = self.nfa_stack.pop()
        nfa1 = self.nfa_stack.pop()
        nfa1.end.is_end = False
        nfa1.end.add_epsilon_transition(nfa2.start)
        self.nfa_stack.append(NFA(nfa1.start, nfa2.end))

    def _union(self):
        nfa2 = self.nfa_stack.pop()
        nfa1 = self.nfa_stack.pop()
        start = State()
        start.add_epsilon_transition(nfa1.start)
        start.add_epsilon_transition(nfa2.start)
        end = State(is_end=True)
        nfa1.end.is_end = False
        nfa2.end.is_end = False
        nfa1.end.add_epsilon_transition(end)
        nfa2.end.add_epsilon_transition(end)
        self.nfa_stack.append(NFA(start, end))

    def _kleene(self):
        nfa = self.nfa_stack.pop()
        start = State()
        end = State(is_end=True)
        start.add_epsilon_transition(nfa.start)
        start.add_epsilon_transition(end)
        nfa.end.is_end = False
        nfa.end.add_epsilon_transition(nfa.start)
        nfa.end.add_epsilon_transition(end)
        self.nfa_stack.append(NFA(start, end))

    def build(self):
        for char in self.postfix_regex:
            if char.isalnum() or char == "#":
                self._char(char)
            elif char == ".":
                self._concat()
            elif char == "|":
                self._union()
            elif char == "*":
                self._kleene()
        return self.nfa_stack.pop()
