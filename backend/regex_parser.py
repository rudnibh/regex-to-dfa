import sys

sys.path.append(sys.path[0] + "/..")
from backend.nfa_builder import NFA, State, NFABuilder


class RegexParser:
    def __init__(self, regex):
        regex = regex.replace("+", "|")
        self.regex = regex
        self.postfix_regex = self._to_postfix()

    def _add_concat_operator(self):
        output = ""
        for i in range(len(self.regex)):
            output += self.regex[i]
            if i + 1 < len(self.regex):
                c1 = self.regex[i]
                c2 = self.regex[i+1]
                if (c1.isalnum() or c1 in '*?)') and (c2.isalnum() or c2 == '('):
                    output += "."
        return output

    def _to_postfix(self):
        # convert infix regex to postfix
        infix = self._add_concat_operator()
        postfix = ""
        stack = []
        precedence = {"*": 3, ".": 2, "|": 1}
        for char in infix:
            if char.isalnum() or char == "#":
                postfix += char
            elif char == "(":
                stack.append(char)
            elif char == ")":
                while stack and stack[-1] != "(":
                    postfix += stack.pop()
                stack.pop()
            else:
                while (
                    stack
                    and stack[-1] != "("
                    and precedence.get(char, 0) <= precedence.get(stack[-1], 0)
                ):
                    postfix += stack.pop()
                stack.append(char)
        while stack:
            postfix += stack.pop()
        return postfix

    def to_nfa(self):
        return NFABuilder(self.postfix_regex).build()


if __name__ == "__main__":
    regex = sys.argv[1]
    parser = RegexParser(regex)
    print(f"Infix: {parser.regex}")
    print(f"Postfix: {parser.postfix_regex}")
    nfa = parser.to_nfa()
    print(nfa)
    nfa.draw()
