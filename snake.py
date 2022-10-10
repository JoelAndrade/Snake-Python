import pygame
import random
import sys
import os
import json

# Constants
row = 19
col = 19
blockLength = 40
snakeLength = blockLength - 1
snakeColor = (0,255,0)
gridColor = (255,0,255)
foodColor = (0,225,200)
fps = 4
delayTime = 200
pauseConstant = 20
highScore = 0

# Sets up the settings
try: # Loads .txt file
    with open('settings.txt') as txtFile:
        settings = json.load(txtFile)
    blockLength = settings['blockLength']
    snakeLength = blockLength - 1
except: # The program will pass if there is no txt file
    settings = { # This sets up the defualt settings if there is no txt file
        'highScore': highScore,
        'blockLength': blockLength,
    }
    


# Setiing up pygame stuff
pygame.init()
window = pygame.display.set_mode((row*blockLength+1, col*blockLength+1)) # Sets window
pygame.mixer.init() # Initializes the mixer for music
pygame.mixer.music.load(os.path.join("Far Cry 3 - Blood Dragon OST - Blood Dragon Theme (Track 02).mp3")) # Loads music
pygame.mixer.music.set_volume(0.1) # sets volume
clock = pygame.time.Clock() # Sets up the pygame 

class Snake: 
    def __init__(self):
        # Sets up vaiables assiociated with the snake
        self.xHeadPos = (col//2)*blockLength + 1 # 361
        self.yHeadPos = (row//2)*blockLength + 1

        self.xCurrentDirection = 1
        self.yCurrentDirection = 0

        self.xDirectionInput = 1
        self.yDirectionInput = 0

        self.xBodyPos = [(col//2)*blockLength + 1 - blockLength]
        self.yBodyPos = [(row//2)*blockLength + 1]

        self.xTailPos = (col//2)*blockLength + 1 - blockLength -blockLength
        self.yTailPos = (row//2)*blockLength + 1

        self.play = True

    def collision(self): # Checks to see if the snake ran into the border or itself
        run = True
        if ((self.xHeadPos >= row*blockLength+1) or (self.xHeadPos <= 0) or (self.yHeadPos >= row*blockLength+1) or (self.yHeadPos <= 0)):
            run = False
        if (self.xHeadPos == self.xTailPos and self.yHeadPos == self.yTailPos):
            run = False
        for i in range(0, len(self.xBodyPos)):
            if (self.xHeadPos == self.xBodyPos[i] and self.yHeadPos == self.yBodyPos[i]):
                run = False
        return run
        
    def getInput(self,input): # Take movement inputs
        if(input == pygame.K_LEFT and self.xCurrentDirection != 1):
            self.xDirectionInput = -1
            self.yDirectionInput = 0
        if(input == pygame.K_RIGHT and self.xCurrentDirection != -1):
            self.xDirectionInput = 1
            self.yDirectionInput = 0
        if(input == pygame.K_UP and self.yCurrentDirection != 1):
            self.xDirectionInput = 0
            self.yDirectionInput = -1
        if(input == pygame.K_DOWN and self.yCurrentDirection!= -1):
            self.xDirectionInput = 0
            self.yDirectionInput = 1
                
    def moveSnake(self): # Algorithm for moving the snake
        # Moves Tail first
        lastElement = len(self.xBodyPos) - 1
        self.xTailPos = self.xBodyPos[lastElement]
        self.yTailPos = self.yBodyPos[lastElement]

        # Moves the body next
        for i in range(len(self.xBodyPos)-1, 0, -1):
            self.xBodyPos[i] = self.xBodyPos[i-1]
            self.yBodyPos[i] = self.yBodyPos[i-1]
        self.xBodyPos[0] = self.xHeadPos
        self.yBodyPos[0] = self.yHeadPos

        # Moves the Head last
        if(self.xDirectionInput == -1):
            self.xHeadPos = self.xHeadPos - blockLength
        if(self.xDirectionInput == 1):
            self.xHeadPos = self.xHeadPos + blockLength
        if(self.yDirectionInput == -1):
            self.yHeadPos = self.yHeadPos - blockLength
        if(self.yDirectionInput == 1):
            self.yHeadPos = self.yHeadPos + blockLength
        
        # This has to do with input issues in the getIput() function. This is so you dont eat the block behind you 
        self.xCurrentDirection = self.xDirectionInput
        self.yCurrentDirection = self.yDirectionInput

    def pause(self, input, CD): # Pauses the game 
        check = True
        if (input == pygame.K_SPACE and (CD == pauseConstant)):
            while(check):
                for event in pygame.event.get():
                    if (event.type == pygame.QUIT):
                        with open('settings.txt','w') as txtFile:
                            json.dump(settings, txtFile)
                        pygame.quit()
                        sys.exit()
                    if (event.type == pygame.KEYDOWN and event.key != pygame.K_p and event.key != pygame.K_m):
                        check = False
                        self.getInput(event.key)
                    if (event.type == pygame.KEYDOWN and (event.key == pygame.K_p or event.key == pygame.K_m)):
                        self.playMusic(event.key)
            CD = 0
        return CD    

    def playMusic(self, input): # Plays music and mutes music
        if(input == pygame.K_p):
            pygame.mixer.music.play(-1)
            self.play = True
        if(input == pygame.K_m and self.play == True):
            pygame.mixer.music.pause()
            self.play = False
        elif(input == pygame.K_m and self.play == False):
            pygame.mixer.music.unpause()
            self.play = True

class Field:
    def __init__(self):
        pass

    def placeFood(self, xHeadPos, yHeadPos, xBodyPos, yBodyPos, xTailPos, yTailPos): # Places the food 
        check = True
        while(check): # This loop checks to see if the food was placed in an empty space
            check = False
            x = random.randint(0,col-1)
            y = random.randint(0,row-1)
            self.xFoodPos = (x*blockLength) + 1
            self.yFoodPos = (y*blockLength) + 1

            if ((self.xFoodPos == xHeadPos and self.yFoodPos == yHeadPos) or (self.xFoodPos == xTailPos and self.yFoodPos == yTailPos)): # Checks if the food was place on the head or tail
                check = True
            for i in range(0, len(xBodyPos)): # Checks if the food was placed on the body
                if (self.xFoodPos == xBodyPos[i] and self.yFoodPos == yBodyPos[i]):
                    check = True
            
    def drawField(self, xHeadPos, yHeadPos, xBodyPos, yBodyPos, xTailPos, yTailPos): 
        window.fill("black") # First makes the background Black

        # Then creates the grid lines
        for i in range(0, row+1): 
            pygame.draw.line(window, gridColor, (0, i*blockLength), (row*blockLength, i*blockLength)) # pygame.draw.line(pygame window, RGB color, Start Position, End Position, thickness of the line (default to 1))
            pygame.draw.line(window, gridColor, (i*blockLength, 0), (i*blockLength, col*blockLength))

        # Then draws the snake blocks
        pygame.draw.rect(window, snakeColor, (xHeadPos, yHeadPos, snakeLength, snakeLength))    
        for i in range(0, len(xBodyPos)):
            pygame.draw.rect(window, snakeColor, (xBodyPos[i], yBodyPos[i], snakeLength, snakeLength))
        pygame.draw.rect(window, snakeColor, (xTailPos, yTailPos, snakeLength, snakeLength))

        # Lastly draws the food block
        pygame.draw.rect(window, foodColor, (self.xFoodPos, self.yFoodPos, snakeLength, snakeLength))

        # This lets you see how big you are in the game and high score. Keep in mind the line breaks for the long string
        pygame.display.set_caption("Snake Length: "+str(len(xBodyPos) + 2)+"            \
                                                                                        \
        High Score: "+str(settings['highScore'])) 
        
        pygame.display.update()

def main():
    # Set window
    pygame.mixer.music.play(-1) # Lets music play infinatly in a loop
    field.placeFood(snake.xHeadPos, snake.yHeadPos, snake.xBodyPos, snake.yBodyPos, snake.xTailPos, snake.yTailPos) # Places food down
    run = True # Lets the loop run 
    pauseCD = pauseConstant

    while(run):
        clock.tick(fps)
        pygame.time.wait(delayTime)

        # Checks for inputs
        for event in pygame.event.get(): 
            if (event.type == pygame.QUIT):
                with open('settings.txt','w') as txtFile:
                    json.dump(settings, txtFile)
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                snake.getInput(event.key)
                snake.playMusic(event.key)
                pauseCD = snake.pause(event.key, pauseCD)
            if (event.type == pygame.KEYUP):
                snake.getInput(event.key)

        # Moves the snakes and checks for collisions
        snake.moveSnake()
        run = snake.collision()

        # This is the player does not cheat and pause all the time 
        if (pauseCD < pauseConstant):
            pauseCD = pauseCD + 1

        # Makes the snake bigger if the snakes eats the food. It also places a new food block
        if (snake.xHeadPos == field.xFoodPos and snake.yHeadPos == field.yFoodPos):
            field.placeFood(snake.xHeadPos, snake.yHeadPos, snake.xBodyPos, snake.yBodyPos, snake.xTailPos, snake.yTailPos)
            snake.xBodyPos.append(snake.xTailPos)
            snake.yBodyPos.append(snake.yTailPos)
        
        # Update the highScore
        if (len(snake.xBodyPos) + 2 > settings['highScore']):
            settings['highScore'] = len(snake.xBodyPos) + 2
        
        # Draw the screen
        if (run):
            field.drawField(snake.xHeadPos, snake.yHeadPos, snake.xBodyPos, snake.yBodyPos, snake.xTailPos, snake.yTailPos)

if (__name__ == "__main__"): 
    while(True):  # Runs the game indefinetly
        field = Field()
        snake = Snake()
        main()