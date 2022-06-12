import igraph as ig
import random
import math
from visual import *

num_vertices = 10
num_arestas = 100

g = ig.Graph()

g.add_vertices(num_vertices)

ids = []
for i in range(num_vertices):
    ids.append(i)

arestas = []

for i in range(num_arestas):
    x = random.randint(0, num_vertices-1)
    y = random.randint(0, num_vertices-1)

    while x == y:
        y = random.randint(0, num_vertices-1)

    arestas.append((ids[x], ids[y]))

g.add_edges(arestas)
g.vs["label"] = ids

font_limit = 12

visual_style = {}
visual_style["bbox"] = calcula_bbox(g.ecount())
visual_style["margin"] = 100
visual_style["edge_color"] = "grey"
visual_style["vertex_label_dist"] = 1.1
visual_style["vertex_size"] = [max(3, 5*math.sqrt(d)) for d in g.degree()] # tamanho do vértice será o maior número entre 1 e 5*sqrt(degree)
visual_style["vertex_label_size"] = [max(10, 4*math.sqrt(d) if 4*math.sqrt(d) < font_limit else font_limit) for d in g.degree()] # tamanho da fonte entre 7 e 20, dependendo do grau do vértice
visual_style["layout"] = g.layout("auto")

ig.plot(g, **visual_style)
