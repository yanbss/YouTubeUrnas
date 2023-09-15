#Módulo com as funções do bot do YouTube
from Utils.YouTube import YouTube

#Arquivos e outros
import csv
import os
import random
import time

def main():

    #login

    bot = YouTube()
    bot.instalaAdBlock()

    usuario = input('E-mail da Conta Google para login: ')
    senha = input('Senha da Conta Google: ')

    bot.fazLogin(usuario, senha) #informativo << NÃO FOI CONTAGEM

    termos = ['urna eletrônica', 'urnas eletronicas', 'bolsonaro embaixadores urnas', 'bolsonaro urnas eletrônicas', 'nova urna eletronica 2022']
    filtros = ['relevância', 'data', 'contagem', 'classificação']

    for termo in termos:
        for filtro in filtros:
            arq_pesquisa = csv.DictWriter(open('../resultados/etapa3/informativo/pesquisa/' + termo + '_' + filtro + '.csv', 'w', newline='', encoding='utf-8'), fieldnames = ['Link', 'id', 'Título', 'Classificação', 'Classificação Normalizada'])
            arq_recomendados = csv.DictWriter(open('../resultados/etapa3/informativo/relacionados/' + termo + '_' + filtro + '.csv', 'w', newline='', encoding='utf-8'), fieldnames = ['Link Origem', 'Link', 'id', 'Título', 'Classificação', 'Classificação Normalizada'])
            arq_pesquisa.writeheader()
            arq_recomendados.writeheader()
            links_pesquisa = bot.pesquisa(termo, filtro)
            num_video = 1
            print('Termo "' + termo + '" - ' + 'Filtro: ' + filtro)
            for link in links_pesquisa: #extrai os 10 recomendados de cada vídeo
                print('Vídeo ' + str(num_video) + ' - ', end = '', flush = True)
                num_video += 1
                bot.visitaLink(link)
                #pm = bot.metricaPopularidade()
                id = bot.extraiId(link)
                titulo = bot.extraiTitulo()
                arq_pesquisa.writerow({'Link': link, 'id': id, 'Título': titulo, 'Classificação': '-', 'Classificação Normalizada': '-'})
                links_recomendados = bot.extraiLinkRecomendados('video')
                num_recomendado = 1
                for recomendado in links_recomendados:
                    print('R' + str(num_recomendado) + ' ', end = '', flush = True)
                    num_recomendado += 1
                    bot.visitaLink(recomendado)
                    #pm = bot.metricaPopularidade()
                    id = bot.extraiId(recomendado)
                    titulo = bot.extraiTitulo()
                    arq_recomendados.writerow({'Link Origem': link, 'Link': recomendado, 'id': id, 'Título': titulo, 'Classificação': '-', 'Classificação Normalizada': '-'})#, 'Métrica de Popularidade': pm[0], 'Visualizações': pm[1], 'Likes': pm[2], 'Comentários': pm[3], 'Classificação': '-'})
                print() #troca linha
            #arq_pesquisa.close()
            #arq_recomendados.close()

if __name__ == "__main__":
    main()
