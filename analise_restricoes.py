
from sympy import *
from sympy.parsing.sympy_parser import (parse_expr,standard_transformations, implicit_application)

def analise_fucao_objetivo(nome_dados_de_entrada, dados_chegada, nome_dados_de_saida, dados_saida, funcao_objetivo):
    variaveis = symbols(funcao_objetivo[0])
    #print("\nvariaveis\n")
    #print(restricoes[i][0])
    e = funcao_objetivo[1]
    #print("\nrestricao\n")
    #print(e)
    #e = "x + y + 5"
    transformations = standard_transformations + (implicit_application,)
    e = parse_expr(e, transformations=transformations)
    #print("\nvariaveis_separadas\n")
    #print(variaveis_separadas)
    variaveis_separadas = funcao_objetivo[0].split()
    print(f"variaveis separadas {variaveis_separadas}")
    print(f"nome dados saida {nome_dados_de_saida}")
    for k in range(0,len(variaveis_separadas)):
        for l in range(0,len(nome_dados_de_entrada)):

            if nome_dados_de_entrada[l] == variaveis_separadas[k]:
                if len(variaveis_separadas) > 1:
                    e = e.subs(variaveis[k],dados_chegada[l])
                else:
                    e = e.subs(variaveis,dados_chegada[l])
        for l in range(0,len(nome_dados_de_saida)):

            if nome_dados_de_saida[l] == variaveis_separadas[k]:
                print("\ndados saida\n")
                print(dados_saida[l])
                print("\nvariaveis[k]\n")
                print(variaveis_separadas[k])
                if len(variaveis_separadas) > 1:
                    e = e.subs(variaveis[k],dados_saida[l])
                else:
                    e = e.subs(variaveis,dados_saida[l])
    return e

def analise_das_restricoes(teste_de_entrada,nome_dados_de_entrada, dados_chegada, nome_dados_de_saida, dados_saida, restricoes):
    teste_entrada = 0
    retricao_atendida = 0
    for i in range(0,len(restricoes)):
        teste_entrada = 0
        for j in range(0, len(nome_dados_de_saida)):
            variaveis_separadas = restricoes[i][0].split()

            for k in range(0,len(variaveis_separadas)):
                if nome_dados_de_saida[j] == variaveis_separadas[k]:
                    teste_entrada = 1

        if teste_de_entrada == 0 or teste_entrada == 0:
            variaveis = symbols(restricoes[i][0])
            #print("\nvariaveis\n")
            #print(restricoes[i][0])
            e = restricoes[i][1]
            #print("\nrestricao\n")
            #print(e)
            #e = "x + y + 5"
            transformations = standard_transformations + (implicit_application,)
            e = parse_expr(e, transformations=transformations)
            #print("\nvariaveis_separadas\n")
            #print(variaveis_separadas)
            for k in range(0,len(variaveis_separadas)):
                for l in range(0,len(nome_dados_de_entrada)):

                    if nome_dados_de_entrada[l] == variaveis_separadas[k]:
                        if len(variaveis_separadas) > 1:
                            e = e.subs(variaveis[k],dados_chegada[l])
                        else:
                            e = e.subs(variaveis,dados_chegada[l])
                for l in range(0,len(nome_dados_de_saida)):

                    if nome_dados_de_saida[l] == variaveis_separadas[k]:
                        #print("\ndados saida\n")
                        #print(dados_saida[l])
                        #print("\nvariaveis[k]\n")
                        #print(variaveis)
                        if len(variaveis_separadas) > 1:
                            e = e.subs(variaveis[k],dados_saida[l])
                        else:
                            e = e.subs(variaveis,dados_saida[l])
            #print("\nvalor final\n")
            #print(e)
            #print("\n sinal \n")
            #print(restricoes[i][2])
            if restricoes[i][2] == '<=':
                if e >= 0:
                    #print("\n>= 0\n")
                    return False
            elif restricoes[i][2] == '>=':
                if e <= 0:
                    #print("\n<= 0\n")
                    return False
            elif restricoes[i][2] == '=':
                if e != 0:
                    #print("\n!= 0\n")
                    return False
            elif restricoes[i][1] == '!=':
                if e == 0:
                    #print("\n== 0\n")
                    return False
            elif restricoes[i][2] == '<':
                if e > 0:
                    #print("\n> 0\n")
                    return False
            elif restricoes[i][2] == '>':
                if e < 0:
                    #print("\n< 0\n")
                    return False

    return True
