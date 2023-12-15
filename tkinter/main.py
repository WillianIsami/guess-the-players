import random
import tkinter as tk
import sqlite3
import csv 
import time 
import ttkbootstrap as ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from ttkbootstrap.constants import *

class GameGUI:
    def __init__(self, root):
        self.db_connection = sqlite3.connect("./tkinter/database.db")
        self.cursor = self.db_connection.cursor()
        self.create_table()
        self.root = root
        self.root.geometry("600x800")
        self.show_background_img()
        self.user_label = ttk.Label(self.root, text="Qual o seu nome?", font=("Helvetica", 12, "bold"), style="Bold.TLabel dark.Inverse.TLabel", justify="center")
        self.user_label.pack()
        self.user_entry = ttk.Entry(root, bootstyle="default")
        self.user_entry.pack()
        self.start_button = ttk.Button(root, text="Iniciar Jogo", command=self.start_game, bootstyle=(PRIMARY, OUTLINE))
        self.start_button.pack()
        self.pontuation = 0
        self.counter = 0
        self.flag = 0
        self.tip_keys = []
        self.show_tips(new_player=True)

    def on_resize(self, event):
        self.image = self.bgimg.copy()
        self.image.thumbnail((event.width, event.height), Image.ANTIALIAS)
        self.l.image = ImageTk.PhotoImage(self.image)
        self.l.config(image=self.l.image)
    
    def show_background_img(self):
        self.bgimg = Image.open('./tkinter/img/background.png')
        self.something = Image.open('./tkinter/img/correct.png')
        self.l = tk.Label(root)
        self.l.place(x=0, y=0, relwidth=1, relheight=1)
        self.l.bind('<Configure>', self.on_resize)

    def fullscreen_option(self):
        # TODO: Fullscreen option
        self.root.attributes('-fullscreen', True)

    def start_game(self):
        self.user = self.user_entry.get().strip()
        if self.user:
            with self.db_connection:
                self.db_connection.execute('INSERT INTO people (name, points) VALUES (?, ?)', (self.user, self.pontuation))
            messagebox.showinfo("Sucesso", "Usuário adicionado ao game.")
        if not self.user:
            messagebox.showerror("Erro", "Por favor, insira um nome de usuário.")
            return
        self.user_label.pack_forget()
        self.user_entry.pack_forget()
        self.start_button.pack_forget()
        self.create_widgets()

    def insert_total_points_db(self, game_over_text):
        # try: 
            print("self - pontuation - ",self.pontuation, self.user)
            query = f"UPDATE people SET points = {self.pontuation} WHERE name = {self.user}"
            self.cursor.execute(query)
            self.db_connection.commit()
            self.db_connection.close()
            ttk.Label(self.root, text=game_over_text).pack()
        # except:
        #     print("erro db")
        #     ttk.Label(self.root, text=f"Ops, algo deu errado! Não foi possível registrar a sua pontuação de: {self.pontuation} pontos").pack()

    def show_tips(self, new_player=False, show_tip=False):
        if new_player:
            with open("./tkinter/players_21.csv", newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                players = list(reader)
            self.random_player = random.choice(players)
            print("random player", self.random_player)
        _, short_name, long_name, age, birth_day, height, weight, nationality, team, league_name, overall, potential, positions, preferred_foot = self.random_player
        tips = {
            "age:":age,
            "birth_day:":birth_day,
            "height (cm):":height,
            "weight (kg):":weight,
            "nationality:":nationality,
            "team:":team,
            "league_name:":league_name,
            "overall:":overall,
            "potential:":potential,
            "positions:":positions,
            "preferred_foot:":preferred_foot
        }
        print("tip keys:", self.tip_keys)
        if len(self.tip_keys):
            for delete in self.tip_keys:
                del tips[delete]
        if not len(tips):
            self.flag += 1
            if self.flag == 1: 
                tip_label = tk.Label(self.root, text=f"Tips over")
                tip_label.pack()
                self.wrong_answer_tip.config(state=tk.DISABLED)
                self.verify_guess(True)
        if show_tip and len(tips):
            tip_key, tip_value = random.choice(list(tips.items()))
            self.tip_keys.append(tip_key)
            self.pontuation -= 1
            tip_label = tk.Label(self.root, text=f"{tip_key} - {tip_value}")
            tip_label.pack()
        return short_name, long_name

    def create_widgets(self):
        self.guess_label = tk.Label(self.root, text="Quem é o jogador?")
        self.guess_label.pack()
        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack()
        self.guess_button = tk.Button(self.root, text="Enviar", command=self.verify_guess)
        self.guess_button.pack()
    
    def verify_guess(self, tips_over = False):
        guess = self.guess_entry.get()
        short_name, long_name = "game", "over"
        if not tips_over: 
            short_name, long_name = self.show_tips()
        print(f"{guess.lower()} - {short_name.lower()} - {long_name.lower()}\n")
        if (guess.lower() == short_name.lower()) or (guess.lower() == long_name.lower()):
            messagebox.showinfo("Parabéns", "Você acertou o jogador!")
            self.pontuation += 10
            self.counter += 1
            self.guess_label.pack_forget()
            self.guess_button.pack_forget()
            self.wrong_answer_label.pack_forget()
            self.wrong_answer_tip.pack_forget()
            self.insert_total_points_db(f"Sua pontuação final: {self.pontuation} pontos")
            time.sleep(3)
            self.root.after(1000, self.root.destroy())
        else:
            self.counter += 1
            if self.counter > 5:
                self.insert_total_points_db(f"O jogador era {short_name}. Acabou as suas tentativas. {self.user}, você ficou com {self.pontuation} pontos.")
                time.sleep(3)
                self.wrong_answer_label.pack_forget()
                self.wrong_answer_tip.pack_forget()
                self.root.after(1000, self.root.destroy())
            if not tips_over and self.counter == 1:
                self.pontuation -= 1
                self.wrong_answer_label = tk.Label(self.root, text="Você errou! Quer receber +1 dica? (-1 ponto).")
                self.wrong_answer_label.pack()
                self.wrong_answer_tip = tk.Button(self.root, text="Receber +1 dica", command=lambda: self.show_tips
                (False, True))
                self.wrong_answer_tip.pack()

    def create_table(self):
        with self.db_connection:
            self.db_connection.execute('''
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    points TEXT
                )
            ''')

if __name__ == "__main__":
    root = ttk.Window(title="Jogo da Advinhação")
    game = GameGUI(root)
    root.mainloop()