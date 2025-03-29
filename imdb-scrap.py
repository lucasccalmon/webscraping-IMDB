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

actions = ActionChains(driver)
#numero de jogos (0 cliques = 100)
cliques=8
while(cliques>=0):
    n=0
    while(n<12):
        #scroll pra baixo
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        sleep(1)
        n= n+1


    #clicar no botao de ver mais
    mais50_button = driver.find_element(By.CLASS_NAME, "ipc-see-more__button")
    mais50_button.click()
    sleep(5)
    cliques = cliques - 1


page_source = driver.page_source


soup = BeautifulSoup(page_source, "html.parser")

table_div = soup.find("ul", class_="ipc-metadata-list")
table_div.get_text()
tds_rechts = soup.find_all('li', class_='ipc-metadata-list-summary-item')
sleep(5)
data = []
for td in tds_rechts:
    nome = td.find('h3').get_text(strip=True)
    ano = td.find('span', class_='sc-e8bccfea-7').get_text(strip=True)
    nota = td.find('span', class_='ipc-rating-star--rating').get_text(strip=True)
    votos =td.find('span', class_='ipc-rating-star--voteCount').get_text(strip=True)
    descricao = td.find('div', class_='ipc-html-content-inner-div').get_text(strip=True) if td.find('div', class_='ipc-html-content-inner-div') else None

    data.append([nome, ano, nota, votos, descricao])

sleep(5)

csv_filename = f'imdb-jogos.csv'

with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Escreva o cabeçalho
    writer.writerow(['nome', 'ano', 'nota', 'votos', 'descricao'])
    writer.writerows(data)

sleep(5)
driver.quit()
