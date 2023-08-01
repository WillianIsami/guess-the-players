import random
import os
import json
import sys
import tkinter as tk
import sqlite3
import csv 
from tkinter import messagebox

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Advinhação")
        self.root.geometry("400x300")
        self.user_label = tk.Label(root, text="Qual o seu nome?")
        self.user_label.pack()
        self.user_entry = tk.Entry(root)
        self.user_entry.pack()
        self.db_connection = sqlite3.connect("database.db")
        self.create_table()
        self.start_button = tk.Button(root, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack()
        self.pontuation = 0
        self.counter = 0
        self.player = None
        self.player_list = []
        self.player_index = 0
        self.random_player = self.get_random_player("players_21.csv")
        # TODO: Another file to store the database settings.

    def start_game(self):
        self.user = self.user_entry.get().strip()
        if self.user:
            with self.db_connection:
                self.db_connection.execute('INSERT INTO people (name) VALUES (?)', (self.user,))
            messagebox.showinfo("Sucesso", "Usuário adicionado ao game.")
        if not self.user:
            messagebox.showerror("Erro", "Por favor, insira um nome de usuário.")
            return
        self.user_label.pack_forget()
        self.user_entry.pack_forget()
        self.start_button.pack_forget()
        self.verify_player()

    def get_random_player(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            players = list(reader)
        random_player = random.choice(players)
        return random_player

    def show_tips(self):
        print("Jogo da Advinhação")
        print("Acerte o nome do jogador através das dicas de posição, time e nacionalidade do jogador")
        print("Você tem 5 chances para acertar o jogador!")
        _, short_name, long_name, age, birth_day, height, weight, nationality, team, league_name, overall, potential, positions, preferred_foot = self.random_player
        tips = {
            "age":age,
            "birth_day":birth_day,
            "height":height,
            "weight":weight,
            "nationality":nationality,
            "team":team,
            "league_name":league_name,
            "overall":overall,
            "potential":potential,
            "positions":positions,
            "preferred_foot":preferred_foot
        }
        tip_one, tip_two = random.choice(list(tips.items()))
        return (f"{tip_one} - {tip_two}")
    
    def widget(self):
        self.guess_label = tk.Label(self.root, text="Quem é o jogador?")
        self.guess_label.pack()
        self.guess_entry = tk.Entry(root)
        self.guess_entry.pack()
        self.guess_button = tk.Button(root, text="Enviar", command=self.verify_player)
        self.guess_button.pack()

    def verify_player(self, guess_entry):
        guess = guess_entry.get().strip()
        short_name, long_name = self.random_player[1:3]
        if (guess.lower() == short_name.lower()) or (guess.lower() == long_name.lower()):
            messagebox.showinfo("Parabéns", "Você acertou o jogador!")
            self.pontuation += 5
            self.counter += 1
            self.player_label.pack_forget()
            self.guess_entry.pack_forget()
            self.guess_button.pack_forget()
            return
        else:
            if self.pontuation:
                messagebox.showinfo("Fim de Jogo", f"O jogador era {short_name}. Acabou as suas tentativas. {self.user}, você ficou com {self.pontuation} pontos.")
                self.verify_player.pack_forget()
                sys.exit()
            messagebox.showinfo("Resposta Errada", "Você errou! Quer receber +1 dica? (-1 ponto).")
            tk.Button(self.root, text="Receber +1 dica", command=self.show_tips)
            self.pontuation -= 1
            self.verify_player()
    
    def create_table(self):
        with self.db_connection:
            self.db_connection.execute('''
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )
            ''')

if __name__ == "__main__":
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()