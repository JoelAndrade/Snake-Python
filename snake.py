import pygame
import random
import sys
import os
import json
import enum

# Try and load load txt file
try:
    with open("settings.txt") as txt_file:
        settings = json.load(txt_file)

# This sets up the defualt settings if there is no txt file
except:
    settings = {
        "high_score":       0,
        "block_length":     40,
        "row":              19,
        "col":              19,
        "snake_color":      (0, 255, 0),
        "grid_color":       (255, 0, 255),
        "food_color":       (0, 225, 200),
        "background_color": "black",
        "speed":            4,
    }

# Constants
snake_length = settings["block_length"] - 1
fps = settings["speed"]
delay_time = 200
pause_timer = 20
high_score = 0

# Setting up pygame stuff
pygame.init()
window = pygame.display.set_mode((settings["row"]*settings["block_length"] + 1, settings["col"]*settings["block_length"] + 1)) # Sets window
pygame.mixer.init() # Initializes the mixer for music
pygame.mixer.music.load(os.path.join("Far Cry 3 - Blood Dragon OST - Blood Dragon Theme (Track 02).mp3")) # Loads music
pygame.mixer.music.set_volume(0.1) # sets volume
clock = pygame.time.Clock()

class Direction(enum.Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NEUTRAL = 5
#

class Snake: 
    def __init__(self, block_length_input, col_input, row_input):
        self.block_length = block_length_input
        self.col = col_input
        self.row = row_input

        self.head_pos_x = (self.col//2)*self.block_length + 1
        self.head_pos_y = (self.row//2)*self.block_length + 1

        self.current_direction_x = Direction.RIGHT.value
        self.current_direction_y = Direction.NEUTRAL.value

        self.direction_input_x = Direction.RIGHT.value
        self.direction_input_y = Direction.NEUTRAL.value

        self.body_pos_x = [(self.col//2)*self.block_length + 1 - self.block_length]
        self.body_pos_y = [(self.row//2)*self.block_length + 1]

        self.tail_pos_x = (self.col//2)*self.block_length + 1 - self.block_length - self.block_length
        self.tail_pos_y = (self.row//2)*self.block_length + 1

        self.play = True
    #

    def collision(self): 
        run = True

        # Check if snake runs into the border
        if ((self.head_pos_x >= self.row*self.block_length + 1) or (self.head_pos_x <= 0) or (self.head_pos_y >= self.row*self.block_length + 1) or (self.head_pos_y <= 0)):
            run = False

        # Check if snake runs into its tail
        if (self.head_pos_x == self.tail_pos_x and self.head_pos_y == self.tail_pos_y):
            run = False

        # Check if snake runs into its body
        for i in range(0, len(self.body_pos_x)):
            if (self.head_pos_x == self.body_pos_x[i] and self.head_pos_y == self.body_pos_y[i]):
                run = False

        return run
    #

    def get_input(self, input):
        if (input == pygame.K_LEFT and self.current_direction_x != Direction.RIGHT.value):
            self.direction_input_x = Direction.LEFT.value
            self.direction_input_y = Direction.NEUTRAL.value
        if (input == pygame.K_RIGHT and self.current_direction_x != Direction.LEFT.value):
            self.direction_input_x = Direction.RIGHT.value
            self.direction_input_y = Direction.NEUTRAL.value
        if (input == pygame.K_UP and self.current_direction_y != Direction.DOWN.value):
            self.direction_input_x = Direction.NEUTRAL.value
            self.direction_input_y = Direction.UP.value
        if (input == pygame.K_DOWN and self.current_direction_y!= Direction.UP.value):
            self.direction_input_x = Direction.NEUTRAL.value
            self.direction_input_y = Direction.DOWN.value
    #

    # Algorithm for moving the snake
    def move_snake(self):
        # Moves Tail first
        self.tail_pos_x = self.body_pos_x[-1]
        self.tail_pos_y = self.body_pos_y[-1]

        # Moves the body next
        for i in range(len(self.body_pos_x) - 1, 0, -1):
            self.body_pos_x[i] = self.body_pos_x[i - 1]
            self.body_pos_y[i] = self.body_pos_y[i - 1]
        self.body_pos_x[0] = self.head_pos_x
        self.body_pos_y[0] = self.head_pos_y

        # Moves the Head last
        if (self.direction_input_x == Direction.LEFT.value):
            self.head_pos_x = self.head_pos_x - self.block_length
        if (self.direction_input_x == Direction.RIGHT.value):
            self.head_pos_x = self.head_pos_x + self.block_length
        if (self.direction_input_y == Direction.UP.value):
            self.head_pos_y = self.head_pos_y - self.block_length
        if (self.direction_input_y == Direction.DOWN.value):
            self.head_pos_y = self.head_pos_y + self.block_length
        
        # This has to do with input issues in the getIput() function. This is so you dont eat the block behind you 
        self.current_direction_x = self.direction_input_x
        self.current_direction_y = self.direction_input_y
    #

    # Pauses the game
    def pause(self, input, CD, settings): 
        check = True
        if (input == pygame.K_SPACE and (CD == pause_timer)):
            while(check):
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        with open('settings.txt','w') as txtFile:
                            json.dump(settings, txtFile)
                        pygame.quit()
                        sys.exit()
                    if (event.type == pygame.KEYDOWN and event.key != pygame.K_p and event.key != pygame.K_m):
                        check = False
                        self.get_input(event.key)
                    if (event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_m)):
                        self.play_music(event.key, settings)
            CD = 0
        return CD
    #

    # Plays music and mutes music
    def play_music(self, input):
        if(input == pygame.K_p):
            pygame.mixer.music.play(-1)
            self.play = True
        if(input == pygame.K_m and self.play == True):
            pygame.mixer.music.pause()
            self.play = False
        elif(input == pygame.K_m and self.play == False):
            pygame.mixer.music.unpause()
            self.play = True
    #
#

class Field:
    def __init__(self, block_lenth_input, snake_length_input, col_input, row_input):
        self.block_length = block_lenth_input
        self.snake_length = snake_length_input
        self.col = col_input
        self.row = row_input
        self.snake_color = (0, 255, 0)
        self.grid_color  = (255, 0, 255)
        self.food_color  = (0, 225, 200)
    #

    def init_colors(self, snake_color_input, grid_color_input, food_color_input, background_color_input):
        self.snake_color      = snake_color_input
        self.grid_color       = grid_color_input
        self.food_color       = food_color_input
        self.background_color = background_color_input
    #

    def place_food(self, head_pos_x, head_pos_y, body_pos_x, body_pos_y, tail_pos_x, tail_pos_y): 
        check = True
        while(check): # This loop checks to see if the food was placed in an empty space
            check = False
            x = random.randint(0, self.col - 1)
            y = random.randint(0, self.row - 1)
            self.food_pos_x = (x*self.block_length) + 1
            self.food_pos_y = (y*self.block_length) + 1

            # Checks if the food was place on the head or tail
            if ((self.food_pos_x == head_pos_x and self.food_pos_y == head_pos_y) or (self.food_pos_x == tail_pos_x and self.food_pos_y == tail_pos_y)):
                check = True
            for i in range(0, len(body_pos_x)): # Checks if the food was placed on the body
                if (self.food_pos_x == body_pos_x[i] and self.food_pos_y == body_pos_y[i]):
                    check = True
    #
            
    def draw_field(self, window_input, head_pos_x, hhead_pos_y, body_pos_x, body_pos_y, tail_pos_x, tail_pos_y):
        # First makes the background Black
        window_input.fill(self.background_color)

        # Then creates the grid lines
        for i in range(0, self.row + 1): 
            pygame.draw.line(window_input, self.grid_color, (0, i*self.block_length), (self.row*self.block_length, i*self.block_length)) # pygame.draw.line(pygame window, RGB color, Start Position, End Position, thickness of the line (default to 1))
            pygame.draw.line(window_input, self.grid_color, (i*self.block_length, 0), (i*self.block_length, self.col*self.block_length))

        # Then draws the snake blocks
        pygame.draw.rect(window_input, self.snake_color, (head_pos_x, hhead_pos_y, self.snake_length, self.snake_length))
        for i in range(0, len(body_pos_x)):
            pygame.draw.rect(window_input, self.snake_color, (body_pos_x[i], body_pos_y[i], self.snake_length, self.snake_length))
        pygame.draw.rect(window_input, self.snake_color, (tail_pos_x, tail_pos_y, self.snake_length, self.snake_length))

        # Lastly draws the food block
        pygame.draw.rect(window_input, self.food_color, (self.food_pos_x, self.food_pos_y, self.snake_length, self.snake_length))
        
        pygame.display.update()
    #
#

def main():
    # Set window
    pygame.mixer.music.play(-1) # Lets music play infinatly in a loop
    field.place_food(snake.head_pos_x, snake.head_pos_y, snake.body_pos_x, snake.body_pos_y, snake.tail_pos_x, snake.tail_pos_y) # Places food down
    run = True # Lets the loop run 
    pause_CD = pause_timer

    while(run):
        clock.tick(fps)
        pygame.time.wait(delay_time)

        # Checks for inputs
        for event in pygame.event.get(): 
            if (event.type == pygame.QUIT):
                with open('settings.txt','w') as txtFile:
                    json.dump(settings, txtFile)
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                snake.get_input(event.key)
                snake.play_music(event.key)
                pause_CD = snake.pause(event.key, pause_CD, settings)
            if (event.type == pygame.KEYUP):
                snake.get_input(event.key)

        # Moves the snakes and checks for collisions
        snake.move_snake()
        run = snake.collision()

        # This is the player does not cheat and pause all the time 
        if (pause_CD < pause_timer):
            pause_CD = pause_CD + 1

        # Makes the snake bigger if the snakes eats the food. It also places a new food block
        if (snake.head_pos_x == field.food_pos_x and snake.head_pos_y == field.food_pos_y):
            field.place_food(snake.head_pos_x, snake.head_pos_y, snake.body_pos_x, snake.body_pos_y, snake.tail_pos_x, snake.tail_pos_y)
            snake.body_pos_x.append(snake.tail_pos_x)
            snake.body_pos_y.append(snake.tail_pos_y)
        
        # Update the highScore
        if (len(snake.body_pos_x) + 2 > settings["high_score"]):
            settings["high_score"] = len(snake.body_pos_x) + 2
        
        # Draw the screen
        if (run):
            field.draw_field(window, snake.head_pos_x, snake.head_pos_y, snake.body_pos_x, snake.body_pos_y, snake.tail_pos_x, snake.tail_pos_y)
            pygame.display.set_caption("Snake Length: " + str(len(snake.body_pos_x) + 2) + "     \
                                                                                                 \
            High Score: " + str(settings["high_score"]))
#


if (__name__ == "__main__"): 
    while(True):
        field = Field(settings["block_length"], snake_length, settings["col"], settings["row"])
        field.init_colors(settings["snake_color"], settings["grid_color"], settings["food_color"], settings["background_color"])

        snake = Snake(settings["block_length"], settings["col"], settings["row"])

        main()
#