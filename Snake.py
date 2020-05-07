import tkinter as tk
from PIL import Image, ImageTk
import random

MOVE_INCREMENT = 20
move_speed = 15
GAME_SPEED = 1000 // move_speed

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600,height=620,background="black",highlightthickness=0)

        self.snake_positions =[(100,100),(80,100),(60,100)]
        self.food_position = self.new_food_position()
        self.score=0
        self.direction ="Right"
        self.bind_all("<Key>",self.on_key_press)

        self.load_assets()
        self.create_object()# place the assests into the window

        self.after(GAME_SPEED,self.perform_action)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open("snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("food.png")
            self.food = ImageTk.PhotoImage(self.food_image)

        except IOError as error:
            print(error)
            root.destroy()

    def create_object(self):
        self.create_text(
            40,20,
            text = f"Score {self.score} (speed: {move_speed})", 
            tag="score",fill ="#fff",
            font=("TkDefaultFont",14)
        )
        
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position,y_position,image=self.snake_body,tag="snake")
        
        self.create_image(self.food_position[0],
                          self.food_position[1],
                          image = self.food,tag="food")# *self.food_position is desturcturimg
        
        self.create_rectangle(7,27,593,613,outline = "#525d69")

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]
        if self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Up":
            new_head_position = (head_x_position , head_y_position - MOVE_INCREMENT)
        elif self.direction == "Down":
            new_head_position = (head_x_position , head_y_position + MOVE_INCREMENT)

        self.snake_positions=[new_head_position] + self.snake_positions[:-1]

        for segments , positions  in zip(self.find_withtag("snake"),self.snake_positions):
            self.coords(segments,positions) 

    def perform_action(self):
        if self.check_collisions():
            self.end_game()
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED,self.perform_action)

    def check_collisions(self):
        head_x_position , head_y_position = self.snake_positions[0]

        return (
            head_x_position in (0,580)
            or head_y_position in (20,620)
            or (head_x_position,head_y_position) in self.snake_positions[1:]
        )
    def on_key_press(self, e):
        new_direction = e.keysym

        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(*self.snake_positions[-1], image=self.snake_body,tag="snake")
            if self.score % 5 == 0:
                global move_speed
                move_speed += 1
            self.food_position = self.new_food_position()
            self.coords(self.find_withtag("food"),self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score,
                               text=f"Score {self.score}(speed: {move_speed})",
                               tag="score")

    def new_food_position(self):
        while True:
            x_position = random.randint(1,29) * MOVE_INCREMENT
            y_position = random.randint(3, 30) * MOVE_INCREMENT
            food_positions = (x_position,y_position)
            if food_positions not in self.snake_positions:
                return food_positions

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text = f"GAME over...!! your score is {self.score}",
            fill = "#fff",
            font = ("TkDefaultFont",14)
        )

root=tk.Tk()
root.title("Snake Game")
root.resizable(False,False)
board = Snake()
board.pack()

root.mainloop()
