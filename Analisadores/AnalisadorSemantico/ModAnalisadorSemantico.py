# coding=utf-8
import sys

# flags
lt_flag = False
lse_flag = False

lista_token = []
semantico_logger = []
dicionario_variaveis = {}


def analisador_semantico(token_list):
    def analisa_variavel(linha_lista, **kwargs):
        buffer = ''

        while lista_token[linha_lista].split(',')[0] != 'tk_deli_6':
            leitura_token = lista_token[linha_lista].split(',')[0]
            proximo_lexema = lista_token[linha_lista + 1].split(',')[1]
            leitura_lexema = lista_token[linha_lista].split(',')[1]
            erro_linha = lista_token[linha_lista].split(',')[2]
            erro_coluna = lista_token[linha_lista].split(',')[3]

            if kwargs.get('const') is True:
                # verifica se tipo é inteiro
                if leitura_token != 'integer':
                    print('Tipo de erro: \'{} \' deve ser inteiro, nao {} na linha {} coluna {}'.
                          format(kwargs.get('var'), leitura_token, erro_linha, erro_coluna))
                    semantico_logger.append('Tipo de erro: \'{}\' deve ser inteiro, não {} na linha {} coluna {}'.
                                            format(kwargs.get('var'), leitura_token, erro_linha, erro_coluna))

                    sys.exit()

            # Verifica divisão por 0
            if leitura_lexema == '/' and (proximo_lexema == '0' or (
                    proximo_lexema in dicionario_variaveis.keys() and dicionario_variaveis[proximo_lexema] == '0')):
                print(
                    'Erro Expressao Matematica: divisão por zero na linha {} coluna {}'.format(erro_linha, erro_coluna))
                semantico_logger.append(
                    'Expressao Matematica: divisão por zero na linha {} coluna {}'.format(erro_linha, erro_coluna))

                sys.exit()
            if leitura_token == 'id' and dicionario_variaveis[leitura_lexema]:
                buffer = buffer + dicionario_variaveis[leitura_lexema] + ' '
            else:
                buffer = buffer + leitura_lexema + ' '
            linha_lista += 1

        for i in buffer.rstrip():
            if i.isalpha():
                return buffer.rstrip()
        return int(eval(buffer.rstrip()))

    lista_token = token_list.copy()

    contador_token = 0
    for linha in lista_token:
        if linha.split(',')[0] != '$':
            token = linha.split(',')[0]
            lexema = linha.split(',')[1]
            erro_linha = linha.split(',')[2]
            erro_coluna = linha.split(',')[3]

        if token == 'id':
            if lista_token[contador_token - 1].split(',')[0] == 'integer':
                semantico_logger.append('Declaração de Variável detectada -> {} {}'.
                                        format(lista_token[contador_token - 1].split(',')[0], lexema))

                semantico_logger.append('Checando se a varíavel foi declarada...')
                if lexema not in dicionario_variaveis.keys():
                    if lista_token[contador_token + 1].split(',')[0] == 'tk_op10':  # =
                        dicionario_variaveis.update(
                            {lexema: str(analisa_variavel(contador_token + 2, var=lexema, const=True))})

                    else:
                        dicionario_variaveis.update({lexema: None})

                    semantico_logger.append('Variável \'{}\' declarada'.format(lexema))
                else:
                    print('\nErro: Variável \'{}\' na linha {} coluna {} a variavel ja foi declarada!'.
                          format(lexema, erro_linha, erro_coluna))
                    semantico_logger.append('\nErro: Variável \'{}\' na linha {} coluna {} está declarada!'.
                                            format(lexema, erro_linha, erro_coluna))
                    sys.exit()

            elif lexema in dicionario_variaveis.keys():
                if lista_token[contador_token + 1].split(',')[0] == 'tk_op10':  # = verifica atr
                    dicionario_variaveis.update({lexema: str(analisa_variavel(contador_token + 2))})
                    semantico_logger.append('Variável \'{}\' mudou seu valor para \'{}\''.
                                            format(lexema, dicionario_variaveis[lexema]))
            else:
                if erro_linha != '1':
                    print('essa é a linha', erro_linha)
                    print('\nErro de nome: A Variável \'{}\' na linha {} coluna {} não foi declarada!'.
                          format(lexema, erro_linha, erro_coluna))
                    semantico_logger.append('\nErro de nome: Variável \'{}\' na linha {} coluna {} não foi declarada!'.
                                            format(lexema, erro_linha, erro_coluna))
                    sys.exit()
        contador_token += 1
    semantico_logger.append('Concluido!')


def lertokens():
    with open(nome_arquivo_fonte) as file:
        listalex = file.readlines()
        return listalex


def lse():
    analisador_semantico(lertokens())
    print('\n Log da análise semantica:')
    for lines in semantico_logger:
        print('\n', lines.split(','))