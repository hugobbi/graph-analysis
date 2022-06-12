# contém funções que processam os dados entrados pelo usuário

import itertools
import sys

# recebe a lista contendo os vértices do grafo e os nomes dos atributos que irão compor o id, retornando a lista com os nomes dos atributos concatenados
def cria_lista_ids(lista_dicionarios, atributos_usados):
    lista_ids = []

    for nodo in lista_dicionarios:
        nomes_atributos = []
        for i in range(len(atributos_usados)): # para cada aributo, forma string que irá compor o nome do vértice
            if i == 0: # o primeiro atributo do nome não recebe "_" antes
                nomes_atributos.append(f"{nodo[atributos_usados[i]]}")
            else:
                nomes_atributos.append(f"_{nodo[atributos_usados[i]]}")
        nome_atributo = "" 
        for nome in nomes_atributos:
            nome_atributo += nome # monta o nome do vértice com as strings geradas por cada atributo    
        lista_ids.append(nome_atributo) # monta a lista contendo os nomes dos vértices
    
    return lista_ids

# recebe a lista contendo os ids dos nodos e retorna True se todos forem diferentes ou False caso contrário
def ids_validos(lista_ids):
    pares_ids = itertools.combinations(lista_ids, 2) # cria pares de ids

    for par in pares_ids:
        if par[0] == par[1]: # se qualquer par for igual, retorna False
            return False

    return True # caso contrário, retorna True

# recebe os parâmetros do usuário e gera o nome do arquivo que contém os dados do grafo
def monta_nome(atributos, lista_restricoes, usar_or, todos):
    nome_final = ""
    nomes = []

    if len(atributos) < 6: # se forem muitos atributos, eles não serão colocados no nome
        for i in range(len(atributos)):
            if i == 0:
                nomes.append(f"{atributos[i].replace(' ', '_')}_")
            else:
                nomes.append(f"{atributos[i].replace(' ', '_')}_")
    elif todos: # se forem usados todos os atributos, será indicado
        nomes.append("ALL_")

    for restricao in lista_restricoes:
        nomes.append(f"{restricao.replace(' ', '_')}_")

    if usar_or:
        nomes.append("OR")
    else:
        nomes.append("AND")

    for nome in nomes:
        nome_final += nome

    return nome_final

# converte string representando intervalo numérico na forma "início-fim" em uma lista contendo os números naquele intervalo
def converte_intervalo(intervalo):
    numeros = intervalo.split("-")

    inicio = int(numeros[0])
    fim = int(numeros[1])

    if inicio > fim: sys.exit("Erro: início do intervalo maior do que o final")

    lista_intervalo = []

    x = inicio
    while x != fim+1: # preenche a lista incrementando os números do início do intervalo ao fim
        lista_intervalo.append(x)
        x += 1

    return lista_intervalo 

# determina se a entrada é um intervalo numérico na forma "início-fim" ou uma lista de inteiros, retornando a lista de inteiros que corresponde ao intervalo ou a própria lista de inteiros
def processa_int_ou_intervalo(entrada):
    lista_intervalo = []

    for v in entrada:
        if "-" in v:
            for num in converte_intervalo(v):
                lista_intervalo.append(num)
        else:
            lista_intervalo.append(int(v)) # transforma os números em inteiros

    return lista_intervalo

