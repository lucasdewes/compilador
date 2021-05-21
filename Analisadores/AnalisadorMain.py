from AnalisadorLexico.ModAnalisadorLexico import analisa
from AnalisadorSintatico.ModAnalisadorSintatico import syntactic_analyzer
from AnalisadorSemantico.ModAnalisadorSemantico import analisador_semantico
from Gerador.Intermediario import intermediate_code

import sys
import os.path

lt_flag = False
sin_flag = False
sema_flag = False
tudo_flag = False
inter_flag = False

pre_code = []
lista_token = []
semantico_logger = []
dicionario_variaveis = {}

# Source code
nome_arquivo_fonte = ''
output_name = ''

# Parameters
parameters = sys.argv[1:]
print('Argumento recebido :', parameters, '\n\n')

if not parameters:
    print('Sem parametros!')
    print('digite -> python AnalisadorSemantico.py [filename].chr [-parametros]')
    sys.exit()
else:
    if parameters[0] == '-help':
        print('\n\nExemple: \n  python AnalisadorMain.py [filename].txt |Para realisar todas as análises')
        print('\n\nExemple: \n  python AnalisadorMain.py [filename].txt  -lt')
        print('\nParametros disponiveis:')
        print(' -lt\tRealiza análise lexica e exibe lista de tokens detectados')
        print(' -sin\tRealiza análise sintatica e exibe log do analisador')
        print(' -sema\tRealiza análise semantica e exibe o log do analisador')
        print('-inter\tRealiza a geração de codigo intermediario')

        sys.exit()

    elif str(parameters[0]).endswith('.txt') or str(parameters[0]).endswith('.chr'):
        nome_arquivo_fonte = parameters[0]
        if not parameters[1:]:
            tudo_flag = True
        for param in parameters[1:]:
            if param == '-lt':
                lt_flag = True
            elif param == '-sin':
                sin_flag = True
            elif param == '-sema':
                sema_flag = True
            elif param == '-inter':
                inter_flag = True

    elif not str(parameters[0]).endswith('.chr') or str(parameters[0]).endswith('.txt'):
        print('Arquivo nao existe')
        print('Arquivo ', parameters[0], ' Nao encontrado!')
        sys.exit()

print(nome_arquivo_fonte)


def lertokens():
    with open("resultado-lex.chr") as file:
        listalex = file.readlines()

        return listalex


if lt_flag:
    analisa(nome_arquivo_fonte)
    listalex = lertokens()
    print('\nLista de tokens detectados:')
    for i in listalex:
        print(i.split(',')[0])

if sin_flag:
    listalex = lertokens()
    print('\n\nAnálise sintática iniciada.')
    result_syntactic = syntactic_analyzer(listalex)
    print('\n Log de transformacoes da pilha:')
    for i in result_syntactic:
        print(i)

if sema_flag:
    semantico_logger = analisador_semantico(lertokens())
    print('\n Log da análise semantica:')
    for lines in semantico_logger:
        print('\n', lines.split(','))

if tudo_flag:
    analisa(nome_arquivo_fonte)
    listalex = lertokens()
    result_syntactic = syntactic_analyzer(listalex)
    semantico_logger = analisador_semantico(lertokens())
    print('\n\n\n')

# -------- test intermediario
output_name = 'intercode'
if inter_flag:
    print('\n\nGenerating code...')
    intermediate_code_result = intermediate_code(lertokens(), 0, 0, pre_code, inter_flag, output_name)
    print(intermediate_code_result)
    for line in intermediate_code_result:
        print(line)
