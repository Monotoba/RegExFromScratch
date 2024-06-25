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
