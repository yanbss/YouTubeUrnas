#Módulo com as funções do bot do YouTube
from Utils.YouTube import YouTube

#Overlap Coefficient
import py_stringmatching as sm

#Arquivos e outros
import csv
import os
import random
import time

def main():

    for i in range(9, 10):

        arq_desinformativos = csv.reader(open('../resultados/etapa0/etapa0online.csv', newline='', encoding='utf-8'))
        arq_saida = csv.DictWriter(open('../resultados/etapa2/etapa2_' + str(i) + '.csv', 'w', newline='', encoding='utf-8'), fieldnames = ['Vídeos assistidos', 'Coeficiente de Overlap'])
        arq_saida.writeheader()
        lista_desinformativos = []
        coef = 0.0

        for linha in arq_desinformativos:
            if(not 'shorts' in linha): #não pega shorts porque não consegue extrair o tempo
                lista_desinformativos.append(linha)

        del lista_desinformativos[0] #remove a primeira linha - cabeçalho

        linha_video_base = random.choice(lista_desinformativos) #seleciona o vídeo que irá ficar voltando para comparar as recomendações
        lista_desinformativos.remove(linha_video_base) #remove da lista
        video_base = linha_video_base[0] #extrai só o link da linha que pegou

        video_atual = video_base
        videos_assistidos = 0
        overlap_coefficient = sm.OverlapCoefficient()
        recomendados = []

        #INICIALIZA O BOT, INSTALA O ADBLOCK E FAZ LOGIN:

        if(i == 9):
            usuario = input('E-mail da Conta Google para login: ')
            senha = input('Senha da Conta Google: ')
            bot = YouTube() #inicia o selenium bot com o FireFox já ativado
            bot.instalaAdBlock()
            bot.fazLogin(usuario, senha)

        while coef < 1.0:

            bot.visitaLink(video_atual)

            time.sleep(10)

            if not recomendados: #primeira rodada, pega os recomendados do vídeo base e vai para o primeiro vídeo aleatório da lista
                recomendados = bot.extraiLinkRecomendados('video')
                linha_video_atual = random.choice(lista_desinformativos)
                lista_desinformativos.remove(linha_video_atual)
                video_atual = linha_video_atual[0]

            else:
                bot.assisteVideo(lista_desinformativos, 2) #assiste 80% do vídeo selecionado aleatoriamente
                videos_assistidos += 1

                bot.visitaLink(video_base) #volta pro vídeo base
                time.sleep(10)
                recomendados_teste = bot.extraiLinkRecomendados('video') #pega as recomendações

                coef = overlap_coefficient.get_sim_score(recomendados, recomendados_teste) #faz o Overlap Coefficient entre as duas listas
                print('Coeficiente de Overlap: ' + str(coef))

                for video in recomendados_teste:
                    recomendados.append(video)

                linha_video_atual = random.choice(lista_desinformativos)
                lista_desinformativos.remove(linha_video_atual)
                video_atual = linha_video_atual[0]

            arq_saida.writerow({'Vídeos assistidos': videos_assistidos, 'Coeficiente de Overlap': coef})

        bot.limpaHistorico()
        del(overlap_coefficient)

        print('rodada ' + str(i) + ' concluída, começando próxima rodada...')

        time.sleep(1200) #espera 20 minutos pra próxima iteração

if __name__ == "__main__":
    main()
