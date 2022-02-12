
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from functools import partial
import re
import math
import statistics
from scipy.stats import t
import time
import os

import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
#from tf.optimizers.Adam import Adam
from keras.callbacks import EarlyStopping


from valores_iniciais_AG import var_iniciais
from rodar_modelo import avaliar_resposta
from selecao import selecao_melhores_res
from crossover  import cross
from rede_neural import criar_rede_neural

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
import matplotlib.animation as animation

class interface(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #self.app = Tk()
        self.title("otimizador")
        self.geometry("1350x650")
        self["bg"] = "grey"

        self.lista_entry_variaveis = []
        self.lista_entry_variaveis_saida = []
        self.dados_variaveis = []
        self.dados_variaveis_saida = []
        self.button_identities = []
        self.button_identities_saida = []
        self.entry_simu_identities = []
        self.melhor_res_identities = []
        self.lista_restricoes = []
        self.dados_restricoes = []
        self.var_entrada_play = []
        self.equacao_FO = StringVar()
        self.max_min = StringVar()
        self.respostas_simu = []
        self.lista_melhor_solucao = []
        self.lista_verificacao = []
        self.lista_FO = []
        self.porcentagem = 0.95
        self.cont = 0
        self.max_min.set("min")

        pastaApp = os.path.dirname(__file__)
        #photo = PhotoImage(file = pastaApp+'\\imagem_play.png')

        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)

        self.AreaOpcoes = Frame (self, width = 1350, height = 100, relief = "raise")
        self.AreaOpcoes.place(x = 0, y = 0)

        self.rodar_simu = Button(self.AreaOpcoes, width = 20,text = "play",command = self.enviar_dados)
        self.rodar_simu.place(x=500, y=50)
        self.AreaBotoes = Frame (self, width = 200, height = 598, relief = "raise")
        self.AreaBotoes.place(x = 0, y = 102)

        self.AreaTrabalho = Frame (self, width = 1148, height = 598, relief = "raise")
        self.AreaTrabalho.place(x = 202, y= 102)

        self.linguagem = Button(self.AreaBotoes, width = 20, text = "endereco da simalcao", command = self.tela_simulacao)
        self.linguagem.place(x=10, y=20)

        self.variaveis_entrada = Button(self.AreaBotoes, width = 20, text = "variaveis de entrada", command = self.tela_variaveis)
        self.variaveis_entrada.place(x=10, y=50)

        self.variaveis_saida = Button(self.AreaBotoes, width = 20, text = "variaveis de saida", command = self.tela_variaveis_saida)
        self.variaveis_saida.place(x=10, y=80)

        self.retricoes = Button(self.AreaBotoes, width = 20, text = "restricoes", command = self.funcao_restricoes_inicial)
        self.retricoes.place(x=10, y=110)

        self.FO = Button(self.AreaBotoes, width = 20, text = "função objetivo", command = self.funcao_tela_inicial_FO)
        self.FO.place(x=10, y=150)
        #self.app.mainloop()

    def  teste_hipotese(self, FO):
        print(f"lista FO: {self.lista_FO}")
        h = 0.1
        if len(self.lista_FO) < 3:
            return False
        self.lista_verificacao.clear()
        for i in range(len(self.lista_FO)-3,len(self.lista_FO)):
            self.lista_verificacao.append(self.lista_FO[i])
        print(f"lista vericacao: {self.lista_verificacao}")
        media = statistics.mean(self.lista_verificacao)
        variancia = statistics.variance(self.lista_verificacao, media)
        desvio_padrao = math.sqrt(variancia)
        #valor_t = (media - FO)/(math.sqrt(variancia)/math.sqrt(len(self.lista_FO)))
        #valor_t = scipy.stats.t.ppf((1+conf)/2., len(self.interv)-1)
        alpha = (1-self.porcentagem)/2
        T = t.ppf(1-alpha, df=len(self.lista_verificacao)-1)

        x= T*desvio_padrao # precisao

        if x <= h*media:
            return True
        else:
            return False

    def  animate(self):
        xList = []
        yList = []
        if len(self.lista_melhor_solucao) > 5:
            for i in range(len(self.lista_melhor_solucao)-5, len(self.lista_melhor_solucao)):
                xList.append(i+1)
                yList.append(self.lista_melhor_solucao[i])
        else:
            for i in range(0, len(self.lista_melhor_solucao)):
                xList.append(i+1)
                yList.append(self.lista_melhor_solucao[i])
        self.a.clear()
        self.a.plot(xList, yList)
    def enviar_dados(self):
        self.dados__play_simulacao = Frame (self, width = 1148, height = 598,relief = "raise")
        self.dados__play_simulacao.place(x = 202, y= 102)

        for i in range(0,len(self.dados_variaveis)+1):
            self.respostas_simu.append(" ")


        self.label_res = Label(self.dados__play_simulacao,text = "resultado da simulação",borderwidth=2,width = 21,highlightbackground="#37d3ff",relief="solid")
        self.label_res.place(x = 30, y= 80)
        self.var_play_simulacao = Frame(self.dados__play_simulacao, width = 600, height = 298, relief = "raise" )
        self.var_play_simulacao.place(x = 30, y= 100)

        self.frame_grafico_simulacao = Frame(self.dados__play_simulacao, width = 600, height = 298, relief = "raise" )
        self.frame_grafico_simulacao.place(x = 250, y= 150)


        #toolbar = NavigationToolbar2TkAgg(canvas, self.frame_grafico_simulacao)
        #toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


        self.melhor_solucao_simulacao = Frame(self.dados__play_simulacao, width = 600, height = 298, relief = "raise" )
        self.melhor_solucao_simulacao.place(x = 250, y= 25)
        for i in range(0,len(self.dados_variaveis)+1):


            if i == len(self.dados_variaveis):
                self.texto_var_play = Label(self.var_play_simulacao, borderwidth=2, text = "FO",width = 10,highlightbackground="#37d3ff",relief="solid")
                self.texto_var_play.grid(row=i, column = 0)

                self.texto_melhor_res = Label(self.melhor_solucao_simulacao, borderwidth=2, text = "FO",width = 10,highlightbackground="#37d3ff",relief="solid")
                self.texto_melhor_res.grid(row=0, column = i)
            else:
                self.texto_var_play = Label(self.var_play_simulacao, borderwidth=2, text = self.dados_variaveis[i][1].get(),width = 10,highlightbackground="#37d3ff",relief="solid")
                self.texto_var_play.grid(row=i, column = 0)

                self.texto_melhor_res = Label(self.melhor_solucao_simulacao, borderwidth=2, text = self.dados_variaveis[i][1].get(),width = 10,highlightbackground="#37d3ff",relief="solid")
                self.texto_melhor_res.grid(row=0, column = i)

            self.entry_simu_identities.append(StringVar())
            self.var_entrada_play = Label(self.var_play_simulacao, textvariable = self.entry_simu_identities[i], borderwidth=2,bg = "white",width = 10,highlightbackground="#37d3ff",relief="solid")
            self.var_entrada_play.grid(row=i, column = 1)

            self.melhor_res_identities.append(StringVar())
            self.var_melhor_entrada_play = Label(self.melhor_solucao_simulacao, textvariable = self.melhor_res_identities[i], borderwidth=2,bg = "white",width = 10,highlightbackground="#37d3ff",relief="solid")
            self.var_melhor_entrada_play.grid(row=1, column = i)
            #print(f"criar entry {i} entry: {self.var_entrada_play}")


        for i in range(0 , len(self.lista_restricoes)):
            self.dados_restricoes.append(["","",""])
            self.string =  str(self.lista_restricoes[i].get())
            for j in range(0 , len(self.dados_variaveis)):
                self.padrao = re.search(str(self.dados_variaveis[j][1].get()), self.string)

                if self.padrao:
                    self.dados_restricoes[i][0] = self.dados_restricoes[i][0] + " " +  self.dados_variaveis[j][1].get()
            for j in range(0 , len(self.dados_variaveis_saida)):
                self.padrao = re.search(str(self.dados_variaveis_saida[j].get()), self.string)

                if self.padrao:
                    self.dados_restricoes[i][0] = self.dados_restricoes[i][0] + " " +  self.dados_variaveis_saida[j].get()
            self.sinal = ["<=",">=","<",">","="]
            tipo_sinal = None
            cont = 0
            while tipo_sinal == None:
                tipo_sinal = re.search(self.sinal[cont], self.string)
                cont = cont + 1

                #if cont >= len(self.sinal):
                #    tipo_sinal = True

            self.dados_restricoes[i][2] = self.sinal[cont-1]
            self.restricao_separada = self.string.split(self.sinal[cont-1])
            #print(self.restricao_separada)
            self.restricao_separada[1] = self.restricao_separada[1].strip()
            for k in range(0,len(self.restricao_separada[1])):
                if self.restricao_separada[1][k] == '+':
                    self.restricao_separada[1][k] = '-'
                if self.restricao_separada[1][k] == '-':
                    self.restricao_separada[1][k] = '+'
            if self.restricao_separada[1][0] == '+' or self.restricao_separada[1][0] == '-':
                self.dados_restricoes[i][1] = self.restricao_separada[0] + " " + self.restricao_separada[1]
            else:
                self.dados_restricoes[i][1] = self.restricao_separada[0] + " - " + self.restricao_separada[1]

        self.dados_equacao_FO = ["",self.equacao_FO.get()]
        self.string =  str(self.equacao_FO.get())
        for j in range(0 , len(self.dados_variaveis)):
            self.padrao = re.search(str(self.dados_variaveis[j][1].get()), self.string)

            if self.padrao:
                self.dados_equacao_FO[0] = self.dados_equacao_FO[0] + " " +  self.dados_variaveis[j][1].get()
        for j in range(0 , len(self.dados_variaveis_saida)):
            self.padrao = re.search(str(self.dados_variaveis_saida[j].get()), self.string)

            if self.padrao:
                self.dados_equacao_FO[0] = self.dados_equacao_FO[0] + " " +  self.dados_variaveis_saida[j].get()
        print(f"equacao_FO: {self.dados_equacao_FO}")
        dados_de_entrada = []
        limites = []
        dados_de_saida = []
        tipo_var_entrada = []
        for j in range(0 , len(self.dados_variaveis)):
            dados_de_entrada.append(str(self.dados_variaveis[j][1].get()))
            limites.append([int(self.dados_variaveis[j][0].get()),int(self.dados_variaveis[j][2].get())])
            if self.dados_variaveis[j][3].get() == "inteiro":
                tipo_var_entrada.append(0)
            else:
                tipo_var_entrada.append(1)
        for j in range(0 , len(self.dados_variaveis_saida)):
            dados_de_saida.append(str(self.dados_variaveis_saida[j].get()))
        endereco_simualacao = self.endereco_simu.get()
        endereco_entrada = self.endereco_arq_entrada.get()
        endereco_saida   = self.endereco_arq_saida.get()

        if self.max_min.get() == "min":
            max_ou_min = 0
        else:
            max_ou_min = 1

        if self.ling.get() == "python":
            linguagem  = 0
        elif self.ling.get() == "R":
            linguagem  = 1
        else:
            linguagem  = 2
        """
        print(dados_de_entrada)
        print(dados_de_saida)
        print(limites)
        print(self.dados_restricoes)
        print(endereco_simualacao)
        print(endereco_entrada)
        print(endereco_saida)
        print(linguagem)
        """
        model = Sequential()
        model.add(Dense(20, input_shape=(len(dados_de_entrada),), activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(25, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(80, activation='relu'))
        model.add(Dropout(0.7))
        model.add(Dense(25, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(20, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(1,))
        model.compile(keras.optimizers.Adam(learning_rate=0.003), 'mean_squared_error')

        self.Pop = var_iniciais(dados_de_entrada, dados_de_saida, limites, tipo_var_entrada, self.dados_restricoes)

        inicio_neural = 0
        resposta_meta = []
        media_score = 0
        media_MSE = 0
        lista_entradas_rn = []
        if max_ou_min == 0:
            FO = 1000000
            FO_rodada = 1000000
            valor_inicial_FO = 1000000
        else:
            FO = -1000000
            FO_rodada = -1000000
            valor_inicial_FO = -1000000

        inicio = time.time()
        geracoes = 0
        while not self.teste_hipotese(FO) and geracoes <= 20:
            geracoes += 1
        #for j in range(0, 5):
            #simula os 50 dados de entrada
            #print("\nPop")
            #print(Pop)
            for i in range(0,len(self.Pop)):


                self.Pop2, valor_real = avaliar_resposta(self.Pop[i],resposta_meta,FO,model,media_score,media_MSE,linguagem,max_ou_min,endereco_simualacao,endereco_entrada,endereco_saida, dados_de_entrada, dados_de_saida, self.dados_restricoes, self.dados_equacao_FO)
                #self.Pop[i].append(self.Pop2)

                if valor_real != 0:
                    lista_entradas_rn.append([])
                for k in range(0,len(self.Pop[i])):

                    self.respostas_simu[k] = self.Pop[i][k]
                    #self.respostas_simu[k] = str(self.Pop[k])
                    if valor_real != 0:
                        if k == len(self.Pop[i])-1:
                            lista_entradas_rn[len(lista_entradas_rn)-1].append(valor_real)
                        else:
                            lista_entradas_rn[len(lista_entradas_rn)-1].append(self.Pop[i][k])
                if max_ou_min == 0:
                    if self.Pop[i][len(self.Pop[i])-1] < FO_rodada:
                        FO_rodada = self.Pop[i][len(self.Pop[i])-1]
                    if self.Pop[i][len(self.Pop[i])-1] < FO:
                        print("melhorou solução")
                        melhor_solucao = self.Pop[i]
                        FO = self.Pop[i][len(self.Pop[i])-1]

                        for l in range(0,len(self.Pop[i])):
                            bname = (self.melhor_res_identities[l])
                            bname.set(str(self.Pop[i][l]))

                        print(FO)
                else:
                    if self.Pop[i][len(self.Pop[i])-1] > FO_rodada:
                        FO_rodada = self.Pop[i][len(self.Pop[i])-1]
                    if self.Pop[i][len(self.Pop[i])-1] > FO:
                        print("melhorou solução")
                        melhor_solucao = self.Pop[i]
                        FO = self.Pop[i][len(self.Pop[i])-1]

                        for l in range(0,len(self.Pop[i])):
                            bname = (self.melhor_res_identities[l])
                            bname.set(str(self.Pop[i][l]))

                        print(FO)
                self.var_entrada_play.config(bg="white")
                for l in range(0,len(self.Pop[i])):
                    bname = (self.entry_simu_identities[l])

                    if l == len(self.Pop[i])-1 and valor_real != 0:
                        bname.set(str(valor_real))
                        if self.Pop[i][l] != valor_real:
                            self.var_entrada_play.config(bg="red")
                    else:
                        bname.set(str(self.Pop[i][l]))

                self.update()
                #self.after(0, self.tela_resultados)
            self.lista_FO.append(FO_rodada)
            FO_rodada = valor_inicial_FO
            model,media_score,media_MSE = criar_rede_neural(lista_entradas_rn)
            self.PopInt = selecao_melhores_res(self.Pop)
            self.Pop.clear()
            self.Pop = cross(self.PopInt, dados_de_entrada, dados_de_saida, limites, tipo_var_entrada, self.dados_restricoes)
        fim = time.time()
        print(f"solução final: {melhor_solucao}")
        print(f"tempo de execução: {fim - inicio}")

        print(f"lista entrada: {len(lista_entradas_rn)}")
        print(f"resposta_meta: {len(resposta_meta)}")
        print(f"inicio_neural: {inicio_neural}")



    def analise_dados_simulacao(self):


        print(self.endereco_simu.get())
        print(self.endereco_arq_entrada.get())
        print(self.endereco_arq_saida.get())

        arquivo_entrada = open(self.endereco_arq_entrada.get(), 'r')
        dados_entrada = arquivo_entrada.read()
        dados_entrada = dados_entrada.split("\n")
        dados_entrada[0] = dados_entrada[0].split(",")

        for i in range(0,len(dados_entrada[0])):
            self.dados_variaveis.append([])
            for j in range(0,4):
                self.dados_variaveis[i].append(StringVar())
            self.dados_variaveis[i][1].set(dados_entrada[0][i])

        arquivo_saida = open(self.endereco_arq_saida.get(), 'r')
        dados_saida = arquivo_saida.read()
        dados_saida = dados_saida.split("\n")
        dados_saida[0] = dados_saida[0].split(",")

        for i in range(0,len(dados_saida[0])):
            self.dados_variaveis_saida.append(StringVar())
            self.dados_variaveis_saida[i].set(dados_saida[0][i])
    def tela_simulacao(self):
        self.dados_simulacao = Frame (self, width = 1148, height = 598, relief = "raise")
        self.dados_simulacao.place(x = 202, y= 102)
        self.ling = StringVar(self.dados_simulacao)
        self.texto_linguagem = Label(self.dados_simulacao, text = "linguagem")
        self.texto_linguagem.place(x=100,y=10)
        self.menu_linguagens = OptionMenu(self.dados_simulacao,self.ling,"python","R","C","C++")
        self.menu_linguagens.place(x=200,y=10)
        self.texto_end_simu = Label(self.dados_simulacao, text = "endereço simulação")
        self.texto_end_simu.place(x=10,y=100)
        self.endereco_simu = Entry(self.dados_simulacao)
        self.endereco_simu.place(x = 200, y= 100, width = 500)
        self.texto_arq_entrada = Label(self.dados_simulacao, text = "endereço arquivo de entrada")
        self.texto_arq_entrada.place(x=10,y=200)
        self.endereco_arq_entrada = Entry(self.dados_simulacao)
        self.endereco_arq_entrada.place(x = 200, y= 200, width = 500)
        self.texto_arq_saida = Label(self.dados_simulacao, text = "endereço arquivo de saida")
        self.texto_arq_saida.place(x=10,y=300)
        self.endereco_arq_saida = Entry(self.dados_simulacao)
        self.endereco_arq_saida.place(x = 200, y= 300, width = 500)
        self.aplicar_endereco = Button(self.dados_simulacao, width = 20, text = "aplicar", command = self.analise_dados_simulacao)
        self.aplicar_endereco.place(x=10, y=380)



    def tela_variaveis(self):
        self.tela_variaveis = Frame(self, width = 1148, height = 598, relief = "raise" )
        self.tela_variaveis.place(x = 202, y= 102)
        #self.num_variaveis = Entry(self.tela_variaveis)
        #self.num_variaveis.place(x=150,y =30)
        #self.atulizar_var = Button(self.tela_variaveis, width = 20, text = "atualizar", command = self.lista_variaveis )
        #self.atulizar_var.place(x=200,y =30)
        self.tabela_var = Frame(self.tela_variaveis, width = 500, height = 300, relief = "raise" )
        self.tabela_var.place(x = 30, y= 100)
        self.label_min = Label(self.tabela_var ,text = "valor minimo")
        self.label_min.grid(row=0,column = 0)
        self.label_nome = Label(self.tabela_var ,text = "nome")
        self.label_nome.grid(row=0,column = 1)
        self.label_max = Label(self.tabela_var ,text = "valor maximo")
        self.label_max.grid(row=0,column = 2)
        self.label_tipo = Label(self.tabela_var ,text = "tipo")
        self.label_tipo.grid(row=0,column = 3)

        for i in range(0,len(self.dados_variaveis)):
            self.lista_entry_variaveis.append([])
            self.lista_entry_variaveis[i].append(Entry(self.tabela_var, textvariable= self.dados_variaveis[i][0]))
            self.lista_entry_variaveis[i][0].grid(row=i+1, column = 0)
            self.lista_entry_variaveis[i].append(Entry(self.tabela_var, textvariable= self.dados_variaveis[i][1]))
            self.lista_entry_variaveis[i][1].grid(row=i+1, column = 1)
            self.lista_entry_variaveis[i].append(Entry(self.tabela_var, textvariable= self.dados_variaveis[i][2]))
            self.lista_entry_variaveis[i][2].grid(row=i+1, column = 2)
            self.tipo_variavel = StringVar(self.tabela_var)
            self.lista_entry_variaveis[i].append(OptionMenu(self.tabela_var,self.dados_variaveis[i][3],"continuo","inteiro"))
            self.lista_entry_variaveis[i][3].grid(row=i+1, column = 3)

    
    def tela_variaveis_saida(self):
        self.tela_variaveis_saida = Frame(self, width = 1148, height = 598, relief = "raise" )
        self.tela_variaveis_saida.place(x = 202, y= 102)
        #self.num_variaveis_saida = Entry(self.tela_variaveis_saida)
        #self.num_variaveis_saida.place(x=150,y =30)
        #self.atulizar_var = Button(self.tela_variaveis_saida, width = 20, text = "atualizar", command = self.lista_variaveis_saida )
        #self.atulizar_var.place(x=200,y =30)
        self.tabela_var_saida = Frame(self.tela_variaveis_saida, width = 500, height = 300, relief = "raise" )
        self.tabela_var_saida.place(x = 30, y= 100)
        self.label_nome = Label(self.tabela_var_saida ,text = "nome")
        self.label_nome.grid(row=0,column = 0)

        for i in range(0,len(self.dados_variaveis_saida)):
            self.lista_entry_variaveis_saida.append(Entry(self.tabela_var_saida, textvariable= self.dados_variaveis_saida[i]))
            self.lista_entry_variaveis_saida[i].grid(row=i+1, column = 0)

    def inserir_variavel(self,n):
        bname = (self.button_identities[n])

        self.restricao.insert(END, bname['text'])
    def inserir_variavel_saida(self,n):
        bname = (self.button_identities_saida[n])

        self.restricao.insert(END, bname['text'])

    def funcao_restricoes_inicial(self):

        self.tela_restricoes_inicial = Frame(self, width = 1148, height = 498, relief = "raise" )
        self.tela_restricoes_inicial.place(x = 202, y= 102)

        self.tela_lista_restricao = Frame(self.tela_restricoes_inicial, width = 448, height = 198 )
        self.tela_lista_restricao.place(x = 100, y= 102)
        for i in range(0,len(self.lista_restricoes)):
            self.tabela_restricoes = Button(self.tela_lista_restricao ,text = self.lista_restricoes[i].get(), command = partial(self.funcao_restricoes, i))
            self.tabela_restricoes.grid(row=i,column = 0)
        print(self.lista_restricoes)
        self.criar_restricao = Button(self.tela_restricoes_inicial , width = 20, text = "criar restricao", command = partial(self.funcao_restricoes, len(self.lista_restricoes)) )
        self.criar_restricao.place(x=100,y =450)
    def teste2(self):
        #self.tela_restricoes.reset()
        self.tela_restricoes.tkraise()
    def teste(self):
        #self.tela_restricoes_inicial.reset()
        self.tela_restricoes_inicial.tkraise()
        #self.tela_restricoes_inicial
        for i in range(0,len(self.lista_restricoes)):
            self.tabela_restricoes = Button(self.tela_lista_restricao ,text = self.lista_restricoes[i].get())
            self.tabela_restricoes.grid(row=i,column = 0)
    def funcao_restricoes(self,num_res):

        if num_res == len(self.lista_restricoes):
            self.lista_restricoes.append(StringVar())
        self.tela_restricoes = Frame(self, width = 1148, height = 498, relief = "raise" )
        self.tela_restricoes.place(x = 202, y= 102)

        self.tela_restricoes_var = Frame(self.tela_restricoes, width = 548, height = 308, relief = "raise" )
        self.tela_restricoes_var.place(x = 202, y= 12)
        for i in range(0,len(self.dados_variaveis)):
            self.linguagem = Button(self.tela_restricoes_var, width = 20, text = self.dados_variaveis[i][1].get(), command=partial(self.inserir_variavel,i))
            self.linguagem.grid(row=i,column = 0)
            self.button_identities.append(self.linguagem)

        self.tela_restricoes_var_saida = Frame(self.tela_restricoes, width = 548, height = 308, relief = "raise" )
        self.tela_restricoes_var_saida.place(x = 202, y= 252)
        for i in range(0,len(self.dados_variaveis_saida)):
            self.linguagem_saida = Button(self.tela_restricoes_var_saida, width = 20, text = self.dados_variaveis_saida[i].get(), command=partial(self.inserir_variavel_saida,i))
            self.linguagem_saida.grid(row=i,column = 0)
            self.button_identities_saida.append(self.linguagem_saida)

        self.salvar_restricao = Button(self.tela_restricoes , width = 20, text = "salvar restricao", command = self.funcao_restricoes_inicial )
        self.salvar_restricao.place(x=100,y = 450)

        self.restricao = Entry(self.tela_restricoes, width = 100, textvariable= self.lista_restricoes[num_res])
        self.restricao.place(x=20,y= 400)

    def funcao_tela_inicial_FO(self):

        self.tela_inicial_FO = Frame(self, width = 1148, height = 498, relief = "raise" )
        self.tela_inicial_FO.place(x = 202, y= 102)

        self.tabela_var_fo = Frame(self.tela_inicial_FO, width = 500, height = 300, relief = "raise" )
        self.tabela_var_fo.place(x = 30, y= 100)

        self.label_max_min = Label(self.tabela_var_fo ,text = "maximo ou minino")
        self.label_max_min.grid(row=0,column = 0)
        self.label_funcao = Label(self.tabela_var_fo ,text = "função")
        self.label_funcao.grid(row=0,column = 1)
        self.label_alterar = Label(self.tabela_var_fo ,text = "alterar função objetivo")
        self.label_alterar.grid(row=0,column = 2)


        self.select_max_min_fo = OptionMenu(self.tabela_var_fo,self.max_min,"max","min")
        self.select_max_min_fo.grid(row=1, column = 0)
        self.label_texto_funcao = Label(self.tabela_var_fo ,text = self.equacao_FO.get())
        self.label_texto_funcao.grid(row=1,column = 1)
        self.button_texto_fo = Button(self.tabela_var_fo, width = 20, text = "alterar", command = self.funcao_objetivo)
        self.button_texto_fo.grid(row=1,column = 2)

    def funcao_objetivo(self):


        self.tela_FO = Frame(self, width = 1148, height = 498, relief = "raise" )
        self.tela_FO.place(x = 202, y= 102)

        self.tela_FO_var = Frame(self.tela_FO, width = 548, height = 308, relief = "raise" )
        self.tela_FO_var.place(x = 202, y= 52)
        for i in range(0,len(self.dados_variaveis)):
            self.linguagem = Button(self.tela_FO_var, width = 20, text = self.dados_variaveis[i][1].get(), command=partial(self.inserir_variavel,i))
            self.linguagem.grid(row=i,column = 0)
            self.button_identities.append(self.linguagem)

        self.tela_FO_var_saida = Frame(self.tela_FO, width = 548, height = 308, relief = "raise" )
        self.tela_FO_var_saida.place(x = 202, y= 202)
        for i in range(0,len(self.dados_variaveis_saida)):
            self.linguagem_saida = Button(self.tela_FO_var_saida, width = 20, text = self.dados_variaveis_saida[i].get(), command=partial(self.inserir_variavel_saida,i))
            self.linguagem_saida.grid(row=i,column = 0)
            self.button_identities_saida.append(self.linguagem_saida)



        self.salvar_FO = Button(self.tela_FO , width = 20, text = "salvar restricao", command = self.funcao_tela_inicial_FO)
        self.salvar_FO.place(x=100,y = 450)

        self.restricao = Entry(self.tela_FO, width = 100, textvariable= self.equacao_FO)
        self.restricao.place(x=20,y= 400)



" sera chamado no executavel"
if __name__ == '__main__' :
    app = interface()
    app.mainloop()
