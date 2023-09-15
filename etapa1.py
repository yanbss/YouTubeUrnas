from Utils.YouTube import YouTube

import csv
import os

def main():

    bot = YouTube()
    bot.instalaAdBlock()

    termos = ['urna eletrônica', 'urnas eletronicas', 'bolsonaro embaixadores urnas', 'bolsonaro urnas eletrônicas', 'nova urna eletronica 2022']
    filtros = ['relevância', 'data', 'contagem', 'classificação']

    for termo in termos:
        for filtro in filtros:
            arq_pesquisa = csv.DictWriter(open('../resultados/etapa1/pesquisa/' + termo + '_' + filtro + '.csv', 'w', newline='', encoding='utf-8'), fieldnames = ['Link', 'id', 'Título', 'Métrica de Popularidade', 'Visualizações', 'Likes', 'Comentários', 'Classificação'])
            arq_recomendados = csv.DictWriter(open('../resultados/etapa1/relacionados/' + termo + '_' + filtro + '.csv', 'w', newline='', encoding='utf-8'), fieldnames = ['Link Origem', 'Link', 'id', 'Título', 'Métrica de Popularidade', 'Visualizações', 'Likes', 'Comentários', 'Classificação'])
            arq_pesquisa.writeheader()
            arq_recomendados.writeheader()
            links_pesquisa = bot.pesquisa(termo, filtro)
            num_video = 1
            print('Termo "' + termo + '" - ' + 'Filtro: ' + filtro)
            for link in links_pesquisa: #extrai os 10 recomendados de cada vídeo
                print('Vídeo ' + str(num_video) + ' - ', end = '', flush = True)
                num_video += 1
                bot.visitaLink(link)
                pm = bot.metricaPopularidade()
                id = bot.extraiId(link)
                titulo = bot.extraiTitulo()
                arq_pesquisa.writerow({'Link': link, 'id': id, 'Título': titulo, 'Métrica de Popularidade': pm[0], 'Visualizações': pm[1], 'Likes': pm[2], 'Comentários': pm[3], 'Classificação': '-'})
                links_recomendados = bot.extraiLinkRecomendados('video')
                num_recomendado = 1
                for recomendado in links_recomendados:
                    print('R' + str(num_recomendado) + ' ', end = '', flush = True)
                    num_recomendado += 1
                    bot.visitaLink(recomendado)
                    pm = bot.metricaPopularidade()
                    id = bot.extraiId(recomendado)
                    titulo = bot.extraiTitulo()
                    arq_recomendados.writerow({'Link Origem': link, 'Link': recomendado, 'id': id, 'Título': titulo, 'Métrica de Popularidade': pm[0], 'Visualizações': pm[1], 'Likes': pm[2], 'Comentários': pm[3], 'Classificação': '-'})
                print() #troca linha

if __name__ == "__main__":
    main()
