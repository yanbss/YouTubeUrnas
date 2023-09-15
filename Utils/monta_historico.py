import csv, glob, os
import time

from YouTube import YouTube

bot = YouTube()

bot.instalaAdBlock()

usuario = input('E-mail da Conta Google para login: ')
senha = input('Senha da Conta Google: ')
bot.fazLogin(usuario, senha)

arq = csv.reader(open('../../resultados/etapa1/final/final_neutros_sem_duplicatas.csv', newline='', encoding='utf-8'))
#arq2 = csv.reader(open('../../resultados/etapa1/final/final_informativos_sem_duplicatas.csv', newline='', encoding='utf-8'))
#arq = csv.reader(open('../../resultados/etapa1/final/final_neutro_sem_duplicatas.csv', newline='', encoding='utf-8'))


lista_videos = []
videos_assistidos = 0

for linha in arq:
    if(linha[0] != 'Link Origem'):
        lista_videos.append(linha[1])

print('Lista completa de vídeos: ')
print(lista_videos)
print('Número de links na lista: ')
print(len(lista_videos))

while(videos_assistidos < 100):
    bot.visitaLink(lista_videos[0])
    print(bot.verificaVideoRemovido('', 1))
    while(bot.verificaVideoRemovido('', 1) != 0):
        del(lista_videos[0])
        bot.visitaLink(lista_videos[0])
        time.sleep(5)
    bot.assisteVideo(lista_videos, 1)
    videos_assistidos += 1
    del(lista_videos[0])
    print('Vídeo atual: ', lista_videos[0])
    print('Vídeos assistidos: ', str(videos_assistidos))
