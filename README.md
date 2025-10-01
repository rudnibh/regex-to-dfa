# Regex to DFA Converter

This project is an interactive tool to convert regular expressions (Regex) into Deterministic Finite Automata (DFA) and visualize the process.

## Features

*   **Regex Parsing**: Tokenizes the input regular expression.
*   **NFA Construction**: Builds a Non-deterministic Finite Automaton (NFA) from the parsed regex using Thompson's Algorithm.
*   **NFA to DFA Conversion**: Converts the NFA into a DFA using the subset construction algorithm.
*   **DFA Minimization**: Minimizes the DFA to have the fewest possible states.
*   **Interactive Visualization**: Displays the NFA, DFA, and minimized DFA graphs.
*   **String Testing**: Tests if a string is accepted by the generated DFA.

## Project Structure

```
regex_to_dfa/
│
├─ backend/
│   ├─ regex_parser.py       # Parses regex
│   ├─ nfa_builder.py        # Builds NFA
│   ├─ dfa_converter.py      # Converts NFA → DFA
│   ├─ dfa_minimizer.py      # Minimizes DFA
│   └─ api.py                # Flask/FastAPI server
│
├─ frontend/
│   ├─ index.html
│   ├─ style.css
│   └─ script.js            # Visualization logic
│
└─ README.md
```

## Tech Stack

*   **Backend**: Python, Flask, Graphviz, AutomataLib
*   **Frontend**: HTML, CSS, JavaScript, D3.js, Viz.js
