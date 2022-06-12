# contém as funções que montam uma lista contendo as arestas do grafo em forma de uma tupla de dois elementos

import itertools

# dependendo da lógica escolhida, verifica se deve ser criada uma aresta entre um par de nodos
def verifica_aresta(lista_resultado, usar_or):
    if usar_or:
        for resultado in lista_resultado:
            if resultado == 1: # dada a lista final de resultados, se houver algum verdadeiro, a aresta é criada
                return True
        return False
    else:
        for resultado in lista_resultado:
            if resultado == 0: # dada a lista final de resultados, se houver algum falso, a aresta não é criada
                return False
        return True

# dados dois vértices e uma lista de atributos usados como restrição, a função retorna -1 se a lista de restrições contiver "none",
# False se os vértices possuírem os mesmos valores para os mesmos atributos restritivos ou True se possuírem todos os valores diferentes 
# para os mesmos atributos restritivos
def dentro_restricao(v1, v2, lista_restricoes):
    for restricao in lista_restricoes:
        if restricao == "none":
            return -1
        if v1[restricao] == v2[restricao]:
            return False
    return True

# monta uma lista de arestas a partir de uma lista de atributos, uma de dicionários, uma de restrições, uma lógica para montar arestas e um limiar
def monta_arestas(atributos, lista_dicionarios, lista_restricoes, usar_or, limiar):
    arestas = []
    pesos_arestas = []

    for v1, v2 in itertools.combinations(lista_dicionarios, 2): # para cada par de dicionários da lista
        lista_resultados = [] # indica se para cada atributo, deve haver uma aresta (1) ou não (0)
        if dentro_restricao(v1, v2, lista_restricoes) == -1: # não é usada nenhuma restrição
            for atributo in atributos:
                if abs(v1[atributo] - v2[atributo]) <= limiar: # se a diferença absoluta do valor do atributo de dois nodos for menor ou igual ao limiar
                    lista_resultados.append(1) # lista de resultados para aquele par contém 1, isto é, verdadeiro
                else:
                    lista_resultados.append(0) # caso contrário contém zero

            if verifica_aresta(lista_resultados, usar_or):
                arestas.append((v1["id"], v2["id"])) # adiciona a aresta à lista de arestas, utilizando o identificador numérico dos vértices
                pesos_arestas.append(sum(lista_resultados)) # como, para cada atributo, a lista contém 1 se há aresta e 0 se não há, a soma desses uns dará o número de atributos dentro do limiar entre o par de nodos

        else: # considerando a restrição
            if dentro_restricao(v1, v2, lista_restricoes): # se os vértices estiverem dentro da restrição
                for atributo in atributos:
                    if abs(v1[atributo] - v2[atributo]) <= limiar: 
                        lista_resultados.append(1) 
                    else:
                        lista_resultados.append(0) 

                if verifica_aresta(lista_resultados, usar_or):
                    arestas.append((v1["id"], v2["id"]))
                    pesos_arestas.append(sum(lista_resultados))

    return arestas, pesos_arestas # retorna lista com arestas e lista com pesos das arestas
