import csv, glob, os

from YouTube import YouTube

caminho_pesquisa = '../../resultados/etapa1/pesquisa'
caminho_relacionados = '../../resultados/etapa1/relacionados'
caminho_desinfo = '../../resultados/etapa0'

resultados = []
desinformativos = []
desinformativos_id = []

cont = 0
totalvideos = 0

cont_embaixadores = 0
cont_bolsonaro_urnas = 0
cont_urna_eletronica = 0
cont_urnas_eletronicas = 0
cont_nova_urna = 0

bot = YouTube()

for filename in glob.glob(os.path.join(caminho_desinfo, '*.csv')):
    with open(os.path.join(os.getcwd(), filename), 'r', encoding = 'utf-8') as f:
        arq_des = csv.DictReader(f)
        for row in arq_des:
            desinformativos.append(row['Link'])

for link in desinformativos:
    if(not 'Link' in link):
        desinformativos_id.append(bot.extraiId(link))

for filename in glob.glob(os.path.join(caminho_pesquisa, '*.csv')):
   with open(os.path.join(os.getcwd(), filename), 'r', encoding = 'utf-8') as f:
       print(filename)
       arq_pesq = csv.DictReader(f)
       for row in arq_pesq:
           resultados.append(row['id'])
           totalvideos += 1
           if(row['id'] in desinformativos_id):
               cont += 1
               if('bolsonaro embaixadores urnas' in filename):
                   cont_embaixadores += 1
               if('bolsonaro urnas eletrônicas' in filename):
                   cont_bolsonaro_urnas += 1
               if('urna eletrônica_' in filename):
                   cont_urna_eletronica += 1
               if('urnas eletronicas_' in filename):
                   cont_urnas_eletronicas += 1
               if('nova urna eletronica 2022' in filename):
                   cont_nova_urna += 1


for filename in glob.glob(os.path.join(caminho_relacionados, '*.csv')):
   with open(os.path.join(os.getcwd(), filename), 'r', encoding = 'utf-8') as f:
       arq_rel = csv.DictReader(f)
       for row in arq_rel:
           resultados.append(row['id'])
           totalvideos += 1
           if(row['id'] in desinformativos_id):
               cont += 1
               if('bolsonaro embaixadores urnas' in filename):
                   cont_embaixadores += 1
               if('bolsonaro urnas eletrônicas' in filename):
                   cont_bolsonaro_urnas += 1
               if('urna eletrônica_' in filename):
                   cont_urna_eletronica += 1
               if('urnas eletronicas_' in filename):
                   cont_urnas_eletronicas += 1
               if('nova urna eletronica 2022' in filename):
                   cont_nova_urna += 1

#for video in resultados:
#    if(video in desinformativos_id):
#        cont += 1

print('Total de vídeos: ', totalvideos)
print('Total de vídeos desinformativos: ', cont)
print('bolsonaro embaixadores urnas:', cont_embaixadores)
print('bolsonaro urnas eletrônicas: ', cont_bolsonaro_urnas)
print('nova urna eletronica 2022: ', cont_nova_urna)
print('urnas eletronicas: ', cont_urnas_eletronicas)
print('urna eletrônica: ', cont_urna_eletronica)
