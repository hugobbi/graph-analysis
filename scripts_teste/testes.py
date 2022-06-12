import argparse as ap
import sys

parser = ap.ArgumentParser()
parser.add_argument("-y", "--yee", nargs="+")
args = parser.parse_args()

a = args.yee 

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
    if "-" in entrada[0]:
        return converte_intervalo(entrada[0])
    else:
        lista_intervalo = []
        for i in entrada:
            lista_intervalo.append(int(i)) # transforma os números em inteiros
        return lista_intervalo

#print(a)

#a = processa_int_ou_intervalo(a)

#print(a)

a = "1-10"

print(converte_intervalo(a))