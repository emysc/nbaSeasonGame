from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Biblioteca de raspagem de dados externa instalada com pip
class Scraping:
    def __init__(self):
        self._driver = self.__setup_driver() # atributo protegido
        self._url = "https://www.basketball-reference.com/leagues/NBA_2025.html" # atributo protegido
    # Encapsulamento de método para privar o acesso ao serviço fora da classe
    def __setup_driver(self):
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Ativa o modo "inivísvel" das janelas chrome que está sendo recolhido os dados
        options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada 
        options.add_argument("--incognito") # Navegador anonimo, para não dar erro de cache
        return webdriver.Chrome(service=service, options=options)
    # Coleta os times
    def get_teams(self):
        self._driver.get(self._url)
        teams = {"Leste": [], "Oeste": []}

        try:
            # Coletar os nomes e links dos times
            eastTeams = self._driver.find_elements(By.XPATH, '//*[@id="confs_standings_E"]/tbody/tr/th/a')
            westTeams = self._driver.find_elements(By.XPATH, '//*[@id="confs_standings_W"]/tbody/tr/th/a')

            # Salvar o nome e URL do time
            teams["Leste"] = [{"name": team.text, "url": team.get_attribute("href")} for team in eastTeams]
            teams["Oeste"] = [{"name": team.text, "url": team.get_attribute("href")} for team in westTeams]

            return teams
        except Exception as e:
            print(f"Erro ao coletar times: {e}")
            return teams
        finally:
            print("Times coletados com sucesso.")
    # Coleta os dados dos jogadores e do coach
    def get_players(self, team_url):
        self._driver.get(team_url)  
        print(f"Acessando URL do time: {team_url}")

        playerInfo = []
        try:
            # Encontra os jogadores na tabela 
            players = self._driver.find_elements(By.XPATH, '//*[@id="roster"]/tbody/tr')
            i = 1;
            for player in players:
                if i == 15:
                    break
                try:
                    name = player.find_element(By.XPATH, f'//*[@id="roster"]/tbody/tr[{i}]/td[1]/a').text  
                    position = player.find_element(By.XPATH, './td[@data-stat="pos"]').text  
                    height = player.find_element(By.XPATH, './td[@data-stat="height"]').text  
                    weight = player.find_element(By.XPATH, './td[@data-stat="weight"]').text  
                    shirtNumber = player.find_element(By.XPATH, f'//*[@id="roster"]/tbody/tr[{i}]/th').text  
                    points = player.find_element(By.XPATH, f'//*[@id="per_game_stats"]/tbody/tr[{i}]/td[28]').text
                    coach = player.find_element(By.XPATH, '//*[@id="meta"]/div[2]/p[4]/a').text
                    
                    # Atribuir os dados coletados a variaveis de um objeto array
                    playerInfo.append({
                        "name": name,
                        "position": position,
                        "height": height,
                        "weight": weight,
                        "points": points,
                        "shirtNumber" : shirtNumber,
                        "coach": coach
                    })
                    i += 1
                except Exception as e:
                    print(f"Erro ao coletar dados de um jogador: {e} ")
            return playerInfo
        except Exception as e:
            print(f"Erro ao acessar a página do time: {e}")
            return []
        
         

        

