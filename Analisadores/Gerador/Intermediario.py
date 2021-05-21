from collections import deque
from Gerador.Posfix import infix_2_postfix

import os

def logical_symbols(symb):
    logic_identifiers = {'>': '<=', '<': '>=', '>=': '<', '<=': '>', '<>': '==', '==': '<>'}

    return logic_identifiers[symb]


def make_expression(token_exp, line_token_exp):
    expression = []
    line_exp = line_token_exp + 1

    while not ('tk_final' in token_exp[line_exp]):
        expression.append(token_exp[line_exp].split(',')[1])
        line_exp += 1

    return ' '.join(expression)


def make_statement(expression, lexeme, pre_code):
    t = 1
    expression = expression[0].split()
    values = []
    operator = ['+', '-', '*', '/']
    for statement in range(len(expression)):
        if expression[statement] in operator:
            first_operand = values.pop()
            second_operand = values.pop()
            if statement == len(expression) - 1:
                pre_code.append(f'{lexeme} := {second_operand} {first_operand} {expression[statement]}')
            else:
                pre_code.append(f't{t} := {second_operand} {first_operand} {expression[statement]}')
                values.append(f't{t}')
                t += 1
        else:
            values.append(expression[statement])
    if len(values) > 0:
        pre_code.append(f'{lexeme} := {values[0]}')


def intermediate_code(tokens_list, start, loop, pre_code, *output, **flags):
    loop_counter = loop
    line = start
    label_stack = deque()

    count_if = 0
    count_else = 0
    loop_flag = False
    if_statement = flags.get('if_statement_flag')
    else_statement = flags.get('else_statement_flag')
    do_statement = flags.get('do_statement_flag')
    while_statement = flags.get('while_statement_flag')

    while line < len(tokens_list):
        token_readed = tokens_list[line].split(',')[0]

        if 'inputKey' == token_readed:
            pre_code.append('READ ' + tokens_list[line + 2].split(',')[1])

        elif 'outputKey' == token_readed:
            pre_code.append('WRITE ' + tokens_list[line + 2].split(',')[1])

        elif 'tk_atrib' == token_readed:
            reverse_polish_notation = [str(infix_2_postfix(make_expression(tokens_list, line))),
                                       infix_2_postfix(make_expression(tokens_list, line))]
            make_statement(reverse_polish_notation, tokens_list[line - 1].split(',')[1], pre_code)

        elif 'int' == token_readed:
            pre_code.append('INT ' + tokens_list[line + 1].split(',')[1])

        elif 'if' == token_readed:
            if_statement = True
            count_if += 1

            # Labels Controller
            loop_counter += 1
            else_label = loop_counter

            # If Printer
            pre_code.append('IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
                            logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
                            tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(else_label))
            label_stack.append(else_label)

        elif 'else' == token_readed:
            # Else Controller
            count_else += 1
            count_if -= 1

            # Label Controller
            if_exit = label_stack.pop()
            else_label = label_stack.pop()

            # Label Printer
            pre_code.append('GOTO _L' + str(if_exit))
            # print('GOTO _L' + str(if_exit))
            label_stack.append(if_exit)
            pre_code.append('_L' + str(else_label) + ':')

        elif 'while' == token_readed:
            loop_flag = True

            loop_counter += 1
            loop_back = loop_counter
            loop_counter += 1
            loop_exit = loop_counter

            pre_code.append('_L' + str(loop_back) + ': IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
                            logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
                            tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(loop_exit))
            label_stack.append(loop_back)
            label_stack.append(loop_exit)

        elif 'tk_fecha_bloco' in token_readed and label_stack:
            # if if_statement is True and tokens_list[line + 1].split(',')[1] == 'else':
            if loop_flag is True:
                loop_exit = label_stack.pop()
                loop_back = label_stack.pop()

                pre_code.append('GOTO _L' + str(loop_back))
                pre_code.append('_L' + str(loop_exit) + ':')

            elif tokens_list[line + 1].split(',')[1] == 'else':
                loop_counter += 1
                if_exit = loop_counter
                label_stack.append(if_exit)
                line += 1
                continue
            elif tokens_list[line + 1].split(',')[1] != 'else':
                count_if -= 1
                if_exit = label_stack.pop()
                pre_code.append('_L' + str(if_exit) + ':')

        elif 'tk_fecha_bloco' in token_readed and label_stack:
            count_else -= 1
            if_exit = label_stack.pop()
            pre_code.append('_L' + str(if_exit) + ':')
            # print('_L' + str(if_exit) + ':')

        line += 1

    if output[0] is True:
        try:
            with open(output[1] + '.ic', 'w+', encoding='utf-8') as ic_file:
                for pre_code_line in pre_code:
                    ic_file.write(pre_code_line)
                    ic_file.write('\n')
            print('\tCreating Intermediate File:\tDONE!')
        except IOError as ioerror:
            print('\tCreating Intermediate File:\tERROR!')
            print('ERROR: ', ioerror)
    elif output[0] is False:
        print('\tCreating Intermediate File:\tNot Specified!')
    return pre_code
