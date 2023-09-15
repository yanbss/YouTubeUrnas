#Módulo com as funções do bot do YouTube
from Utils.YouTube import YouTube

#Arquivos e outros

import csv
import time
import os

def main():

    entrada = csv.reader(open('../entradas/listaTSE.csv', newline='', encoding='utf-8'))

    #deleta os arquivos anteriores, caso existam
    try:
        os.remove('../resultados/etapa0/junho23/etapa0online.csv')
        os.remove('../resultados/etapa0/junho23/etapa0removidos.csv')
    except OSError:
        print('Impossível remover os arquivos')

    saida = csv.DictWriter(open('../resultados/etapa0/junho23/etapa0online.csv', 'w', newline='', encoding='utf-8'), fieldnames = ['Link', 'Métrica de Popularidade', 'Visualizações', 'Likes', 'Comentários'])
    saida2 = csv.DictWriter(open('../resultados/etapa0/junho23/etapa0removidos.csv', 'w', newline='', encoding='utf-8'), fieldnames = ['Link', 'Código Remoção'])
    saida.writeheader()
    saida2.writeheader()

    cont_videos_online = 0
    cont_videos_removidos = 0
    cont_total = 0

    listaSemDuplicados = []

    for linha in entrada:
        if('youtu' in linha[0]): #inspeciona as linhas do arquivo e joga para dentro de uma lista, caso o link já não esteja na lista
            if linha[0] not in listaSemDuplicados: #impossibilita a inserção de itens duplicado
                listaSemDuplicados.append(linha[0])

    print('Número de vídeos totais (duplicados eliminados): ' + str(len(listaSemDuplicados)))

    bot = YouTube() #inicia o selenium bot
    bot.instalaAdBlock()

    for link in listaSemDuplicados:

        res = bot.verificaVideoRemovido(link, 0)

        cont_total += 1

        print('\nVídeos processados: ', cont_total)

        if(res == 0): #vídeo online
            cont_videos_online += 1
            #pm = bot.metricaPopularidade()
            pm = [1, 1, 1, 1]
            saida.writerow({'Link': link, 'Métrica de Popularidade': pm[0], 'Visualizações': pm[1], 'Likes': pm[2], 'Comentários': pm[3]})
        else:
            cont_videos_removidos += 1
            saida2.writerow({'Link': link, 'Código Remoção': res})
            print('Código Remoção: ' + str(res))

    print('Total de vídeos online: ' + str(cont_videos_online))
    print('Total de vídeos removidos: ' + str(cont_videos_removidos))

if __name__ == "__main__":
    main()
