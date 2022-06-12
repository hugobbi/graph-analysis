# funções para lidar com a montagem das estruturas de dados

from csv import DictReader

# le csv inteiro e o guarda na memória, após, salva cada linha da leitura em uma lista
def importa_csv(caminho_csv): # recebe o caminho e o nome do arquivo a ser lido
	with open(caminho_csv) as arquivo:
		leitura = DictReader(arquivo) # lê cada atributo como string, que será convertido posteriormente

		keys = []
		for coluna in leitura.fieldnames:
			keys.append(coluna)
		
		linhas = []
		id = 0 # identificador usado para criar arestas
		for linha in leitura:
			linhas.append(linha) # grava cada linha (um dicionário próprio) em uma lista de linhas
			linha["id"] = id
			id += 1

		keys = leitura.fieldnames # guardas as keys do dicionário

		for linha in linhas: # converte atributos do dicionário para seus tipos respectivos (inicialmente são strings)
			for key in keys: 
				if key == "Step":
					linha[key] = int(float(linha[key])) # converte step para int
				elif key != "Link" and key != "id":
					linha[key] = float(linha[key]) # converte o resto dos atributos menos link, que já é uma string, e o id, que já é um inteiro, para float

		return linhas, keys # retorna lista contendo dicionários

# normaliza lista de valroes segundo a seguinte fórmula: n = (x-min)/(max-min)
def normaliza_lista(lista_atributos): # normaliza os valores de uma lista
    minimo = min(lista_atributos)
    maximo = max(lista_atributos)

    lista_atributos_norm = []

    for atributo in lista_atributos:
        lista_atributos_norm.append((atributo-minimo)/(maximo-minimo)) 

    return lista_atributos_norm

# normaliza os valores da lista de dicionários e retorna uma lista de dicionários normalizada
def normaliza_lista_dict(lista_dicionarios, keys, lista_ids_label): # normaliza os valores do dicionário inteiro
	lista_dicionarios_norm = lista_dicionarios
	
	keys_norm = []
	for key in keys:
		if key not in lista_ids_label: # só os atributos que não compõem o label serão normalizados
			lista_atributos = [] # lista de atributos, usada para calcular fórmula da normalização
			
			for dicionario in lista_dicionarios_norm:
				lista_atributos.append(dicionario[key]) # guarda todos os valores de uma key do dicionário na lista

			lista_atributos = normaliza_lista(lista_atributos)

			for dicionario, atributo_norm in zip(lista_dicionarios_norm, lista_atributos):
				dicionario[f"{key} Norm"] = atributo_norm # para cada dicionário na lista, atribui o valor respectivo da lista de atributos normalizados

			keys_norm.append(key + " Norm") # monta lista com nomes dos atributos normalizados
		else:
			keys_norm.append(key)

	return lista_dicionarios_norm, keys_norm # retorna a lista de dicionários normalizada