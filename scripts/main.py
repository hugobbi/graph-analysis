# cria grafo com dados lidos de um csv

import igraph as ig
import time
import sys
import argparse as ap
import datetime as dt
from processa_entradas import *
from importa_csv_dict import *
from cria_arestas import *
from toma_medidas import *
from visual import *

t_inicio = time.time()

arestas_para_custoso = 2000 # quantidade de arestas para que o grafo seja considerado custoso

# Argparse e argumentos do usuário

parser = ap.ArgumentParser()
parser.add_argument("-f", "--arquivo", help='''Nome do arquivo csv contendo os dados que será usado para gerar o grafo. Tipo: string. Se o diretório do arquivo não for o mesmo do main.py, indicar o caminho para o arquivo. Exemplo no mesmo diretório do script: -f "meuarquivo.csv". Exemplo em um diretório diferente: -f "/home/user/caminho_para_arquivo/meuarquivo.csv"''')
parser.add_argument("-atb", "--atributos", default = ["ALL"], nargs="+", help="Lista de atributos considerados para montar as arestas. Será passado o número da coluna correspondente ao atributo. Este número pode ser visto com o script mostra_colunas.py. Se nenhum atributo for passado, como padrão, serão usados todas as colunas menos as que compõem o id do grafo. Tipo: int. Exemplo: -atb 3 4. Pode também ser passado um intervalo de números no formato inicial-final. Exemplo: -atb 1-3 irá gerar uma lista com 1, 2 e 3.")
parser.add_argument("-id", "--identificadores", nargs="+", help="Lista de atributos que irão compor o label dos vértices do grafo. Pode ser passado apeanas um atributo ou múltiplos, que serão concatenados. Será passado o número da coluna correspondente ao atributo. Este número pode ser visto com o script mostra_colunas.py. Tipo: int. Se o label dos vértices não for único, o programa irá informar sobre e irá encerrar. Exemplo: -id 1 2. Pode também ser passado um intervalo de números no formato inicial-final. Exemplo: -atb 1-3 irá gerar uma lista com 1, 2 e 3.")
parser.add_argument("-rst", "--restricao", default=["none"], nargs="+", help="Lista de atributos usados como restrição para criar uma aresta, isto é, se, entre dois vértices, o valor do atributo restritivo é o mesmo, a aresta não é criada. O padrão é nenhuma restrição. Podem ser informadas múltiplas restrições. Será passado o número da coluna correspondente ao atributo. Este número pode ser visto com o script mostra_colunas.py. Tipo: int. Exemplo: -rst 2. Pode também ser passado um intervalo de números no formato inicial-final. Exemplo: -atb 1-3 irá gerar uma lista com 1, 2 e 3.")
parser.add_argument("-lim", "--limiar", type=float, default = 0, help="Limiar usado para gerar as arestas do grafo. O padrão é 0 (zero). Tipo: float. Exemplo: -lim 0.001")
parser.add_argument("-o", "--usar_or", action="store_true", default=False, help="Usa a lógica OR para formar as arestas, isto é, para ser criada uma aresta, pelo menos um dos atributos passados na lista de atributos tem que estar dentro do limiar. O padrão é AND, ou seja, todos os atributos passados têm que estar dentro do limiar.")
parser.add_argument("-m", "--medidas",  default=["none"], nargs="+", help=f'''Lista de medidas de centralidade que serão tomadas sobre o grafo, as quais serão registradas em uma tabela. O padrão é nenhuma, de modo que nenhuma tabela será gerada. Se for muito custoso para tomar a medida (o grafo tem mais de {arestas_para_custoso} arestas), o programa irá perguntar ao usuário se ele realmente quer tomá-la. Podem ser informadas múltiplas medidas. Tipo: string. Exemplo: -m "degree" "betweenness"''')
parser.add_argument("-ni", "--no_graph_image", action="store_true", default=False, help=f"Define se será gerada uma imagem para o grafo. O padrão é gerar uma imagem, se este parâmetro for indicado, não será gerada uma imagem do grafo. Se este tiver mais de {arestas_para_custoso} arestas, será perguntado se realmente quer gerar a imagem, dado o custo computacional da tarefa.")
parser.add_argument("-raw", "--raw_graph", action="store_true", default=False, help="Determina se o grafo usado para tomar as medidas inclui vértices que não formam nenhuma aresta. Por padrão, o programa remove os vértices de grau zero do grafo. Com esta opção, o programa usará o grafo sem remover estes vértices.")
parser.add_argument("-giant", "--giant_component", action="store_true", default=False, help="Determina se apenas o giant component é mostrado na imagem ou se todo o grafo é mostrado. O padrão é mostrar todo o grafo.")
parser.add_argument("-norm", "--normalized", action="store_false", default=True, help="Determina se o programa normaliza os dados de entrada. O padrão é normalizar.")
parser.add_argument("-mdeg", "--min_degree", type=int, default = 0, help="Ao mostrar o grafo, apenas serão plotados os vértices cujo degree é maior que o especificado. O padrão é 0, ou seja, sem restrições para degree. Tipo int. Exemplo: -mdeg 1")

args = parser.parse_args()

nome_arquivo_csv = args.arquivo # nome do arquivo csv a ser usado para gerar grafo
atributos_numerico = args.atributos # lista de atributos, passados como número da coluna
lista_ids_label_numerico = args.identificadores # lista de ids usados no label, passados como número da coluna
lista_restricoes_numerico = args.restricao # lista de restricoes para criar arestas, passadas como número da coluna
limiar = args.limiar # limiar usado para criar arestas
usar_or = args.usar_or # lógica para criar arestas
lista_medidas = args.medidas # lista de medidas que serão tomadas do grafo 
nao_gerar_imagem_grafo = args.no_graph_image # define se será gerada uma imagem do grafo ou não
usar_grafo_puro = args.raw_graph # define se será usado o grafo sem processamento (remover vértices de grau zero) ou não
giant_component = args.giant_component # define se apenas o giant component será mostrado na imagem
normalized = args.normalized # define se os dados usados serão normalizados
min_degree = args.min_degree # apenas serão mostrados vértices cujo grau é maior que este valor


# Verfica consistência de entrada

if args.identificadores == None:
    print("Erro na passagem de parâmetro, o campo dos ids não foi informado.")
    sys.exit("Saindo do programa")

if args.arquivo == None:
    print("Erro na passagem de parâmetro, o campo do nome do arquivo não foi informado.")
    sys.exit("Saindo do programa")

print("Parâmetros OK") # se todos os parâmetros necessário foram informados


# Processa listas numéricas

if atributos_numerico != ["ALL"]:
    atributos_numerico = processa_int_ou_intervalo(atributos_numerico)

lista_ids_label_numerico = processa_int_ou_intervalo(lista_ids_label_numerico)

if lista_restricoes_numerico != ["none"]:
    lista_restricoes_numerico = processa_int_ou_intervalo(lista_restricoes_numerico)

# Lê csv, traduz entrada numérica dos ids para atributos e normaliza dados, se foi pedido

print("Lendo arquivo...")
lista_dict_veiculos, keys = importa_csv(nome_arquivo_csv)

lista_ids_label = [] # usada como label do grafo, indica também atributos que não serão normalizados
for num_id in lista_ids_label_numerico: # traduz os número passados como argumento correspondente às colunas 
    lista_ids_label.append(keys[num_id-1]) # numeração das colunas começa em 1, por isso -1

if normalized:
    lista_dict_veiculos, keys = normaliza_lista_dict(lista_dict_veiculos, keys, lista_ids_label)
print("Arquivo lido.")


# Traduz entrada numérica dos outros parâmetros

print("Traduzindo atributos...")

atributos = []
todos = False
if atributos_numerico != ["ALL"]:
    for num_atb in atributos_numerico: 
        atributos.append(keys[num_atb-1]) 

    if len(atributos) + len(lista_ids_label) == len(keys):
        todos = True # se forem usadas todas as colunas, será indicado
else:
    todos = True
    for atributo in keys:
        if atributo not in lista_ids_label:
            atributos.append(atributo) # atributos usados serão todos menos os que compõem o id

if lista_restricoes_numerico != ["none"]:
    lista_restricoes = []
    for num_rest in lista_restricoes_numerico:
        lista_restricoes.append(keys[num_rest-1])
else:
    lista_restricoes = lista_restricoes_numerico
    

# Prints para mostrar parâmetros selecionados

print("\nAtributos usados:")
print(f"Lista de atributos: {atributos}")
print(f"Lista de atributos para ids: {lista_ids_label}")
print(f"Lista de atributos restritivos: {lista_restricoes}")
print(f"Lista de medidas de centralidade: {lista_medidas}")
output_m = "True" if lista_medidas != ["none"] else "False"
print(f"Tomar medidas: {output_m}")
print(f"Limiar: {limiar}")
print(f"Usar lógica or: {usar_or}")
print(f"Arquivo: {nome_arquivo_csv}")
print(f"Gerar imagem do grafo: {nao_gerar_imagem_grafo}")
print(f"Usar grafo puro: {usar_grafo_puro}")
print(f"Mostrar apenas giant component: {giant_component}")
print(f"Usar dados normalizados: {normalized}\n")
print(f"Degree abaixo ou igual não será plotado: {min_degree}")


# Cria ids

print("Gerando lista de ids...")
lista_ids = cria_lista_ids(lista_dict_veiculos, lista_ids_label) # monta lista de identificadores dos vértices do grafo
if not ids_validos(lista_ids): # se os ids gerados não forem únicos
    print("Erro: ids gerados não são únicos, usar outros atributos")
    sys.exit("Saindo do programa")
else:
    print("Ids válidos")


# Monta lista de arestas

print("Gerando arestas...")
arestas, pesos_arestas = monta_arestas(atributos, lista_dict_veiculos, lista_restricoes, usar_or, limiar)


# Cria grafo e o processa

print("Atribuindo valores ao grafo...")
g_raw = ig.Graph()
n_vertices = (len(lista_dict_veiculos))
g_raw.add_vertices(n_vertices)
g_raw.vs["label"] = lista_ids # label do grafo é a lista de ids
g_raw.add_edges(arestas) # grafo recebe as arestas
g_raw.es["peso"] = pesos_arestas # arestas recebem seus pesos

for key in keys: 
	g_raw.vs[key] = [veiculo[key] for veiculo in lista_dict_veiculos] # grafo recebe os atributos dos dicionários

if not usar_grafo_puro:
    g = g_raw.copy() # copia o grafo original
    to_delete_ids = []

    for v in g.vs:
        if v.degree() == 0:
            to_delete_ids.append(v) # seleciona todos os vértices cujo grau é zero
    g.delete_vertices(to_delete_ids) # remove todos os ids que não formam nenhuma aresta (cujo grau é zero)
else:
    g = g_raw.copy() # se for para usar o grafo puro, os vértices de grau zero não serão removidos

print("Pronto") # finalizou a atribuição

print("\nInformações do grafo gerado:")
print(g.degree_distribution()) # mostra informações do grafo, como número de vértices e quantidade de arestas
print(g.summary())


# Temporizador de saída

t_total = time.time() - t_inicio
print(f"Finalizou em {t_total} segundos")


# Trata custo computacional

quantidade_arestas = len(arestas)
custo = 0 # define a intensidade do custo computacional: 0 para baixo, 1 para médio e 2 para alto
medidas_custosas = ["betweenness"] # lista de medidas que são custosas e não desejáveis de ser tomadas se o grafo for muito grande
nova_lista_medidas = lista_medidas # usada para, se for escolhido, filtrar as medidas que são custosas
opcao_grafo_grande = 0

if quantidade_arestas <= arestas_para_custoso:
    custo = 0
else:
    custo = 1

if not nao_gerar_imagem_grafo or lista_medidas != ["none"]: # se o usuário optou por gerar uma imagem do grafo ou realizar alguma medida
    if custo == 1:
        print(f"O grafo possui mais que {arestas_para_custoso} arestas. O custo computacional para gerar uma imagem do grafo ou tomar medidas de centralidade custosas será alto. Você deseja tomá-las e gerar uma imagem do grafo?")
        print("1 - Tomar medidas custosas e gerar imagem do grafo")
        print("2 - Apenas tomar medidas custosas")
        print("3 - Apenas gerar imagem do grafo")
        print("4 - Não gerar imagem e não tomar medidas custosas")

        while opcao_grafo_grande != 1 and opcao_grafo_grande != 2 and opcao_grafo_grande != 3 and opcao_grafo_grande != 4: # recebe o input do usuário, verificando a consistência da entrada
            opcao_grafo_grande = int(input("Digite sua opção: "))
            
            if opcao_grafo_grande != 1 and opcao_grafo_grande != 2 and opcao_grafo_grande != 3 and opcao_grafo_grande != 4:
                print("Opção inválida, digite novamente.")

        if opcao_grafo_grande == 3 or opcao_grafo_grande == 4: # se for escolhido para não tomar medidas custosas
            nova_lista_medidas = [] # esvazia lista de medidas
            
            for medida in lista_medidas:
                if medida not in medidas_custosas:
                    nova_lista_medidas.append(medida)  # filtra medidas custosas da lista de medidas
    
    # salva informações que irão compor os nomes dos arquivos de saída
    tempo = dt.datetime.now()
    hora_atual = tempo.strftime('%Y%m%d_%H%M%S')
    parametros_usados = monta_nome(atributos, lista_restricoes, usar_or, todos)


# Gera imagem do grafo

if not nao_gerar_imagem_grafo:
    if opcao_grafo_grande == 1 or opcao_grafo_grande == 3 or custo == 0: # se foi selecionado para fazer a imagem do grafo, ou se não for custoso
        if g.vcount() != 0:
            nome_imagem_grafo = f"grafo_img_{hora_atual}_{parametros_usados}_{quantidade_arestas}.pdf"

            print("\nPlotando grafo...")

            if giant_component: # se foi escolhido para apenas mostrar o giant component do grafo
                g_plot = g.components().giant().copy()
            else: # caso contrario, mostrar todo o grafo
                g_plot = g.copy()

            if min_degree < 0:
                    print("Degree mínimo é negativo e será desconsiderado")
                    min_degree = 0

            if min_degree != 0:
                while possui_grau_minimo(g_plot, min_degree):
                    a_remover_grau = []
                    for v in g_plot.vs:
                        if v.degree() <= min_degree:
                            a_remover_grau.append(v)
                    g_plot.delete_vertices(a_remover_grau)

            visual_style = determine_visual_style(g_plot)
            ig.plot(g_plot, target=nome_imagem_grafo, **visual_style)

            print(f"Imagem {nome_imagem_grafo} gerada")
        else:
            print("Nenhuma imagem será gerada, pois o grafo está vazio")
    else:
        print("O grafo não será plotado.")


# Toma medidas de caracterização

if nova_lista_medidas != ["none"]:
    print("Gerando tabela...")

    if len(nova_lista_medidas) != 0:
        if g.vcount() != 0:
            nome_tabela = f"tabela_{hora_atual}_{parametros_usados}.pdf"
            monta_tabela(calcula_medidas(g, nova_lista_medidas, g.vs["label"]), nome_tabela) # tabela com as medidas selecionadas é gerada

            print(f"Tabela {nome_tabela} gerada")
        else:
            print("Nenhuma tabela será gerada, pois o grafo está vazio")
    else:
        print("Lista de medidas está vazia.")