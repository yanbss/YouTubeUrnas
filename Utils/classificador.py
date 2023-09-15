import csv, glob, os, sys, re

from YouTube import YouTube

def extraiId(link):
    if('youtu.be' in link):
        return link.split('/')[3]
    elif('shorts' in link):
        if('?' in link):
            return re.search('.*\/(.*)\?', link).group(1)
        else:
            return link.split('/')[4]
    else: #link normal youtube.com/v?=ID
        return link.split('=')[1]

def main(): #sys.argv[1] = argumento passado pela linha de comando

    #py classificador.py 3 1 = etapa 3 perfil 1

    desinformativos = []
    desinformativos_id = []

    cont = 0

    if(len(sys.argv) == 2): #classificador da etapa 1
        caminho_pesquisa = '../../resultados/etapa1/pesquisa'
        caminho_relacionados = '../../resultados/etapa1/relacionados'
    else: #sys.argv[2] é o número do perfil
        caminho_pesquisa = '../../resultados/etapa3/perfil' + str(sys.argv[2]) + '/pesquisa'
        caminho_relacionados = '../../resultados/etapa3/perfil' + str(sys.argv[2]) + '/relacionados'
        caminho_home = '../../resultados/etapa3/perfil' + str(sys.argv[2]) + '/home'

    arq_des = csv.DictReader(open('../../resultados/etapa0/etapa0online.csv', 'r', encoding = 'utf-8'))
    for row in arq_des:
        desinformativos.append(row['Link'])

    for link in desinformativos:
        if(not 'Link' in link):
            desinformativos_id.append(extraiId(link))

    for filename in glob.glob(os.path.join(caminho_pesquisa, '*.csv')):
       with open(os.path.join(os.getcwd(), filename), 'r', encoding = 'utf-8') as f:
           arq_pesq = csv.DictReader(f)
           nome_arq_class = filename.split('\\')[1]
           arq_pesq_class = csv.DictWriter(open(caminho_pesquisa + '/classificados/' + nome_arq_class, 'w', newline='', encoding='utf-8'), fieldnames = ['Link', 'id', 'Título', 'Métrica de Popularidade', 'Visualizações', 'Likes', 'Comentários', 'Classificação', 'Classificação Normalizada'])
           arq_pesq_class.writeheader()
           for row in arq_pesq:
               if(row['id'] in desinformativos_id):
                   arq_pesq_class.writerow({'Link': row['Link'], 'id': row['id'], 'Título': row['Título'], 'Métrica de Popularidade': row['Métrica de Popularidade'], 'Visualizações': row['Visualizações'], 'Likes': row['Likes'], 'Comentários': row['Comentários'], 'Classificação': '1', 'Classificação Normalizada': '1'})
                   cont += 1
               else:
                   arq_pesq_class.writerow({'Link': row['Link'], 'id': row['id'], 'Título': row['Título'], 'Métrica de Popularidade': row['Métrica de Popularidade'], 'Visualizações': row['Visualizações'], 'Likes': row['Likes'], 'Comentários': row['Comentários'], 'Classificação': row['Classificação'], 'Classificação Normalizada': '-'}) #escreve igual

    for filename in glob.glob(os.path.join(caminho_relacionados, '*.csv')):
       with open(os.path.join(os.getcwd(), filename), 'r', encoding = 'utf-8') as f:
           arq_relacionados = csv.DictReader(f)
           nome_arq_rel = filename.split('\\')[1]
           arq_rel_class = csv.DictWriter(open(caminho_relacionados + '/classificados/' + nome_arq_rel, 'w', newline='', encoding='utf-8'), fieldnames = ['Link Origem', 'Link', 'id', 'Título', 'Métrica de Popularidade', 'Visualizações', 'Likes', 'Comentários', 'Classificação', 'Classificação Normalizada'])
           arq_rel_class.writeheader()
           for row in arq_relacionados:
               if(row['id'] in desinformativos_id):
                   arq_rel_class.writerow({'Link Origem': row['Link Origem'], 'Link': row['Link'], 'id': row['id'], 'Título': row['Título'], 'Métrica de Popularidade': row['Métrica de Popularidade'], 'Visualizações': row['Visualizações'], 'Likes': row['Likes'], 'Comentários': row['Comentários'], 'Classificação': '1', 'Classificação Normalizada': '1'})
                   cont += 1
               else:
                   arq_rel_class.writerow({'Link Origem': row['Link Origem'], 'Link': row['Link'], 'id': row['id'], 'Título': row['Título'], 'Métrica de Popularidade': row['Métrica de Popularidade'], 'Visualizações': row['Visualizações'], 'Likes': row['Likes'], 'Comentários': row['Comentários'], 'Classificação': row['Classificação'], 'Classificação Normalizada': '-'}) #escreve igual

if __name__ == "__main__":
    main()
