import queue
from collections import deque
import sys
import os
import csv
# import logging

stack = deque()
queue = []

listalex = []
lista_result_sintatico = []
lista_tab = []  # lista de nao terminais, tokens e numero da regra
lista_comandos = []  # lista de regras para manipular a pilha
lista_reservadas = []

dict_estados = {}
dict_acoes = {}
dict_reservadas = {}

# Source Code
nome_arquivo_fonte = ''

def syntactic_analyzer(lista):
    def manipulacao(nao_terminal, terminal):
        # print('nao terminal e terminal', nao_terminal, terminal, '\n')
        # print('dicionario de estados:', dict_estados, '\n')
        # print('printando keys\n')
        # print(dict_estados.keys(), '\n')

        if (nao_terminal, terminal) in dict_estados.keys():
            # print(' \n\n entrou no if \n\n')
            print('\ncaso encontrado! retorona:', dict_estados[nao_terminal, terminal])
            return dict_estados[nao_terminal, terminal]
        else:
            return 'error'

    # lendo a tabela em forma de lista de tokens
    with open('Syntactic_Table.config') as config:  # linha, coluna, numero
        buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
        for line in buff_reader_config:
            lista_tab.append(line)
        # print('\nlista_tab criada : ')

    # print(lista_tab)
    # print('\n entra no for criar dict estados')

    for line_lista in range(len(lista_tab)):  # criando dicionario de comparacoes
        nao_terminal = lista_tab[line_lista][0]
        config_terminal = lista_tab[line_lista][1]
        config_faca = lista_tab[line_lista][2]
        dict_estados[nao_terminal, config_terminal] = config_faca
    # print('\ndicionario estados criado')

    with open('regras_pilha.config') as config:  # lendo a lista de manipulacoes
        buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
        for line in buff_reader_config:
            lista_comandos.append(line)
        # print('\nlista_comandos criada')

    for line_regras in range(len(lista_comandos)):  # criando dicionario de acoes
        id_acao = lista_comandos[line_regras][0]
        manipula_pilha = lista_comandos[line_regras][1:]
        dict_acoes[id_acao] = manipula_pilha
    # print('\ndicionario acoes criado')

    with open('palavras_reservadas.config') as config:  # lendo lista das palavras reservadas
        buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
        for line in buff_reader_config:
            lista_reservadas.append(line)
        # print('\nlista_reservadas criada')

    for linha_palavras_reservadas in range(len(lista_reservadas)):  # criando dicionario de palavras reservadas
        reser_token = lista_reservadas[linha_palavras_reservadas][0]
        reser_lexeme = lista_reservadas[linha_palavras_reservadas][1:]
        dict_reservadas[reser_token] = reser_lexeme
    # print('\ndicionario reservadas craido')

    for token_list_line in list(lista):  # inserindo na fila
        queue.append(token_list_line.split(',')[0])
    print('\nTokens inseridos na fila:')
    print(queue)
    # A fila ja tem '$' no final

    stack.append('$')  # iniciando a pilha com $ e <PROGRAM> em cima
    stack.append('<PROGRAM>')
    print('\n$ e <PROGRAM> inseridos na pilha')
    print('\npilha:', stack)

    local_erro = 0

    while queue and stack:
        print('\nTem item na pilha e na lista')
        if stack[-1] == 'Ã®':
            print('\n topo da pilha é terminal, retirando î = Ã® \n', stack)
            stack.pop()
            print(stack)
        if queue[0] == 'comentario_de_linha':
            print('\ncomentario de linha, linha ignorada')
            del queue[0]

        nao_terminal = stack[-1]

        print(stack)
        print(queue)

        if nao_terminal.isupper():
            print(stack)
            print(queue)
            print('\nTopo da pilha eh Maiusculo -> <NAO-TERMINAL>')
            print('\nPrimeiro da Pilha eh:', nao_terminal)
            terminal = queue[0]
            print('Primeiro da lista eh:', terminal)

            grammar = manipulacao(nao_terminal, terminal)
            print('\ngrammar definido:', grammar)

            if grammar == 'erro':
                print('\ngrammar == erro')
                print(stack)
                print(queue)

                if dict_reservadas.get(nao_terminal) is None:
                    print(dict_reservadas.get(nao_terminal), 'eh None')
                    print(stack)
                    print(queue)

                    print('\nerro sintatico: ', lista[local_erro].split(',')[1],
                          'inesperado, Caracter invalido na linha ', lista[local_erro].split(',')[2], ', coluna ',
                          lista[local_erro].split(',')[3])
                    sys.exit()

                print("\nErro sintatico: {} inesperado! esperava {} na linha {} coluna {}".format(
                    lista[local_erro].split(',')[1], ''.join(dict_reservadas.get(nao_terminal)),
                    lista[local_erro].split(',')[2], lista[local_erro].split(',')[3]))
                sys.exit()
            stack.pop()
            print('\ndeu pop na pilha')

            print('\noque tem na lista_result_sintatico:', lista_result_sintatico)

            print('\ntransformar:', nao_terminal, 'em', dict_acoes.get(grammar), 'na lista de result sintatico')
            lista_result_sintatico.append(nao_terminal + ' -> ' + ' '.join(dict_acoes.get(grammar)))
            print('\nnova lista result sintatico:', lista_result_sintatico)

            contador_gramat = len(dict_acoes.get(grammar)) - 1
            print('\nContador gramat:', contador_gramat)

            while contador_gramat >= 0:

                print('print test:', dict_acoes.get(grammar)[contador_gramat]) ############
                print('\nA acao nao manda encerrar:')
                stack.append(dict_acoes.get(grammar)[contador_gramat])
                print('\nitens adicionaodos na pilha:', dict_acoes.get(grammar)[contador_gramat])

                contador_gramat -= 1

        elif stack[-1] == queue[0]:
            # logger
            print(stack[-1], '==', queue[0], '-> eliminando da pilha e da lista')
            lista_result_sintatico.append(stack[-1] + ' na pilha == ' + queue[0] + ' na fila -> removendo')
            if stack[-1] == '$':
                print('\n\n\tFim do analisador!\n\tFinalisado sem erro.')

            del queue[0]
            local_erro += 1
            stack.pop()

        elif stack[-1] != queue[0]:
            print(stack)
            print(queue)

            print("Erro sintatico: {} inesperado! esperava {} na linha {} coluna {}".format(lista[local_erro].split(',')[1],
                              dict_reservadas.get(nao_terminal),
                              lista[local_erro].split(',')[2], lista[local_erro].split(',')[3]))
            # logger
            sys.exit()
    if not queue and not stack:
        return lista_result_sintatico

    else:
        print("Error --> A Pilha ou fila nao estao vazia")
        # syntactic_logger.error('Error --> Stack or Queue are not empty')
        sys.exit()