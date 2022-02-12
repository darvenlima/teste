
import random
import math

from analise_restricoes import analise_das_restricoes

def cross(PopInt, dados_de_entrada, dados_de_saida, limites_dados_de_entrada, tipo_var_entrada, restricoes):
    cross1 = []
    cross2 = []
    Pop = []
    for i in range(0,int((len(PopInt)/2)-1)):
        prob = random.random()
        if prob < 0.9:
            teste = False
            while teste == False:
                cross1.clear()
                cross2.clear()
                """ escolhe um ponto de corte"""
                corte = random.randint(1, len(PopInt[i])-2)
                """faz o cruzamento dos cromossomos"""
                for j in range(0,len(PopInt[2*i])):
                    if j < corte:
                        cross1.append(PopInt[2*i][j])
                        cross2.append(PopInt[2*i+1][j])
                    else:
                        cross1.append(PopInt[2*i+1][j])
                        cross2.append(PopInt[2*i][j])
                """testa se as duas novas entradas são viáveis na função de restrições"""
                teste1 = analise_das_restricoes(1,dados_de_entrada,cross1,dados_de_saida, 0, restricoes)
                teste2 = analise_das_restricoes(1,dados_de_entrada,cross2,dados_de_saida, 0, restricoes)
                if teste1 == True and teste2 == True:
                    #print("\ncrossover aceito\n")
                    teste = True
            PopInt[2*i].clear()
            PopInt[2*i+1].clear()
            """adiciona as duas novas entradas na lista PopInt"""
            for j in range(0,len(cross1)):
                PopInt[2*i].append(cross1[j])
                PopInt[2*i+1].append(cross2[j])


    #passa os dados do PopInt para o Pop
    for i in range(0,len(PopInt)):
        Pop.append(PopInt[i])

    #Loop da mutação
    for i in range(0,len(Pop)):
        for j in range(0,len(Pop[i])):
            prob = random.random()
            if prob < 1:
                teste = False
                while teste == False:
                    if tipo_var_entrada[j] == 0:
                        Pop[i][j] = random.randint(limites_dados_de_entrada[j][0], limites_dados_de_entrada[j][1])
                    else:
                        Pop[i][j] = random.uniform(limites_dados_de_entrada[j][0], limites_dados_de_entrada[j][1])
                    teste1 = analise_das_restricoes(1,dados_de_entrada,Pop[i],dados_de_saida, 0, restricoes)
                    if teste1 == True:
                        teste = True
    return Pop
