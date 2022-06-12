# funções que calculam os parâmetros visuais do grafo (a imagem final)

import math

# calcula o tamanho da imagem do grafo
def calcula_bbox(n_arestas):
    bbox_limit = 3000

    #bbox = int(1058725/987 + (1495 * n_arestas)/1974) # criada por mínimos quadrados
    bbox = math.sqrt(n_arestas)*150 # criada com raiz quadrada, chegando perto dos pontos

    #if n_arestas > 1200: # criada com composta de log, chegando perto dos pontos
    #    bbox = math.log10(n_arestas)*1200 - 1000 
    #else:
    #    bbox = math.log10(n_arestas)*1000 - 1000

    if bbox > bbox_limit: # define limite para bbox
        bbox = bbox_limit
    
    return (bbox, bbox)  

# determina cor de um vértice, quão maior o degree, mais quente a cor
def determina_cor_vertice(grau, media):
    razao = grau / media

    if razao < 0.1:
        return "#ADD8E6" # light blue
    elif razao < 0.3:
        return "#0000CD" # medium blue
    elif razao < 0.5:
        return "#0000FF" # blue
    elif razao < 0.7:
        return "#90EE90" # light green
    elif razao < 0.9:
        return "#00FF00" # green
    elif razao < 1.1:
        return "#006400" # dark green
    elif razao < 1.3:
        return "#FFFF00" # yellow
    elif razao < 1.5:
        return "#FFCC00" # dark yellow
    elif razao < 1.7:
        return "#FFA500" # orange
    elif razao < 1.9:
        return "#FF8C00" # dark orange
    elif razao < 2.1:
        return "#FF4500" # orange red
    elif razao < 2.3:
        return "#FF3333" # light red
    elif razao < 2.5:
        return "#FF0000" # red
    elif razao < 2.7:
        return "#8B0000" # dark red
    elif razao < 2.9:
        return "#9370DB" # medium purple
    elif razao < 3.1:
        return "#A020F0" # purple
    else:
        return "#000000" # black

# cria lista de cores dos vértices do grafo
def lista_cores(g):
    lista_graus = g.degree()
    
    if len(lista_graus) == 0:
        media_graus = 0
    else:
        media_graus = sum(lista_graus) / len(lista_graus)

    lista_cores = []
    for grau in lista_graus:
        lista_cores.append(determina_cor_vertice(grau, media_graus))

    return lista_cores

# determina características visuais do grafo
def determine_visual_style(g):
    font_limit = 8

    visual_style = {}
    visual_style["bbox"] = calcula_bbox(g.ecount())
    visual_style["margin"] = 60
    visual_style["edge_color"] = "grey"
    visual_style["vertex_color"] = lista_cores(g)
    visual_style["vertex_label_dist"] = 1.1
    visual_style["vertex_size"] = [max(15, 6*math.sqrt(d)) for d in g.degree()] # tamanho do vértice será o maior número entre 1 e 5*sqrt(degree)
    visual_style["vertex_label_size"] = [max(10, 4*math.sqrt(d) if 4*math.sqrt(d) < font_limit else font_limit) for d in g.degree()] # tamanho da fonte entre 7 e 20, dependendo do grau do vértice
    visual_style["layout"] = g.layout("auto")

    return visual_style

# determina se o grafo possui algum vértice com grau mínimo passado
def possui_grau_minimo(grafo, d_minimo):
    for v in grafo.vs:
        if v.degree() <= d_minimo:
            return True
    return False