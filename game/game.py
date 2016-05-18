import tkinter as tk
import time

# Constant Definition

RENDER = 0.0005
SPEED = 2
WIDTH = 384
HEIGHT = 576

# CLASSES

# Game Classes

class Game(object):
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", 1)

        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)

        self.canvas.pack()

class Coords(object):
    def __init__(self, obj):
        self.x1 = obj.canvas.coords(obj.id)[0]
        self.y1 = obj.canvas.coords(obj.id)[1]
        self.x2 = obj.canvas.coords(obj.id)[2]
        self.y2 = obj.canvas.coords(obj.id)[3]

class Background(object):
    def __init__(self, canvas, background, speed=0):
        self.canvas = canvas
        
        self.bg = tk.PhotoImage(file=background)
        self.width = self.bg.width()
        self.height = self.bg.height()

        self.images = []
        
        for x in range(0, round(WIDTH / self.width)):
            for y in range(0, round(HEIGHT / self.height) + 1):
                self.images.append(self.canvas.create_image(x * self.width, y * self.height, image=self.bg, anchor="nw"))
        
        self.speed = speed

    def update(self):
        i = 0
        for x in range(0, round(WIDTH / self.width)):
            for y in range(0, round(HEIGHT / self.height) + 1):
                self.canvas.move(self.images[i], 0, self.speed)
                if self.canvas.coords(self.images[i])[1] > HEIGHT:
                    self.canvas.coords(self.images[i], x * self.width, 0 - self.height + self.speed)
                    
                i += 1

# General Classes

class Ship(object):
    def __init__(self, canvas, x=0, y=0, *args):
        self.canvas = canvas

        self.images = []
        for img in args:
            self.images.append(tk.PhotoImage(file=img))

        self.width = self.images[0].width()
        self.height = self.images[0].height()

        self.id = self.canvas.create_rectangle(x, y, x + self.width, y + self.height, fill='', outline='')
        self.image = self.canvas.create_image(x, y, image=self.images[0], anchor="nw")

        self.velX = 0
        self.velY = 0

    def coords(self):
        return Coords(self)

    def move(self):
        self.canvas.move(self.image, self.velX, self.velY)
        self.canvas.move(self.id, self.velX, self.velY)

    def update(self):
        self.move()

# Player-Oriented Classes

class Status(object):
    def __init__(self, canvas):
        self.canvas = canvas

        self.images = [tk.PhotoImage(file="normal.png"),
                       tk.PhotoImage(file="shooting.png"),
                       tk.PhotoImage(file="hurt.png"),
                       tk.PhotoImage(file="hurt_shooting.png")]

        self.canvas.bind_all("<KeyPress-space>", self.shoot)
        self.canvas.bind_all("<KeyRelease-space>", self.stop)

        self.bg = self.canvas.create_rectangle(self.images[0].width() / 2, -1, WIDTH, self.images[0].height() - 4, fill="grey", outline="grey")
        self.image = self.canvas.create_image(0, -3, image=self.images[0], anchor="nw")

    def shoot(self, event):
        self.canvas.itemconfig(self.image, image=self.images[1])

    def stop(self, event):
        self.canvas.itemconfig(self.image, image=self.images[0])
    
class Spaceship(Ship):
    def __init__(self, canvas):
        Ship.__init__(self, canvas, (WIDTH - 64) / 2, HEIGHT - 100, "ship.png", "ship_l.png", "ship_r.png")

        self.canvas.bind_all("<KeyPress-Left>", self.steer_left)
        self.canvas.bind_all("<KeyPress-Right>", self.steer_right)
        self.canvas.bind_all("<KeyRelease-Left>", self.no_steer)
        self.canvas.bind_all("<KeyRelease-Right>", self.no_steer)

    def steer_left(self, event):
        self.canvas.itemconfig(self.image, image=self.images[1])
        self.velX = -1

    def steer_right(self, event):
        self.canvas.itemconfig(self.image, image=self.images[2])
        self.velX = 1

    def no_steer(self, event):
        self.canvas.itemconfig(self.image, image=self.images[0])
        self.velX = 0

    def update(self):
        if self.coords().x1 + self.velX > 0 and self.coords().x2 + self.velX < WIDTH:
            self.move()

# Game Initialization

game = Game("Galactic Criminal")
background = Background(game.canvas, "space.png", SPEED)
spaceship = Spaceship(game.canvas)
status = Status(game.canvas)

# Game loop

while 1:
    game.root.update()
    background.update()
    spaceship.update()
    time.sleep(RENDER)
