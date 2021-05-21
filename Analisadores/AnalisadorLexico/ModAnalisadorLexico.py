import sys
import os.path

# Bliblioteca padrao de string
import string

arquivo_s = "resultado-lex.chr"


def Delimitador(caracter):
    # delimitadores linguagem
    delimitadores = "()[]{};,"
    if caracter in delimitadores:
        return True
    return False


# Especificando qual dos tokens delimitadores eh a entrada
def qualTokenDelimitador(entrada):
    # String com os operadores componentes da linguagem
    delimitadores = "()[]{};,"
    posicao = delimitadores.find(entrada)
    return "tk_deli_" + str(posicao)


# Verificando se a entrada eh uma letra
def Letra(caracter):
    # String com as letras componentes da linguagem (a..z|A..Z)
    letra = string.ascii_letters
    if caracter in letra:
        return True
    return False


# Verificando se a entrada eh um digito
def Digito(caracter):
    # String com os digitos componentes da linguagem
    digito = '0123456789'
    if caracter in digito:
        return True
    return False


# Verificando se a entrada eh um simbolo asc_ii
def Simbolo(caracter):
    # Strings com os simbolos da tabela ASCII (32 a 126)
    simbolos = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~ '''
    if caracter in simbolos:
        return True
    return False


# Verificando se a entrada eh um operador
def Operador(entrada):
    # Listas com os operadores componentes da linguagem
    operadores = '. + - * / ++ -- == != > >= < <= && || ='.split()
    if entrada in operadores:
        return True
    return False


# Identificando qual dos tokens operadores eh a entrada

def qualTokenOperador(entrada):  # aqui detecta o < & >
    # Listas com os operadores componentes da linguagem
    operadores = '= + - * / < > ++ -- == != >= <= ||'.split()
    posicao = 0
    for x in operadores:
        if x == entrada:
            break
        posicao += 1
    if posicao > 9:
        return "tk_op" + str(posicao)
    else:
        return "tk_op1" + str(posicao)


# Verificando se a entrada eh uma palavra reservada
def Reservada(entrada):
    # Lista para abrigar palavras que serao indexadas por uma mesma letra no dicionario a seguir
    reservadas = "starten fertig print read if else enquanto end int ".split()
    if entrada in reservadas:
        return True
    return False


# Metodo que especifica qual dos tokens palavras reservadas eh a entrada
def qualTokenReservada(entrada):
    # Listas com os operadores componentes da linguagem
    reservadas = '''starten fertig print read if else while end int'''.split()
    posicao = 0
    for x in reservadas:
        if x == entrada:
            break
        posicao += 1
    if posicao == 0:
        return "starten"
    elif posicao == 1:
        return "fertig"
    elif posicao == 2:
        return "schr"
    elif posicao == 3:
        return "lesen"
    elif posicao == 4:
        return "ob"
    elif posicao == 5:
        return "obni"
    elif posicao == 6:
        return "wah"
    elif posicao == 7:
        return "ende"
    elif posicao == 8:
        return "integer"
    else:
        return "Palavra nao encontrada ->" + str(posicao)


# Metodo que executa o analsador lexico
def analisa(nome_do_arquivo):
    # Abre o arquivo de saida do programa
    arquivo_saida = open(arquivo_s, 'w')
    # Verifica se o arquivo de entrada existe no diretorio em questao
    if not os.path.exists(nome_do_arquivo):
        arquivo_saida.write("Arquivo de entrada inexistente")
        return

    # Abre o arquivo de entrada do programa
    arquivo = open(nome_do_arquivo, 'r')

    # Le a primeira linha
    linha_programa = arquivo.readline()

    # numero_linha indica a linha do caracter_atual
    numero_linha = 1

    # While que percorre o code linha por linha
    while linha_programa:
        i = 0
        tamanho_linha = len(linha_programa)
        while i < tamanho_linha:  # Percorre os caracteres da linha
            caracter_atual = linha_programa[i]
            caractere_seguinte = None
            # Soh posso pegar o caractere_seguinte se ele existe na linha
            if (i + 1) < tamanho_linha:
                caractere_seguinte = linha_programa[i + 1]
                # ===================================================================================
            # Verifica se o caracter eh um delimitador - OK
            if Delimitador(caracter_atual):
                arquivo_saida.write(
                    qualTokenDelimitador(caracter_atual) + ',' + caracter_atual + ',' + str(
                        numero_linha) + ',' + str(i) + '\n')
            # ===================================================================================
            # Consumindo comentarios de linha - OK
            elif caracter_atual == '/' and caractere_seguinte == '/':
                # Fazendo o programa pular para a proxima linha
                i = tamanho_linha
                arquivo_saida.write(
                    'comentario_de_linha,//,' + str(numero_linha) + ',' + str(i) + '\n')
            # ===================================================================================
            # Consumindo comentarios de bloco - OK
            elif caracter_atual == '/' and caractere_seguinte == '*':
                cont = True  # Variavel que impedirah o loop a seguir de continuar caso
                # seja falsa, isso acontece com erro fim inesperado de arquivo
                linha_comeco = numero_linha  # Guardo a linha que o bloco comecou, para caso
                # o erro de bloco nao fechado ocorrer o programa
                # poderah indicar o comeco do erro
                while cont and not (caracter_atual == '*' and caractere_seguinte == '/'):
                    # Soh posso pegar o caractere atual e o proximo se ele existe na linha
                    if (i + 2) < tamanho_linha:
                        i += 1
                        caracter_atual = linha_programa[i]
                        caractere_seguinte = linha_programa[i + 1]
                    else:
                        linha_programa = arquivo.readline()  # Le a proxima linha
                        tamanho_linha = len(linha_programa)
                        numero_linha += 1
                        i = -1
                        if not linha_programa:
                            arquivo_saida.write(
                                "Erro Lexico - Comentario de bloco nao fechado - Linha: %d\n" % linha_comeco)
                            cont = False
                i += 1  # Faco isso para que nao considere o '/' do final do bloco (na composicao */) no proximo loop
            # ===================================================================================
            # Verificando se o elemento eh um operador
            elif caractere_seguinte is not None and Operador(caracter_atual + caractere_seguinte):
                arquivo_saida.write(qualTokenOperador(
                    caracter_atual + caractere_seguinte) + ',' + caracter_atual + caractere_seguinte + ',' + str(
                    numero_linha) + ',' + str(i) + '\n')
                i += 1
            elif Operador(caracter_atual):
                arquivo_saida.write(
                    qualTokenOperador(caracter_atual) + ',' + caracter_atual + ',' + str(
                        numero_linha) + ',' + str(i) + '\n')

            # ===================================================================================
            # Verificando se o elemento em questao eh caractere constante - OK
            # string.punctuation[6] retorna o simbolo - ' - que representa o inicio do caractere constante
            elif caracter_atual == string.punctuation[6]:

                if (linha_programa[i + 1] == '\n') or (not (string.punctuation[6] in linha_programa[i + 1:])):
                    arquivo_saida.write(
                        'Erro Lexico - Caractere nao fechado - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
                    i = tamanho_linha
                elif Simbolo(linha_programa[i + 1]) and linha_programa[i + 1] != string.punctuation[6] and \
                        linha_programa[i + 2] == string.punctuation[6]:
                    arquivo_saida.write('literalbriefe,' + linha_programa[i + 1] + ',' + str(
                        numero_linha) + ',' + str(i) + '\n')
                    i += 2
                elif linha_programa[i + 1] == string.punctuation[6] and linha_programa[i + 2] == string.punctuation[
                        6]:
                    arquivo_saida.write(
                        'Erro Lexico - Caractere nao pode ser aspas simples - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
                    i += 2
                elif linha_programa[i + 1] == string.punctuation[6]:
                    arquivo_saida.write(
                        'Erro Lexico - Caractere nao pode ser vazio - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
                    i += 1
                else:
                    arquivo_saida.write(
                        'Erro Lexico - Tamanho ou simbolo do Caractere invalido - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
                    i = linha_programa[i + 1:].find(string.punctuation[6]) + 1

            # ===================================================================================
            # Verificando se o elemento em questao eh cadeia constante - OK
            # string.punctuation[1] retorna o simbolo - " - que representa o inicio da cadeia constante
            elif caracter_atual == string.punctuation[1]:
                i += 1  # Para passar a primeira ocorrencia do caractere "
                ehValido = True

                # Se a linha soh contem uma ocorrencia de ", significa que a string nao foi fechada
                if linha_programa[i:].find(string.punctuation[1]) == -1:
                    arquivo_saida.write(
                        'Erro Lexico - String nao fechada - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
                    i = tamanho_linha
                else:
                    fim_cadeia = i + linha_programa[i:].find(string.punctuation[1])
                    nova_cadeia = linha_programa[i:fim_cadeia]
                    i = fim_cadeia
                    for x in nova_cadeia:
                        if not Simbolo(x):
                            ehValido = False
                            arquivo_saida.write(
                                'Erro Lexico - String com simbolo invalido (Nao ascii) - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
                            break
                    if ehValido:
                        arquivo_saida.write('literalbriefe,' + nova_cadeia + ',' + str(
                            numero_linha) + ',' + str(i) + '\n')
            # ===================================================================================
            # Verificando se o elemento em questao eh um numero - OK
            elif Digito(caracter_atual):
                string_temp = caracter_atual
                i += 1
                j = 0  # Vai contar se o numero tem pelo menos 1 digito depois do '.'
                caracter_atual = linha_programa[i]
                while Digito(caracter_atual) and (i + 1 < tamanho_linha):
                    string_temp += caracter_atual
                    i += 1
                    caracter_atual = linha_programa[i]

                if caracter_atual == '.':
                    if (i + 1) < tamanho_linha:
                        string_temp += caracter_atual
                        i += 1
                        caracter_atual = linha_programa[i]
                        while Digito(caracter_atual) and i + 1 < tamanho_linha:
                            j += 1
                            string_temp += caracter_atual
                            i += 1
                            caracter_atual = linha_programa[i]

                        if caracter_atual == '.':
                            j = 0
                            # Tratamento de erro, modalidade do desespero
                            while i + 1 < tamanho_linha:
                                i += 1
                                caracter_atual = linha_programa[i]
                                if Delimitador(caracter_atual) or caracter_atual == ' ':
                                    i -= 1  # Eh necessario voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
                                    break
                    else:
                        arquivo_saida.write(
                            'Erro Lexico - Numero mal formado - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)

                    if j > 0:
                        arquivo_saida.write('Numero Real,' + string_temp + ' - Linha: ' + str(
                            numero_linha) + ' e Coluna: ' + str(i) + '\n')
                    else:
                        arquivo_saida.write(
                            'Erro Lexico - Numero mal formado - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
                else:
                    arquivo_saida.write('literalzahl,' + string_temp + ',' + str(
                        numero_linha) + ',' + str(i) + '\n')
                    if not Digito(caracter_atual):
                        i -= 1
            # ===================================================================================
            # Verificando identificadores ou palavras reservadas - OK
            elif Letra(caracter_atual):
                # Apos verificar que o primeiro caractere da palavra era uma letra, vou percorrendo o identificador
                # ateh encontrar um caractere que nao possa ser de identificadores ou ateh o final da linha
                string_temp = caracter_atual
                i += 1
                algum_erro = False
                while i < tamanho_linha:
                    caractere_seguinte = None
                    caracter_atual = linha_programa[i]
                    if i + 1 < tamanho_linha:
                        caractere_seguinte = linha_programa[i + 1]
                    if Letra(caracter_atual) or Digito(caracter_atual) or caracter_atual == '_':
                        string_temp += caracter_atual
                    elif (Delimitador(
                            caracter_atual) or caracter_atual == ' ' or caracter_atual == '\t' or caracter_atual == '\r'):
                        i -= 1  # Preciso voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
                        break
                    elif (caractere_seguinte is not None and Operador(
                            caracter_atual + caractere_seguinte)) or Operador(caracter_atual):
                        i -= 1
                        break
                    elif caracter_atual != '\n':
                        arquivo_saida.write(
                            "Erro Lexico - Identificador com caracter invalido: " + caracter_atual + " - Linha: %d\n" % numero_linha + ' e Coluna: %d\n' % i)
                        algum_erro = True
                        break
                    i += 1  # Passando o arquivo ateh chegar ao final do identificador/palavra reservada

                if algum_erro:
                    while i + 1 < tamanho_linha:
                        i += 1
                        caracter_atual = linha_programa[i]
                        if Delimitador(
                                caracter_atual) or caracter_atual == ' ' or caracter_atual == '\t' or caracter_atual == '\r' or caracter_atual == '/':
                            i -= 1  # Preciso voltar um elemento da linha para que o delimitador seja reconhecido no momento certo
                            break
                else:  # Se nao houver erros basta verificar se o elemento eh palavra reservada tambem
                    if Reservada(string_temp):

                        arquivo_saida.write(
                            qualTokenReservada(string_temp) + ',' + string_temp + ',' + str(
                                numero_linha) + ',' + str(i) + '\n')
                    else:
                        arquivo_saida.write(
                            'id,' + string_temp + ',' + str(numero_linha) + ',' + str(
                                i) + '\n')

            # -----------------------------------------------
            # Verificando Erros Lexicos - Caracter Invalido
            # Os caracteres especiais \n, \t, \r e espaco sao desconsiderados como caracteres invalidos
            # por aparecerem constantemente no codigo em questao
            elif caracter_atual != '\n' and caracter_atual != ' ' and caracter_atual != '\t' and caracter_atual != '\r':
                arquivo_saida.write(
                    'Erro Lexico - Caracter Invalido: ' + caracter_atual + ' - Linha: %d\n' % numero_linha + ' e Coluna: %d\n' % i)
            # ===================================================================================
            i += 1  # Incrementando a leitura dos caracteres da linha lida no momento

        linha_programa = arquivo.readline()  # Le a proxima linha
        numero_linha += 1
    # Fim do programa
    arquivo_saida.write('$')
    # Fim do arquivo de entrada
    arquivo.close()
    # Fim do arquivo de entrada
    # ----- FIM DO ANALISADOR LEXICO -----


# Executando o programa