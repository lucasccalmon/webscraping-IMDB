from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from time import sleep
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse
import re



url = 'https://www.imdb.com/search/title/?title_type=video_game&sort=user_rating,desc'


driver = webdriver.Edge()
# Abre a página principal
driver.get(url)
sleep(5)


#botar a pagina em ingles
ingles_button = driver.find_element(By.CLASS_NAME, "ipc-responsive-button")
ingles_button.click()
sleep(2)
ingles_button2 = driver.find_element(By.XPATH, "//li[@role='menuitem' and contains(., 'Idioma') and contains(., 'Português (Brasil)')]")
ingles_button2.click()
sleep(2)
ingles_button3 = driver.find_element(By.ID, "language-option-en-US")
ingles_button3.click()
sleep(5)

page_source = driver.page_source

elementos = 500
#soup = BeautifulSoup(page_source, "html.parser")
actions = ActionChains(driver)
#numero de jogos (0 cliques = 100)
cliques=elementos/50
while(cliques-1>0):
    for i in range(12):

        #scroll pra baixo
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        
        


    #clicar no botao de ver mais
    sleep(2)
    mais50_button = driver.find_element(By.CLASS_NAME, "ipc-see-more__button")
    mais50_button.click()
    sleep(2)
    cliques = cliques - 1

backtop_button = driver.find_element(By.CLASS_NAME, "ipc-scroll-to-top-button")
backtop_button.click()
sleep(3)

botoes_jogos = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

count = 0
count2= -3
data = []
for jogo in botoes_jogos:
    soup = BeautifulSoup(jogo.get_attribute("outerHTML"), "html.parser")
    try:
        sleep(3)
        info_button = jogo.find_element(By.CLASS_NAME, "ipc-icon-button.li-info-icon")
        info_button.click()
        sleep(3)
    except:
        sleep(3)
        actions = ActionChains(driver)
        for i in range(15):
            actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(1)
        info_button = jogo.find_element(By.CLASS_NAME, "ipc-icon-button.li-info-icon")
        info_button.click()
        sleep(2)
    nome = soup.find('h3').get_text(strip=True)
    ano = soup.find('span', class_='sc-e8bccfea-7').get_text(strip=True)
    nota = soup.find('span', class_='ipc-rating-star--rating').get_text(strip=True)
    votos =soup.find('span', class_='ipc-rating-star--voteCount').get_text(strip=True)
    descricao = soup.find('div', class_='ipc-html-content-inner-div').get_text(strip=True) if soup.find('div', class_='ipc-html-content-inner-div') else None

    soup_modal = BeautifulSoup(driver.page_source, 'html.parser')
    ul_element = soup_modal.find('ul', {'data-testid': 'btp_gl'})
    # Extrai os textos dos <li> dentro da <ul>
    generos = [li.get_text(strip=True) for li in ul_element.find_all('li')] if ul_element else None
    data.append([nome, ano, nota, votos, descricao, generos])
    botao_fechar = jogo.find_element(By.XPATH, "//button[@title='Close Prompt']")
    botao_fechar.click()
    sleep(2)
    count += 1
    count2 +=1
    print(count)
sleep(5)
csv_filename = f'imdb-jogos-genero.csv'

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escreva o cabeçalho
    writer.writerow(['nome', 'ano', 'nota', 'votos', 'descricao', 'generos'])
    writer.writerows(data)

sleep(5)
driver.quit()
