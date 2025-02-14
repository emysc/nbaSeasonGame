import tkinter as tk
import time
import ttkbootstrap as ttk# Biblioteca TTKbootstrap para efeitos visuais
from ttkbootstrap.constants import *# Biblioteca TTKbootstrap para efeitos visuais
from Load import populate
from Entity.Team import Team
from Entity.Player import Player
from Entity.Coach import Coach
import threading # nova biblioteca dos modulos do Python
import json # nova biblioteca dos modulos do Python
import os # nova biblioteca dos modulos do Python
from PIL import Image, ImageTk # Nova biblioteca externa (download  com pip) de inserção de imagens 

# Configuração da Janela Principal
# Biblioteca TTKbootstrap para efeitos visuais
root = ttk.Window(themename="superhero")
root.geometry("1000x650")
root.title("NBA Simulator Season 2024-25")

jsonFilePath = "data.json"
savedData = {}

# Criar um frame para a tela de carregamento
loadingFrame = ttk.Frame(root)
loadingFrame.place(relx=0.5, rely=0.5, anchor="center")

label = ttk.Label(loadingFrame, text="Carregando dados...", font=("Arial", 14))
label.pack(pady=10)

progress = ttk.Progressbar(loadingFrame, mode="indeterminate", length=200, bootstyle="info-striped")
progress.pack(pady=10)
progress.start(10)

# Inicialização das variaveis do optionMenu da conferencia
conferences = []
conferenceOptions = []
selectedConference = None 
conferenceOptionMenu = None 

# Time 1
team1Options = [Team("", "", "")]
selectedTeam1 = tk.StringVar(value="Selecione um time:")
team1OptionMenu = tk.OptionMenu(root, selectedTeam1, *team1Options)
team1OptionMenu.config(width=40)

# Time 2
team2Options = [Team("", "", "")]
selectedTeam2 = tk.StringVar(value="Selecione um time:")
team2OptionMenu = tk.OptionMenu(root, selectedTeam2, *team2Options)
team2OptionMenu.config(width=40)

# Configuração estética da interface gráfica dos times 1 e 2
team1ResultLabel = tk.Label(root, text="")
team2ResultLabel = tk.Label(root, text="")
nameTeam1ResultLabel = ttk.Label(root, text="")
nameTeam2ResultLabel = ttk.Label(root, text="")

# Configuração estética da tabela de jogadores e coach dos times 1 e 2
treePlayersTeam1 = ttk.Treeview(root, columns=("Shirt", "Name", "Position", "Height", "Points"), show="headings", height=6)
treePlayersTeam2 = ttk.Treeview(root, columns=("Shirt", "Name", "Position", "Height", "Points"), show="headings", height=6)
for tree in [treePlayersTeam1, treePlayersTeam2]:
    tree.heading("Shirt", text="Nº Camiseta")
    tree.heading("Name", text="Nome")
    tree.heading("Position", text="Posição")
    tree.heading("Height", text="Altura")
    tree.heading("Points", text="Pontos")
    tree.column("Shirt", width=90, anchor="center")
    tree.column("Name", width=110, anchor="center")
    tree.column("Position", width=60, anchor="center")
    tree.column("Height", width=80, anchor="center")
    tree.column("Points", width=80, anchor="center")
    
def closeLoadWindow():
    # Esconde a tela de carregamento
    loadingFrame.place_forget()
    # Após populado as conferencias, chamo a função para popular o option menu e o main
    optionMenuConference()  
    main()  

def loadData():
    global conferences, conferenceOptions, teamsConference, savedData

    if os.path.exists(jsonFilePath):
        with open(jsonFilePath, "r", encoding="utf-8") as arquivo:
            savedData = json.load(arquivo)
            
            conferences = []
            for conf in savedData["conferences"]:
                
                # Verifica se a chave 'conference' existe 
                conference = conf.get("conference", "Desconhecida")  
                
                # Cria o objeto Team 
                coach = Coach(**conf["coach"]) if "coach" in conf else None
                team = Team(conf["name"], conference, coach)
                
                # Adiciona jogadores se existirem
                team.players = [Player(**player) for player in conf.get("players", [])]
                
                conferences.append(team)

            conferenceOptions = savedData.get("conferenceOptions", [])
            teamsConference = {conf.name: conf.players for conf in conferences}

    else:
        # Popula as equipes caso o arquivo JSON não exista
        conferences = populate.createTeams()
        conferenceOptions = populate.getAllConferences()

        # Prepara os dados para serem salvos no arquivo
        data_to_save = {
            "conferences": [conf.to_dict() for conf in conferences],
            "conferenceOptions": conferenceOptions,
        }

        # Salva os dados no arquivo JSON
        with open(jsonFilePath, "w", encoding="utf-8") as arquivo:
            json.dump(data_to_save, arquivo, ensure_ascii=False, indent=4)

        # Le os dados no JSON
        with open(jsonFilePath, "r", encoding="utf-8") as arquivo:
            savedData = json.load(arquivo)

        # Organiza os dados do JSON
        conferences = []
        for conf in savedData["conferences"]:
            conference = conf.get("conference", "Desconhecida")
            coach = Coach(**conf["coach"]) if "coach" in conf else None
            team = Team(conf["name"], conference, coach)
            team.players = [Player(**player) for player in conf.get("players", [])]
            conferences.append(team)

        # Atualiza as opções de conferência e times
        conferenceOptions = savedData.get("conferenceOptions", [])
        teamsConference = {conf.name: conf.players for conf in conferences}

    # Fecha a janela de carregamento e 
    root.after(0, closeLoadWindow)

def initLoad():
    # Executa a função em paralelo com o tkinter utilizando threads, para carregar os dados e executar a janela ao mesmo tempo
    threading.Thread(target=loadData, daemon=True).start()

def optionMenuConference():
    global selectedConference, conferenceOptionMenu
    
    selectedConference = ttk.StringVar(value="Selecione uma conferência")
    
    conferenceOptionMenu = tk.OptionMenu(root, selectedConference, *conferenceOptions)
    conferenceOptionMenu.config(width=40)
    conferenceOptionMenu.grid(row=0, column=1, pady=10)

def main():
    root.title("NBA Simulator Season 2024-25")
    # Linha horizontal, para fins estéticos
    for i in range(55):  
        separator = ttk.Separator(root, bootstyle="info")
        separator.grid(row=6, column=i, sticky="ew")
        
    Progressbar = ttk.Progressbar(bootstyle="success")
    Progressbar.grid(row=6, column=i, sticky="ew")
     
    # Conferência OptionMenu
    conferenceLabel = tk.Label(root, text="Conferência:")
    conferenceLabel.grid(row=0, column=0, padx=5)
    selectedConference.trace("w", selectedConferenceChanged)
    conferenceOptionMenu.grid(row=0, column=1, pady=10)
    
    # Time 1 OptionMenu
    team1Label = tk.Label(root, text="Time 1:")
    team1Label.grid(row=1, column=0, padx=5)
    selectedTeam1.trace("w", onTeam1Select)
    team1OptionMenu.grid(row=1, column=1, pady=10)
    team1OptionMenu.config(state="disabled")  
    
    # Time 2 OptionMenu
    team2Label = tk.Label(root, text="Time 2:")
    team2Label.grid(row=2, column=0, padx=10)
    team2OptionMenu.grid(row=2, column=1, pady=10)
    team2OptionMenu.config(state="disabled")   
    
    # Botão de play
    btnPlay = ttk.Button(root, text="Jogar", command=play, bootstyle="success") 
    btnPlay.grid(row=3, column=1, padx=5, pady=10)

    # Resultado
    nameTeam1ResultLabel.grid(row=7, column=1, pady=10)
    nameTeam2ResultLabel.grid(row=7, column=3, pady=10)
    team1ResultLabel.grid(row=8, column=1)
    team2ResultLabel.grid(row=8, column=3)
    treePlayersTeam1.grid(row=9, column=1)
    treePlayersTeam2.grid(row=9, column=3)
    
    # Imagem logo NBA
    image_path = "images/NBAlogo.png" 
    image = Image.open(image_path) 
    image = image.resize((200, 100))  
    photo = ImageTk.PhotoImage(image)
    logo = ttk.Label(root, image=photo)
    logo.grid(row=1, column=3)
    logo.image = photo
    
    
def selectedConferenceChanged(*args):
    conference_name = selectedConference.get()
    
    # Filtra as conferências pelo nome
    team1NewOptions = next((conf["teams"] for conf in savedData["conferences"] if conf["name"] == conference_name), [])
    
    if not team1NewOptions:
        print(f"Erro: Nenhum time encontrado para a conferência {conference_name}")
        return

    # Remove todas as opções do menu atual
    team1OptionMenu["menu"].delete(0, "end")        

    # Adiciona as novas opções ao menu
    for option in team1NewOptions:
        team1OptionMenu["menu"].add_command(label=option["name"], command=lambda value=option: selectedTeam1.set(value["name"]))

    resetValue(team1NewOptions)
   
def resetValue(team1NewOptions):
    global team1Options 
    team1Options = team1NewOptions
    global team2Options 
    team2Options = [Team("team2", "", "")]
    selectedTeam1.set("Selecione um time:")
    selectedTeam2.set("Selecione um time:")
    team1OptionMenu.config(state="normal")  
    team2OptionMenu.config(state="disabled") 

def onTeam1Select(*args):
    if "Selecione um time:" != selectedTeam1.get():   
        team2NewOptions = [team for team in team1Options if team["name"] != selectedTeam1.get()]

        team2OptionMenu["menu"].delete(0, "end")
        
        for option in team2NewOptions:
            team2OptionMenu["menu"].add_command(label=option["name"], command=lambda value=option: selectedTeam2.set(value["name"]))

        global team2Options 
        team2Options = team2NewOptions
        selectedTeam2.set("Selecione um time:")
        team2OptionMenu.config(state="normal") 

def play():
    if "Selecione um time:" != selectedTeam1.get() and "Selecione um time:" != selectedTeam2.get():
        # team1 = next(team for team in team1Options if team.name == selectedTeam1.get())
        team1 = next(team for team in team1Options if team["name"] == selectedTeam1.get())

        # team2 = next(team for team in team2Options if team.name == selectedTeam2.get())
        team2 = next(team for team in team2Options if team["name"] == selectedTeam2.get())

        
        totalPointsTeam1 = 0
        totalPointsTeam2 = 0
        
        # Limpa as tabelas anteriores
        treePlayersTeam1.delete(*treePlayersTeam1.get_children())
        treePlayersTeam2.delete(*treePlayersTeam2.get_children())

        # Adiciona informações do coach
        # treePlayersTeam1.insert("", "end", values=("", f"Coach: {team1.coach.name}", "", "", ""))
        treePlayersTeam1.insert("", "end", values=("", f"Coach: {team1['coach']['name']}", "", "", ""))

        # treePlayersTeam2.insert("", "end", values=("", f"Coach: {team2.coach.name}", "", "", ""))
        treePlayersTeam2.insert("", "end", values=("", f"Coach: {team2['coach']['name']}", "", "", ""))


        # Adiciona os jogadores na tabela
        for i in range(5):  
            # player1 = team1.players[i]
            player1 = team1["players"][i]

            # player2 = team2.players[i]
            player2 = team2["players"][i]

            totalPointsTeam1 +=  player1["points"]
            totalPointsTeam2 += player2["points"]

            treePlayersTeam1.insert("", "end", values=(player1["shirtNumber"], player1["name"], player1["position"], f"{player1["height"]} pés", player1["points"]))
            treePlayersTeam2.insert("", "end", values=(player2["shirtNumber"], player2["name"], player2["position"], f"{player2["height"]} pés", player2["points"]))

        # Atualiza os resultados
        nameTeam1ResultLabel.config(text=selectedTeam1.get(), font=("Arial", 13), bootstyle="inverse-warning")
        nameTeam2ResultLabel.config(text=selectedTeam2.get(), font=("Arial", 13), bootstyle="inverse-info")
        team1ResultLabel.config(text=f"{totalPointsTeam1}", font=("Arial", 16))
        team2ResultLabel.config(text=f"{totalPointsTeam2}", font=("Arial", 16))
        
        # Imagem 1
        image_path = "images/Lebron.jpg"  
        image = Image.open(image_path)  
        image = image.resize((250, 150))  
        photo = ImageTk.PhotoImage(image)
        labelImage1 = ttk.Label(root, image=photo)
        labelImage1.grid(row=10, column=1, padx= 50, pady= 10)
        labelImage1.image = photo
        
        # Imagem 2
        image_path2 = "images/jimmyButler.png" 
        image2 = Image.open(image_path2) 
        image2 = image2.resize((250, 150))  
        photo2 = ImageTk.PhotoImage(image2)
        labelImage2 = ttk.Label(root, image=photo2)
        labelImage2.grid(row=10, column=3, padx= 50, pady= 10)
        labelImage2.image2 = photo2
        
if __name__ == "__main__":
    initLoad()
    root.mainloop()