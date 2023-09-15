#Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

#Outros
import re
import os
import time, datetime
import random
import geckodriver_autoinstaller

class YouTube:

    def __init__(self):

        self.bot = webdriver.Firefox()

    def visitaLink(self, link):
        self.bot.get(link)
        time.sleep(5)

    def instalaAdBlock(self):

        self.bot.install_addon((os.getcwd() + r'\adblock_for_firefox-5.0.5.xpi'), temporary=True)
        time.sleep(30)
        self.bot.switch_to.window(window_name = self.bot.window_handles[1])
        self.bot.close()
        self.bot.switch_to.window(window_name = self.bot.window_handles[0])
        print('Navegador iniciado e Adblock instalado! Prosseguindo...')

    def fazLogin(self, usuario, senha):

        self.bot.get('https://accounts.google.com/')

        time.sleep(3)

        self.bot.find_element('xpath', '//input[@type="email"]').send_keys(usuario)
        self.bot.find_element('xpath', '//input[@type="email"]').send_keys(Keys.ENTER)

        time.sleep(3)

        self.bot.find_element('xpath', '//input[@type="password"]').send_keys(senha)
        self.bot.find_element('xpath', '//input[@type="password"]').send_keys(Keys.ENTER)

        #tempo maior para caso peça confirmação de identidade
        time.sleep(200)

    def pesquisa(self, termo, filtro): #retorna os 20 primeiros resultados de pesquisa

        links = []

        termo = termo.replace(' ', '+')
        link_pesquisa = 'https://www.youtube.com/results?search_query=' + termo

        #aplica filtros (se for relevância, não precisa aplicar filtro)

        if(filtro == 'relevância'):
            self.bot.get(link_pesquisa)
        if(filtro == 'data'):
            link_data = link_pesquisa + '&sp=CAI'
            print('link data: ', link_data)
            self.bot.get(link_data)
        if(filtro == 'contagem'):
            link_contagem = link_pesquisa + '&sp=CAM'
            print('link contagem: ', link_contagem)
            self.bot.get(link_contagem)
        if(filtro == 'classificação'):
            link_classificacao = link_pesquisa + '&sp=CAE'
            print('link classificação: ', link_classificacao)
            self.bot.get(link_classificacao)

        time.sleep(10)

        self.bot.execute_script("window.scrollByPages(3)") #tem que rolar p/ pegar o número de comentários

        time.sleep(3)

        #se quiser pegar o título do vídeo junto:
        #titulos = self.bot.find_elements_by_xpath('//*[@id="video-title"]')

        #for titulo in titulos:
        #    print(titulo.get_attribute('href'))
        #    print(titulo.text)

        videos = self.bot.find_elements_by_xpath('//*[@id="thumbnail"]')

        for video in videos:
            link = video.get_attribute('href')
            if(link != None):
                if(not 'googleadservices' in link):
                    links.append(link)

        while(len(links) > 20): #reduz para os primeiros 20 resultados
            links.pop()

        #print(len(links))
        print('links: ', links)

        return links

    def extraiLinkRecomendados(self, pagina): #extrai os links dos 10 primeiros recomendados (pagina = 'home' || 'video')

        if(pagina == 'home'):
            self.bot.get('https://www.youtube.com/')
            time.sleep(3)

        recomendados = self.bot.find_elements_by_xpath('//*[@id="thumbnail"]')

        if(pagina == 'video'):
            recomendados.remove(recomendados[0]) #primeiro da lista é o próprio vídeo

        links = []

        for video in recomendados:
            link = video.get_attribute('href')
            if(link != None):
                if(pagina == 'home'): #não adiciona shorts aos recomendados da página inicial
                    if(not ('shorts' in link)):
                        links.append(link)
                else:
                    links.append(link)

        while(len(links) > 10): #remove as últimas 10 recomendações, para que fiquem apenas as 10 primeiras
            links.pop()

        return links

    def extraiTitulo(self): #alterado p/etapa 3

        #if('shorts' in self.bot.current_url):
            #titulo = self.bot.find_element_by_xpath('//*[@id="overlay"]').text
        titulo = self.bot.title.replace(' - YouTube', '')
        #else:
            #titulo = self.bot.find_element_by_css_selector('h1.title:nth-child(4)').text

        if(';' in titulo): #tem que substituir ; por - senão troca de célula no .csv
            titulo.replace(';', '-')

        return titulo

    def tempo_video(self): #extrai o tempo do vídeo em segundos

        tempo_video = self.bot.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0].text

        if(tempo_video.count(':') == 2): #vídeo com hora, minuto e segundo (vídeo com mais de uma hora)
            x = time.strptime(tempo_video, '%H:%M:%S')
            tempo_video_segundos = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
        else: #vídeo com minutos e segundos -- vídeos apenas com segundos respeitam a estrutura também (00:ss)
            x = time.strptime(tempo_video, '%M:%S')
            tempo_video_segundos = datetime.timedelta(minutes=x.tm_min, seconds=x.tm_sec).total_seconds()

        return tempo_video_segundos

    def assisteVideo(self, lista, etapa): #função p/ assistir vídeo da etapa 2 e 3 se etapa = 2 vídeo tem q ter menos de 30 min, se etapa 3, assiste video independente de tamanho

        tempo_video_segundos = self.tempo_video()

        if(etapa == 2):
            while(tempo_video_segundos > 1800): #seleciona outro da lista para assistir caso o vídeo tenha mais de 30 minutos
                #print('Vídeo com mais de 30 minutos! Selecionando outro...')
                video_novo = random.choice(lista)[0]
                while(self.verificaVideoRemovido(video_novo, 0) != 0): #caso o vídeo tenha sido removido no tempo entre a etapa0 e a etapa2
                    video_novo = random.choice(lista)[0]
                time.sleep(10)
                tempo_video_segundos = self.tempo_video()

        player = self.bot.find_element_by_id('movie_player')
        player.send_keys(Keys.SPACE) #dá play no vídeo

        time.sleep(2)

        self.aceleraVideo()

        tempo_assistir = int((tempo_video_segundos * 0.6)/2) #divide por 2 porque o vídeo foi acelerado 2x. p/ criação dos históricos foi assistido 60% dos vídeos, p/ etapa 2 foram 80% (e só videos com menos de 30 minutos)

        time.sleep(tempo_assistir) #espera 80% do tempo do vídeo

    def aceleraVideo(self): #acelera o vídeo para 2x

        js = 'document.getElementsByClassName("video-stream html5-main-video")[0].playbackRate = 2.0;'

        self.bot.execute_script(js)

    def extraiId(self, link): #iterar, talvez ainda não esteja 100% (usar regex em todos?)
        if('youtu.be' in link):
            return link.split('/')[3]
        elif('shorts' in link):
            if('?' in link):
                return re.search('.*\/(.*)\?', link).group(1)
            else:
                return link.split('/')[4]
        else: #link normal youtube.com/v?=ID
            return link.split('=')[1]

    def verificaVideoRemovido(self, link, etapa): #etapa 0 tem que visitar o link, demais etapas só verifica já na página

        #0 = online, 1 = viola diretrizes, 2 = vídeo não está mais disponível,
        #3 = gravação ao vivo não está mais disponível, 4 = vídeo privado,
        #5 = vídeo indisponível #6 = vídeo de canal com conteúdo inadequado (login necessário)
        #7 = vídeo da jovem pan tornado privado após pressão comercial (pós-eleições - etapa 3)

        if(etapa == 0):
            #self.bot.get(link)
            self.bot.execute_script(f'location.href="{link}";')
            element_present = EC.presence_of_element_located((By.ID, 'logo-icon'))
            WebDriverWait(self.bot, 99999999).until(element_present)
            time.sleep(3)

        try:
            self.bot.find_element('xpath', '//*[text() = "Este vídeo foi removido por violar as diretrizes da comunidade do YouTube"]')
            return 1
        except NoSuchElementException:
            try:
                self.bot.find_element('xpath', '//*[text() = "Este vídeo não está mais disponível"]')
                return 2
            except NoSuchElementException:
                try:
                    self.bot.find_element('xpath', '//*[text() = "A gravação dessa transmissão ao vivo não está disponível."]')
                    return 3
                except NoSuchElementException:
                    try:
                        self.bot.find_element('xpath', '//*[text() = "Vídeo privado"]')
                        return 4
                    except NoSuchElementException:
                        try:
                            self.bot.find_element('xpath', '//*[text() = "Vídeo indisponível"]')
                            return 5
                        except NoSuchElementException:
                            try:
                                self.bot.find_element('xpath', '//*[text() = "Faça login para ver este canal"]')
                                return 6
                            except NoSuchElementException:
                                return 0

    def metricaPopularidade(self): #alterado p/ etapa 3

        likes = ''
        comentarios = ''
        visualizacoes = ''

        time.sleep(3)

        if('shorts' in self.bot.current_url): #vídeo é shorts, contagem de likes/comentários e views é diferente

            try:
                string_likes = self.bot.find_element('xpath', '//*[contains(@aria-label, "Marque este vídeo")]').text
                string_likes = re.findall(r'\d+', string_likes) #pega só os digitos, sem pontos e caracteres
                if(string_likes == []): #não consegue pegar os likes (shorts com poucos likes ou sem)
                    string_likes = '0'
            except NoSuchElementException:
                string_likes = '0'

            try:
                string_comentarios = self.bot.find_element('xpath', '//*[contains(@aria-label, "comentários")]').get_attribute('aria-label')
                string_comentarios = re.findall(r'\d+', string_comentarios)
                if(string_comentarios == []):
                    string_comentarios = '0'
            except NoSuchElementException:
                string_comentarios = '0'

            self.bot.find_element('xpath', '//*[@aria-label="Mais ações"]').click()
            self.bot.find_element('xpath', '//*[text() = "Descrição"]').click()
            string_visualizacoes = self.bot.find_element('xpath', '//*[@id="view-count"]').text
            string_visualizacoes = re.findall(r'\d+', string_visualizacoes)

        else: #vídeo normal

            self.bot.execute_script("window.scrollByPages(1)") #tem que rolar p/ pegar o número de comentários

            time.sleep(2)

            try:
                string_likes = self.bot.find_element('xpath', '//*[contains(@aria-label, "Marque este vídeo")]').get_attribute('aria-label')
                string_likes = re.findall(r'\d+', string_likes) #pega só os digitos, sem pontos e caracteres
                if(string_likes == []):
                    string_likes = '0'
            except NoSuchElementException:
                string_likes = '0'

            try:
                string_comentarios = self.bot.find_element('xpath', '//h2[@id="count"]').text
                string_comentarios = re.findall(r'\d+', string_comentarios)
                if(string_comentarios == []):
                    string_comentarios = '0'
            except NoSuchElementException:
                string_comentarios = '0'

            string_visualizacoes = self.bot.find_element('xpath', '//span[@class="view-count style-scope ytd-video-view-count-renderer"]').text
            if(string_visualizacoes == None):
                try:
                    self.bot.find_element('xpath', '//div[@id="description"]').click()
                    time.sleep(2)
                    string_visualizacoes = self.bot.find_element('xpath', '//span[@class="style-scope yt-formatted-string bold"]').text
                    print('string_visualizações (text): ', string_visualizacoes)
                except NoSuchElementException:
                    if(string_visualizacoes == ''):
                        print('entrou nosuchelement e string vazia')
                        string_visualizacoes = self.bot.find_element('xpath', '//span[@class="style-scope yt-formatted-string bold"]').text

            string_visualizacoes = re.findall(r'\d+', string_visualizacoes)
            print('string visualizacoes (pós findall): ', string_visualizacoes)

        for string in string_likes:
            likes = likes + string

        for string in string_comentarios:
            comentarios = comentarios + string

        for string in string_visualizacoes:
            visualizacoes = visualizacoes + string

        print('likes: ', likes)
        print('comentarios: ', comentarios)
        print('visualizações: ', visualizacoes)

        return [(int(likes) + int(comentarios) + int(visualizacoes)), visualizacoes, likes, comentarios]

    def fechaNavegador(self):
        self.bot.close()

    def limpaHistorico(self):

        self.bot.get('https://www.youtube.com/feed/history')
        time.sleep(3)

        self.bot.find_element('xpath', '//*[text() = "Limpar todo o histórico de exibição"]').click()

        time.sleep(2)

        self.bot.find_element('xpath', '//*[contains(@aria-label, "LIMPAR HISTÓRICO DE EXIBIÇÃO")]').click()

        time.sleep(2)

    def pausaHistorico(self):
        self.bot.get('https://www.youtube.com/feed/history')
        time.sleep(3)

        self.bot.find_element('xpath', '//*[text() = "Pausar o histórico de visualizações"]').click()

        time.sleep(2)

        self.bot.find_element('xpath', '//*[contains(@aria-label, "PAUSAR")]').click()

        time.sleep(2)

    def ativaHistorico(self):
        self.bot.get('https://www.youtube.com/feed/history')
        time.sleep(3)

        self.bot.find_element('xpath', '//*[text() = "Ativar o histórico de exibição"]').click()

        time.sleep(2)

        self.bot.find_element('xpath', '//*[contains(@aria-label, "ATIVAR")]').click()

        time.sleep(2)

    def constroiHistorico(self, lista):

        for video in lista:
            self.visitaLink(video)
            self.assisteVideo([], 3)

#    def extraiTituloRecomendados(self): NÃO UTILIZADO

#        recomendados = self.bot.find_elements_by_xpath('//*[@id="video-title"]')

#        titulos = []

#        for video in recomendados:
#            titulos.append(video.text)

#        while(len(titulos) > 10):
#            titulos.pop()

#        return titulos
