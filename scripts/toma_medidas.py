# contém as funções que montam uma tabela com medidas de caracterização

from pandas import DataFrame
import matplotlib.pyplot as plt
import random

# gera lista lista com ids aleatórios
def gera_ids_aleatorios(n_ids, n_vertices):
    lista_ids = []
    for i in range(n_ids):
        num = random.randint(0, n_vertices-1)
        if num not in lista_ids: lista_ids.append(num) # remove ids repetidos
    
    return lista_ids

# gera lista lista com ids aleatórios
def gera_ids_aleatorios(n_ids, n_vertices):
    lista_ids = []
    for i in range(n_ids):
        num = random.randint(0, n_vertices-1)
        if num not in lista_ids: lista_ids.append(num) # remove ids repetidos
    
    return lista_ids

# calcula medidas de centralidade do grafo, retornando um dicionário com as medidas
def calcula_medidas(grafo, lista_medidas, lista_ids):
    lista_degree = [] # usada para ordenar tabela
    for v in grafo.vs:
        lista_degree.append(v.degree())
    lista_degree.sort(reverse=True) # ordenena a lista de degrees em ordem decrescente

    lista_ids_num_ordenada = []
    for degree in lista_degree:
        for i in range(len(grafo.vs)):
            if degree == grafo.vs[i].degree() and i not in lista_ids_num_ordenada: # pega o id numérico em ordem decrescente de degree
                lista_ids_num_ordenada.append(i)
            
    lista_ids_ordenada = []
    for id in lista_ids_num_ordenada: # traduz o id numérico para o id do label do grafo
        lista_ids_ordenada.append(lista_ids[id])

    dict_valores_medidas = {"id" : lista_ids_ordenada} # mostra as medidas em ordem decrescente de degree

    for medida in lista_medidas:
        lista_medida_calculada = getattr(grafo, medida)()

        lista_medida_calculada = list(map(lambda x: round(x, 4), lista_medida_calculada))

        lista_medida_calculada_ordenada = []
        for i in lista_ids_num_ordenada:
            lista_medida_calculada_ordenada.append(lista_medida_calculada[i])

        dict_valores_medidas[medida] = lista_medida_calculada_ordenada
    

    return dict_valores_medidas


# usa um dicionário com os dados para plotar uma tabela com estes dados
def monta_tabela(dados, nome):
    colunas = list(dados.keys())
    df = DataFrame(dados, columns=colunas)

    fig, ax = plt.subplots(figsize=(11.69,8.27))

    fig.patch.set_visible(False)
    ax.axis("off")
    ax.axis("tight")

    ax.table(cellText=df.values, colLabels=df.columns, cellLoc ="center", loc ="upper center")

    plt.savefig(f"{nome}", format="pdf", bbox_inches="tight")