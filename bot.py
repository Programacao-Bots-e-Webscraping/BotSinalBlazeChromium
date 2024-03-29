from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from time import sleep
import requests

mensagens_enviadas = []
options = Options()
options.add_argument('--headless')
options.add_argument('--mute-audio')
options.add_argument('--no-sandbox')
#driver = webdriver.Chromium(service=service,options=options)
driver = webdriver.Chrome(options=options,service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
driver.get('https://blaze-7.com/pt/games/double')
sleep(5)

    


#Mensagens Padrao
analise = 'Analisando...'
win = 'Green do Double'
win_branco = '⬜ Green do branco ⬜'
loss = 'Essa não deu!\nPare e volte mais tarde'
nao_confirmacao = 'Não confirmou Entrada \nAguarde o próximo sinal'
##############################

def esperar():
    while True:
        try:
            driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
            break
        except:
            pass
    
    while True:
        try:
            driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
        except:
            break
        
def retornar_historico():
    return [i['color'] for i in requests.get('https://blaze-7.com/api/roulette_games/recent').json()][::-1]

            
def retornar_ultimo():
    return requests.get('https://blaze-7.com/api/roulette_games/current').json()['color']

def martin_gale(gale,ultimo):
    enviar_mensagem(gale)
    esperar()
    sleep(1.5)
    ultimo_ = retornar_ultimo()
    if ultimo_ != ultimo and ultimo_ != 0:
        enviar_mensagem(win)
        return True
    elif ultimo_ == 0: 
        enviar_mensagem(win_branco)
        return True
            
def enviar_mensagem(mensagem):
    bot_token = ''
    chat_id = ''
    url_blaze = '🎰 [Blaze](https://blaze-7.com/pt/games/double)'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensagem}\n{url_blaze}&parse_mode=Markdown'
    requests.get(url)


cor = ['Branco','Preto','Vermelho']
simbolo = ['⬜','⬛','🟥']


print('Bot Grupo de sinais iniciado ...')
enviar_mensagem('Bot Grupo de sinais iniciado ...')
while True:
    try:
        print('ok')
        esperar()
        sleep(1.5)
        historico = retornar_historico()
        ultimo = retornar_ultimo()
        historico.append(ultimo)
        padrao = historico[-4:]
        print(padrao)
        confirmacao = f'{simbolo[padrao[0]]} Entrada confirmada no {cor[padrao[0]]}\n{simbolo[0]} Proteção no branco'
        gale1 = f'Vamos para o gale 1 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} Proteção no Branco'
        gale2 = f'Vamos para o gale 2 \n{simbolo[padrao[0]]} {cor[padrao[0]]}\n{simbolo[0]} Proteção no Branco'

        
        
        #Como as estratégias sempre jogam na cor contraria, resolvi colocar as cores
        #Vermelha e Preta em indices diferentes para aproveirar a logica
        if padrao == [1,1,1,1] or padrao == [2,2,2,2] or padrao == [1,2,1,2] or padrao == [2,1,2,1]:                
            enviar_mensagem(analise)
            esperar()
            sleep(1.5)
            ultimo = retornar_ultimo()
            while True:
                if ultimo == padrao[0]:
                    enviar_mensagem(confirmacao)
                    esperar()
                    sleep(1.5)
                    ultimo_ = retornar_ultimo()
                    if ultimo_ != ultimo and ultimo_ != 0:
                        enviar_mensagem(win)
                        break
                    elif ultimo_ == 0:
                        enviar_mensagem(win_branco)
                        break
                    else:
                        if martin_gale(gale1,ultimo):
                            break
                        else:
                            if martin_gale(gale2,ultimo):
                                break
                            else:
                                enviar_mensagem(loss)
                                break
                                      
                else:
                    enviar_mensagem(nao_confirmacao)
                    break
    except Exception as e:
        print(e)
        driver.get('https://blaze-7.com/pt/games/double')
        sleep(10)
        pass
