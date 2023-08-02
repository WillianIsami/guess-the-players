import random 
import os
import json
import sys

class Game():
    def __init__(self):
        self.user = input("Qual o seu nome? ")
        self.pontuation = 0
        print("Jogo da advinhação\nAcerte o nome do jogador através das dicas de posição, time e nacionalidade do jogador\n")
        print("Você tem 5 chances para acertar os 5 jogadores e ficar no pódio!")
        self.xyz = []
        self.counter = 0
        self.parameter = 0
        self.pontuation = 0
        self.winner = 0

    def verify_player(self, path):
        with open(path, encoding='utf-8') as fl:
            read = fl.readlines()
        if self.counter >= 3:
            self.write_podium()
            self.order_json()
            sys.exit() 
        rand = random.randint(0,29)
        player = read[rand].split(':')
        self.player = player[0]
        n = 5
        x = 1
        for i in range(0,5):
            name = input(f"Qual o nome e sobrenome do jogador de futebol? Você tem {n} tentativas\n").upper()
            if n == 0:
                print("n == 1")
                self.write_podium()
                self.order_json()
                sys.exit() 
            if self.player == name:
                print("Parabéns você acertou o jogador!")
                self.pontuation += 5
                print(f"Sua pontuação atual: {self.pontuation}")
                self.counter += 1
                if self.counter < 3:
                    print("\nTente acertar um outro jogador agora:")
                self.winner += 1
                if self.winner == 3:
                    print(f"Parabéns! Você acertou os 3 jogadores de futebol")
                    self.write_podium()
                    self.order_json()
                    sys.exit()
                self.verify_player("dataset_players.txt")
            elif self.player != name:
                if n == 1:
                    print("Acabou as suas tentativas.")
                    self.write_podium()
                    self.order_json()
                    sys.exit()
                print("\nVocê errou! Quer receber +1 dica? (-1 ponto).")
                try:
                    dics = int(input("1. Sim\nDigite qualquer coisa para 'não'\n"))
                    if dics == 1:
                        if x <= 3:
                            print(f"Dica do jogador: {player[x]}")
                            x+=1
                            self.pontuation -= 1
                        else:
                            print("Acabou as dicas")
                    if dics != 1:
                        print()
                except:
                    print()
            n -= 1
    
    def write_users(self):
        data = {
            
        }
        with open("users.json", "w") as file:
            json.dump(data, file)

    def write_podium(self):
        print(f"{self.user} você ficou com {self.pontuation} pontos.")
        podium = {
            f"{self.user}": self.pontuation
        }
        with open("users.json", 'r') as fl:
            content = json.load(fl)
        content.update(podium)
        content_json = json.dumps(content, indent=4, separators=(', ', ': '))
        with open("users.json", "w") as file:
            file.write(content_json)

    def order_json(self):
        with open("users.json", 'r') as fl:
            cont = json.load(fl)
        sorted_data = sorted(cont.items(), key=lambda x: x[1], reverse=True)
        order_json = {}
        for key, value in sorted_data:
            order_json[key] = value
        ordered_json = json.dumps(order_json, indent=4)
        with open("users.json", 'w', encoding='utf-8') as fl:
            fl.write(ordered_json)

if __name__ == "__main__":
    path = "dataset_players.txt"
    game = Game()
    if not os.path.exists("users.json"):
        game.write_users()
    game.verify_player(path)