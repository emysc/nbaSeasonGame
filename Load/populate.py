import sys
sys.path.append("./Entity")
from Entity.Player import Player
from Entity.Team import Team
from Entity.Conference import Conference
from Load.Scraping import Scraping
from Entity.Coach import Coach

def getAllConferences():
    return ["Oeste", "Leste"]

def createTeams():
    scraper = Scraping()
    teamsData = scraper.get_teams()  

    westConf = Conference(name="Oeste", teams=[])
    eastConf = Conference(name="Leste", teams=[])

    # Popula com os times da conferencia Oeste
    for teamData in teamsData["Oeste"]:
        team = Team(name=teamData["name"], conference="Oeste", coach = "coach")
        westConf.addTeam(team)

         # Coleta jogadores usando a url do time, acessando cada url
        playersData = scraper.get_players(teamData["url"])
        for playerInfo in playersData:
            player = Player(
                name=playerInfo['name'], 
                shirtNumber=playerInfo['shirtNumber'], 
                position=playerInfo['position'], 
                height=playerInfo['height'], 
                salary=0,  # Salário não coletado
                points = playerInfo['points']
            )
            team.addPerson(player)
            coach = Coach(name=playerInfo['coach'], height= 0, salary= 0 )
            team.addPerson(coach)
            
    # Popula com os times da conferencia Leste
    for teamData in teamsData["Leste"]:
        team = Team(name=teamData["name"], conference="Leste", coach = "coach")
        eastConf.addTeam(team)

        # Coleta jogadores usando a url do time, acessando cada url
        playersData = scraper.get_players(teamData["url"])
        for playerInfo in playersData:
            player = Player(
                name=playerInfo['name'], 
                shirtNumber=playerInfo['shirtNumber'], 
                position=playerInfo['position'], 
                height=playerInfo['height'], 
                salary=0, 
                points = playerInfo['points']
            )
            team.addPerson(player)
            coach = Coach(name=playerInfo['coach'], height= 0, salary= 0 )
            team.addPerson(coach)
    # Fecha o driver      
    scraper._driver.quit() 
    return [eastConf, westConf]
