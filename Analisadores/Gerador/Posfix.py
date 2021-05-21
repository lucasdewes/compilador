from collections import deque


def infix_2_postfix(infix_exp):
    precedence = {'*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
    operation_stack = deque()
    postfix_list = []
    token_list = infix_exp.split()

    for token in token_list:
        if token.isidentifier() or token.isdigit():
            postfix_list.append(token)
        elif token == '(':
            operation_stack.extend(token)
        elif token == ')':
            token_on_top = operation_stack.pop()
            while token_on_top != '(':
                postfix_list.append(token_on_top)
                token_on_top = operation_stack.pop()
        else:
            while (not len(operation_stack) == 0) and (precedence[operation_stack[-1]] >= precedence[token]):
                postfix_list.append(operation_stack.pop())
            operation_stack.extend(token)

    while not len(operation_stack) == 0:
        postfix_list.append(operation_stack.pop())
    return ' '.join(postfix_list)
