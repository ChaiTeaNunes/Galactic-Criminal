import tkinter as tk
import time

RENDER = 0.0025

class Game(object):
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", 1)

        self.width = 384
        self.height = 576
        
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bd=0, highlightthickness=0)

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

        self.bg = self.game.canvas.create_rectangle(self.images[0].width() / 2, -1, game.width, self.images[0].height() - 4, fill="grey")
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

        self.images = [None for x in range(0, (int(game.width / self.width) + 1) * (int(game.height / self.height) + 1))]

        image = 0
        
        for x in range(0, int(game.width / self.width) + 1):
            for y in range(0, int(game.height / self.height) + 1):
                self.images[image] = self.game.canvas.create_image(x * self.width, y * self.height, image=self.bg, anchor="nw")
                image += 1
        
        self.speed = speed

    def update(self):
        image = 0
        for x in range(0, int(game.width / self.width) + 1):
            for y in range(0, int(game.height / self.height) + 1):
                self.game.canvas.move(self.images[image], 0, self.speed)
                if self.game.canvas.coords(self.images[image])[1] > game.height:
                    self.game.canvas.coords(self.images[image], (image % (int(game.width / self.width) + 1)) * self.width, 0 - self.height + 1)
                image += 1

class Entity(object):
    def __init__(self, game):
        self.game = game

    def update(self):
        raise Exception("All entities must have an update!")

class Spaceship(Entity):
    def __init__(self, game):
        Entity.__init__(self, game)
        
        self.images = [tk.PhotoImage(file="ship.png"),
                       tk.PhotoImage(file="ship_l.png"),
                       tk.PhotoImage(file="ship_r.png")]

        self.game.canvas.bind_all("<KeyPress-Left>", self.steer_left)
        self.game.canvas.bind_all("<KeyPress-Right>", self.steer_right)
        self.game.canvas.bind_all("<KeyRelease-Left>", self.no_steer)
        self.game.canvas.bind_all("<KeyRelease-Right>", self.no_steer)

        self.image = self.game.canvas.create_image((self.game.width - self.images[0].width()) / 2, self.game.height - 100, image=self.images[0], anchor="nw")

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
        if self.game.canvas.coords(self.image)[0] + self.velX != 0 and self.game.canvas.coords(self.image)[0] + 64 + self.velX != self.game.width:
            self.game.canvas.move(self.image, self.velX, 0)

game = Game("Galactic Criminal")
background = Background(game, "space.png", 1)
spaceship = Spaceship(game)
status = Status(game)

while 1:
    game.root.update()
    background.update()
    spaceship.update()
    time.sleep(RENDER)
