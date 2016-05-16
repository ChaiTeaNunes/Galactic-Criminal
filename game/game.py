import tkinter as tk
import time

class Game(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Galactic Criminal")
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", 1)

        self.width = 400
        self.height = 600
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bd=0, highlightthickness=0)

        self.canvas.pack()

class Spaceship(object):
    def __init__(self, game):
        self.game = game
        
        self.no_tilt = tk.PhotoImage(file="sprite_0.png").subsample(4, 4)
        self.tilt_left = tk.PhotoImage(file="sprite_3.png").subsample(4, 4)
        self.tilt_right = tk.PhotoImage(file="sprite_1.png").subsample(4, 4)

        self.game.canvas.bind_all("<KeyPress-Left>", self.steer_left)
        self.game.canvas.bind_all("<KeyPress-Right>", self.steer_right)
        self.game.canvas.bind_all("<KeyRelease-Left>", self.no_steer)
        self.game.canvas.bind_all("<KeyRelease-Right>", self.no_steer)

        self.image = self.game.canvas.create_image(168, 500, image=self.no_tilt, anchor="nw")

        self.x = 0

    def steer_left(self, event):
        self.game.canvas.itemconfig(self.image, image=self.tilt_left)
        self.x = -1

    def steer_right(self, event):
        self.game.canvas.itemconfig(self.image, image=self.tilt_right)
        self.x = 1

    def no_steer(self, event):
        self.game.canvas.itemconfig(self.image, image=self.no_tilt)
        self.x = 0

    def update(self):
        if self.game.canvas.coords(self.image)[0] + self.x != 0 and self.game.canvas.coords(self.image)[0] + 64 + self.x != 400:
            self.game.canvas.move(self.image, self.x, 0)

game = Game()
spaceship = Spaceship(game)

while 1:
    game.root.update()
    spaceship.update()
    time.sleep(0.0025)
