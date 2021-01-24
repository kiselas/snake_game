import random
import time
from collections import deque
from tkinter import *

from PIL import ImageTk, Image

game_width = 700
game_height = 600
snake_item = 50
start_x = 7
start_y = 6
snake_x_nav = 0
snake_y_nav = 0
snake_size = 3
difficulty = {'Easy': 0.50, 'Medium': 0.15, 'Hard': 0.05}

tk = Tk()
tk.title('Snake on Python')
canvas = Canvas(tk, width=game_width, height=game_height,
                bd=0)
# set bg
image = ImageTk.PhotoImage(Image.open('media/bg.png'))
canvas.create_image(0, 0, anchor=NW, image=image)
canvas.pack()
tk.update()

# infinite queue of colors
colors = deque(["#640CAB", "#582781", "#3F046F", "#9240D5", "#A468D5", '#FFF500', '#BFBA30',
                '#A69F00', '#FFF840', '#FFFA73'
                ])

# the snake takes the color of the eaten apple
next_snake_color = deque(['white', 'white'])


def pick_color_apple(colors):
    temp = colors.popleft()
    colors.append(temp)
    global next_snake_color
    next_snake_color.popleft()
    next_snake_color.append(temp)
    return temp


class SnakeApple:

    def __init__(self):
        self.apple_color = pick_color_apple(colors)
        self.coord_x = random.randrange(1, 14)
        self.coord_y = random.randrange(1, 12)
        self.apple = canvas.create_oval(self.coord_x * snake_item, self.coord_y * snake_item,
                                        self.coord_x * snake_item + snake_item, self.coord_y * snake_item + snake_item,
                                        fill=self.apple_color)

    def eat_apple(self):
        canvas.delete(self.apple)

    def check_eat_apple(self, snake_coord_x, snake_coord_y):
        if snake_coord_x == self.coord_x and snake_coord_y == self.coord_y:
            return True


class Snake:

    def __init__(self, canvas=canvas, game_width=game_width, game_height=game_height,
                 snake_size=snake_size, start_x=start_x, start_y=start_y):
        self.snake_list = []
        self.snake_size = snake_size
        self.snake_x = start_x
        self.snake_y = start_y
        self.snake_x_nav = 0
        self.snake_y_nav = 0
        self.canvas = canvas
        self.game_width = game_width
        self.game_height = game_height
        self.last_move = ['start']
        self.game_running = True

    # create and increasing the snake
    def paint_item(self):

        snake_elem = self.canvas.create_rectangle(self.snake_x * snake_item, self.snake_y * snake_item,
                                                  self.snake_x * snake_item + snake_item,
                                                  self.snake_y * snake_item + snake_item,
                                                  fill=next_snake_color[0])
        self.snake_list.append(snake_elem)
        canvas.bind_all('<KeyPress-Left>', self.snake_move)
        canvas.bind_all('<KeyPress-Right>', self.snake_move)
        canvas.bind_all('<KeyPress-Up>', self.snake_move)
        canvas.bind_all('<KeyPress-Down>', self.snake_move)
        self.check_snake_items()

    def check_snake_items(self):

        if len(self.snake_list) >= self.snake_size:
            print(self.snake_list[0])
            temp_item = self.snake_list.pop(0)
            self.canvas.delete(temp_item)

    def check_border(self):

        game_border_x = self.game_width // snake_item - 1
        game_border_y = self.game_height // snake_item - 1
        if self.snake_x > game_border_x or self.snake_x < 0 \
                or self.snake_y > game_border_y or self.snake_y < 0:
            self.game_over()

    def game_over(self):
        game = self.canvas.create_text(self.game_width / 2, self.game_height / 2,
                                       text="GAME OVER!",
                                       font="Arial 60",
                                       fill="#ff0000")
        self.game_running = False

    def snake_move(self, event):
        global difficulty
        while self.game_running:
            if event.keysym == 'Up':
                if self.last_move[0] != 'Down':
                    print(self.last_move[0])
                    self.last_move[0] = 'Up'
                    self.snake_x_nav = 0
                    self.snake_y_nav = -1
                    self.check_snake_items()
            if event.keysym == 'Down':
                if self.last_move[0] != 'Up':
                    self.last_move[0] = 'Down'
                    self.snake_x_nav = 0
                    self.snake_y_nav = 1
                    self.check_snake_items()
            if event.keysym == 'Left':
                if self.last_move[0] != 'Right':
                    self.last_move[0] = 'Left'
                    self.snake_x_nav = -1
                    self.snake_y_nav = 0
                    self.check_snake_items()
            if event.keysym == 'Right':
                if self.last_move[0] != 'Left':
                    self.last_move[0] = 'Right'
                    self.snake_x_nav = 1
                    self.snake_y_nav = 0
                    self.check_snake_items()
            self.check_border()
            self.snake_x = self.snake_x + self.snake_x_nav
            self.snake_y = self.snake_y + self.snake_y_nav
            self.paint_item()

            # defines game speed
            time.sleep(difficulty['Medium'])

            tk.update_idletasks()
            tk.update()

            if apple.check_eat_apple(self.snake_x, self.snake_y):
                apple.eat_apple()
                self.snake_size = self.snake_size + 1
                apple.__init__()


snake = Snake(canvas=canvas, game_width=game_width, game_height=game_height,
              snake_size=snake_size, start_x=start_x, start_y=start_y)

snake.paint_item()

apple = SnakeApple()

tk.mainloop()
