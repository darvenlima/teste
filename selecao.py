import random
import math



def selecao_melhores_res(Pop):
    PopInt = []
    #print(f"Pop selecao: {Pop}")
    for i in range(0,50):
        """faz a seleção das melhores soluções e armazena no PopInt"""
        escolha1 = random.randint(0, len(Pop)-1)
        escolha2 = random.randint(0, len(Pop)-1)
        #print("escolha1 %f  escolha2 %f"%(Pop[escolha1][len(Pop[escolha1])-1],Pop[escolha2][len(Pop[escolha2])-1]))
        if Pop[escolha1][len(Pop[escolha1])-1] < Pop[escolha2][len(Pop[escolha2])-1]:
            #print("escolha1 melhor")
            PopInt.append([])
            for j in range(0,len(Pop[escolha1])-1):
                PopInt[len(PopInt)-1].append(Pop[escolha1][j])
        else:
            #print("escolha2 melhor")
            PopInt.append([])
            for j in range(0,len(Pop[escolha2])-1):
                PopInt[len(PopInt)-1].append(Pop[escolha2][j])
    return PopInt
