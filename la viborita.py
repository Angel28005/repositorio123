from tkinter import *
import random

#LO VISUAL
GAME_WIDTH = 400
GAME_HEIGHT = 300
VELOCIDAD = 100
SPACE_SIZE = 30
CUERPO = 3
VIBORA_COLOR = "#FD7EE7"
COMIDA_COLOR = "#77E13D"
BACKGROUND_COLOR = "#222223"

class Vibora:
    def __init__(self):
        self.body_size = CUERPO
        self.coordinates = []
        self.squares = []

        for i in range(0, CUERPO):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=VIBORA_COLOR, tag="vibora")
            self.squares.append(square)

class Comida:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=COMIDA_COLOR, tag="comida")

def next_turn(vibora, comida):
    x, y = vibora.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    vibora.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=VIBORA_COLOR)
    vibora.squares.insert(0, square)

    if x == comida.coordinates[0] and y == comida.coordinates[1]:
        global puntos
        puntos += 1
        label.config(text="Puntos: {}".format(puntos))
        canvas.delete("comida")
        comida = Comida()
    else:
        del vibora.coordinates[-1]
        canvas.delete(vibora.squares[-1])
        del vibora.squares[-1]

    if check_collisions(vibora):
        perdiste()
    else:
        window.after(VELOCIDAD, next_turn, vibora, comida)

def change_direction(nueva_direccion):
    global direction

    if nueva_direccion == 'left':
        if direction != 'right':
            direction = nueva_direccion
    elif nueva_direccion == 'right':
        if direction != 'left':
            direction = nueva_direccion
    elif nueva_direccion == 'up':
        if direction != 'down':
            direction = nueva_direccion
    elif nueva_direccion == 'down':
        if direction != 'up':
            direction = nueva_direccion

def check_collisions(vibora):
    x, y = vibora.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in vibora.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def perdiste():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
    font=('consolas', 50), text=":(", fill="white", tag="perdiste")

window = Tk()
window.title("La viborita")
window.resizable(False, False)

puntos = 0
direction = 'down'

label = Label(window, text="Puntos: {} la vibora se mueve con W,A,S,D".format(puntos), font=('consolas', 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

vibora = Vibora()
comida = Comida()

window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

next_turn(vibora, comida)

window.mainloop()