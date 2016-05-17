import tkinter as tk
import time

# Constant Definition

RENDER = 0.0005
SPEED = 2
WIDTH = 384
HEIGHT = 576

# Class Definition

class Game(object):
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", 1)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)

        self.canvas.pack()

class Status(object):
    def __init__(self, game):
        self.game = game

        self.images = [tk.PhotoImage(file="normal.png"),
                       tk.PhotoImage(file="shooting.png"),
                       tk.PhotoImage(file="hurt.png"),
                       tk.PhotoImage(file="hurt_shooting.png")]

        self.game.canvas.bind_all("<KeyPress-space>", self.shoot)
        self.game.canvas.bind_all("<KeyRelease-space>", self.stop)

        self.bg = self.game.canvas.create_rectangle(self.images[0].width() / 2, -1, WIDTH, self.images[0].height() - 4, fill="grey")
        self.image = self.game.canvas.create_image(0, -3, image=self.images[0], anchor="nw")

    def shoot(self, event):
        self.game.canvas.itemconfig(self.image, image=self.images[1])

    def stop(self, event):
        self.game.canvas.itemconfig(self.image, image=self.images[0])

class Background(object):
    def __init__(self, game, background, speed=0):
        self.game = game
        
        self.bg = tk.PhotoImage(file=background)
        self.width = self.bg.width()
        self.height = self.bg.height()

        self.images = []
        
        for x in range(0, int(WIDTH / self.width) + 1):
            for y in range(0, int(HEIGHT / self.height) + 1):
                self.images.append(self.game.canvas.create_image(x * self.width, y * self.height, image=self.bg, anchor="nw"))
        
        self.speed = speed

    # TODO: optimize
    def update(self):
        i = 0
        for x in range(0, int(WIDTH / self.width) + 1):
            for y in range(0, int(HEIGHT / self.height) + 1):
                self.game.canvas.move(self.images[i], 0, self.speed)
                if self.game.canvas.coords(self.images[i])[1] > HEIGHT:
                    self.game.canvas.coords(self.images[i], x * self.width, 0 - self.height + self.speed)
                    
                i += 1

class Spaceship(Game):
    def __init__(self, game):
        self.game = game
        
        self.images = [tk.PhotoImage(file="ship.png"),
                       tk.PhotoImage(file="ship_l.png"),
                       tk.PhotoImage(file="ship_r.png")]

        self.game.canvas.bind_all("<KeyPress-Left>", self.steer_left)
        self.game.canvas.bind_all("<KeyPress-Right>", self.steer_right)
        self.game.canvas.bind_all("<KeyRelease-Left>", self.no_steer)
        self.game.canvas.bind_all("<KeyRelease-Right>", self.no_steer)

        self.image = self.game.canvas.create_image((WIDTH - self.images[0].width()) / 2, HEIGHT - 100, image=self.images[0], anchor="nw")

        self.velX = 0

    def steer_left(self, event):
        self.game.canvas.itemconfig(self.image, image=self.images[1])
        self.velX = -1

    def steer_right(self, event):
        self.game.canvas.itemconfig(self.image, image=self.images[2])
        self.velX = 1

    def no_steer(self, event):
        self.game.canvas.itemconfig(self.image, image=self.images[0])
        self.velX = 0

    def update(self):
        if self.game.canvas.coords(self.image)[0] + self.velX != 0 and self.game.canvas.coords(self.image)[0] + 64 + self.velX != WIDTH:
            self.game.canvas.move(self.image, self.velX, 0)

# Game Initialization

game = Game("Galactic Criminal")
background = Background(game, "space.png", SPEED)
spaceship = Spaceship(game)
status = Status(game)

# Game loop

while 1:
    game.root.update()
    background.update()
    spaceship.update()
    time.sleep(RENDER)
