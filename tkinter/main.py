import random
import tkinter as tk
import sqlite3
import csv 
from tkinter import messagebox

class GameGUI:
    def __init__(self, root):
        self.db_connection = sqlite3.connect("database.db")
        self.create_table()
        self.root = root
        self.root.title("Jogo da Advinhação")
        self.root.geometry("400x300")
        self.user_label = tk.Label(root, text="Qual o seu nome?")
        self.user_label.pack()
        self.user_entry = tk.Entry(root)
        self.user_entry.pack()
        self.start_button = tk.Button(root, text="Iniciar Jogo", command=self.start_game)
        self.start_button.pack()
        self.pontuation = 0
        self.counter = 0
        self.flag = 0
        self.show_tips(True)

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
        self.create_widgets()

    def show_tips(self, new_player=False, show_tip=False):
        if new_player:
            with open("players_21.csv", newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                players = list(reader)
            self.random_player = random.choice(players)
        _, short_name, long_name, age, birth_day, height, weight, nationality, team, league_name, overall, potential, positions, preferred_foot = self.random_player
        tips = {
            "age:":age,
            "birth_day:":birth_day,
            "height:":height,
            "weight:":weight,
            "nationality:":nationality,
            "team:":team,
            "league_name:":league_name,
            "overall:":overall,
            "potential:":potential,
            "positions:":positions,
            "preferred_foot:":preferred_foot
        }
        tip_one, tip_two = random.choice(list(tips.items()))
        if show_tip:
            tip_label = tk.Label(self.root, text=f"{tip_one} - {tip_two}")
            tip_label.pack()
        return short_name, long_name

    def create_widgets(self):
        self.guess_label = tk.Label(self.root, text="Quem é o jogador?")
        self.guess_label.pack()
        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()
        self.guess_button = tk.Button(self.root, text="Enviar", command=self.verify_guess)
        self.guess_button.pack()
    
    def verify_guess(self):
        guess = self.guess_entry.get()
        short_name, long_name = self.show_tips()
        print(f"{guess.lower()} - {short_name.lower()} - {long_name.lower()}\n")
        if (guess.lower() == short_name.lower()) or (guess.lower() == long_name.lower()):
            messagebox.showinfo("Parabéns", "Você acertou o jogador!")
            self.pontuation += 10
            self.counter += 1
            self.guess_label.pack_forget()
            self.guess_button.pack_forget()
            self.wrong_answer_label.pack_forget()
            self.wrong_answer_entry.pack_forget()
            self.wrong_answer_tip.pack_forget()
            messagebox.showinfo("Game Over", f"Sua pontuação final: {self.pontuation} pontos")
            self.root.after(5000, self.close_app)
        else:
            self.counter += 1
            if self.counter > 5:
                messagebox.showinfo("Fim de Jogo", f"O jogador era {short_name}. Acabou as suas tentativas. {self.user}, você ficou com {self.pontuation} pontos.")
                self.wrong_answer_label.pack_forget()
                self.wrong_answer_tip.pack_forget()
                self.root.after(5000, self.close_app)
            self.flag += 1
            if self.flag == 1:
                self.wrong_answer_label = tk.Label(self.root, text="Você errou! Quer receber +1 dica? (-1 ponto).")
                self.wrong_answer_label.pack()
                self.wrong_answer_tip = tk.Button(self.root, text="Receber +1 dica", command=lambda: self.show_tips
                (False, True))
                self.wrong_answer_tip.pack()

    def close_app(self):
        self.root.destroy()

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