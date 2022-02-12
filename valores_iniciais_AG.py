
import random
import math
from analise_restricoes import analise_das_restricoes


def var_iniciais(dados_de_entrada, dados_de_saida, limites_dados_de_entrada,tipo_var_entrada, restricoes):

    Pop = []
    PopInt = []
    entradas = []

    melhor_s = 0
    melhor_S_max = 0
    melhor_l = 0
    melhor_r = 0

    #inicio = time.time()
    #gera os primeiros 50 cenários
    for num_pop_ini in range(0,50):
        igual = True

        """testa até achar uma solução única e viável"""
        while igual == True:
            entradas.clear()
            """gera um valor para cada entrada dentro dos limites extipulados"""
            for i in range(0,len(dados_de_entrada)):
                if tipo_var_entrada[i] == 0:
                    entradas.append(random.randint(limites_dados_de_entrada[i][0], limites_dados_de_entrada[i][1]))
                else:
                    entradas.append(random.uniform(limites_dados_de_entrada[i][0], limites_dados_de_entrada[i][1]))
            """analisa se a entrada é viável e se é única"""
            igual = False
            if analise_das_restricoes(1,dados_de_entrada, entradas, dados_de_saida, 0, restricoes) == True:
                for i in range(0,len(Pop)):
                    cont_igual = 0
                    for j in range(0,len(dados_de_entrada)):
                        if entradas[j] == Pop[i][j]:
                            cont_igual = cont_igual + 1
                    if cont_igual == len(dados_de_entrada):
                        igual = True
            else:
                #print("\nsolucao inviavel\n")
                igual = True
        Pop.append([])
        """armazena a solução na lista Pop"""
        for j in range(0,len(dados_de_entrada)):
            Pop[len(Pop)-1].append(entradas[j])
        entradas.clear()

    return Pop
