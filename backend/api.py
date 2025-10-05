from flask import Flask, jsonify, request
from flask_cors import CORS
import sys

sys.path.append(sys.path[0] + "/..")
from backend.regex_parser import RegexParser
from backend.dfa_converter import DFAConverter
from backend.dfa_minimizer import DFAMinimizer

app = Flask(__name__)
CORS(app)


def get_graph_dot(graph):
    dot = "digraph G {\n"
    q = [graph.start]
    visited = {graph.start}
    state_names = {graph.start: "q0"}
    i = 1
    while q:
        curr = q.pop(0)
        curr_name = state_names[curr]
        if curr.is_end:
            dot += f'  {curr_name} [shape=doublecircle];\n'
        else:
            dot += f'  {curr_name} [shape=circle];\n'
        for symbol, state in curr.transitions.items():
            if state not in visited:
                visited.add(state)
                q.append(state)
                state_names[state] = f"q{i}"
                i += 1
            dot += f'  {curr_name} -> {state_names[state]} [label="{symbol}"];\n'
        #also consider epsilon transitions for nfa
        if hasattr(curr, "epsilon_transitions"):
            for state in curr.epsilon_transitions:
                if state not in visited:
                    visited.add(state)
                    q.append(state)
                    state_names[state] = f"q{i}"
                    i += 1
                dot += f'  {curr_name} -> {state_names[state]} [label="ε"];\n'
    dot += "}"
    return dot


@app.route("/convert", methods=["POST"])
def convert():
    regex = request.json["regex"]
    parser = RegexParser(regex)
    nfa = parser.to_nfa()
    dfa = DFAConverter(nfa).convert()
    minimized_dfa = DFAMinimizer(dfa).minimize()

    nfa_dot = get_graph_dot(nfa)
    dfa_dot = get_graph_dot(dfa)
    minimized_dfa_dot = get_graph_dot(minimized_dfa)

    return jsonify(
        {
            "nfa": nfa_dot,
            "dfa": dfa_dot,
            "minimized_dfa": minimized_dfa_dot,
        }
    )


@app.route("/test", methods=["POST"])
def test():
    regex = request.json["regex"]
    string = request.json["string"]
    parser = RegexParser(regex)
    nfa = parser.to_nfa()
    dfa = DFAConverter(nfa).convert()
    minimized_dfa = DFAMinimizer(dfa).minimize()

    curr = minimized_dfa.start
    for char in string:
        if char in curr.transitions:
            curr = curr.transitions[char]
        else:
            return jsonify({"accepted": False})
    return jsonify({"accepted": curr.is_end})


if __name__ == "__main__":
    app.run(debug=True)
