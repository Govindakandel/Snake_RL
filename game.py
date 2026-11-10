import pygame
from collections import deque
import random
from typing import Literal



pygame.init()

# global variables
height = 600
width = 800
Cell_size = 20
speed = Cell_size  # the snake moves one cell at a time
score = 0

class Snake :
    def __init__(self):
        self.body = deque([pygame.Rect(width // 2, height // 2, Cell_size, Cell_size),  pygame.Rect(width // 2 +Cell_size, height // 2, Cell_size, Cell_size)])  # initialize the snake's body with one segment at the center of the screen
        self.direction = "Right"
        self.new_tail = None  # initialize new_tail to None

    def move(self , action : Literal["Up" , "Down" , "Left" , "Right" ]):
        head = self.body[0].copy() # (h_x , h_y)
        if self.direction == "Left" or self.direction == "Right":
            if action == "Up":
                self.direction = "Up"
                head.center = (head.centerx, head.centery - speed)
            elif action == "Down":
                self.direction = "Down"
                head.center = (head.centerx, head.centery + speed)
            else :
                if self.direction == "Left":
                    head.center = (head.centerx - speed, head.centery)
                else :
                    head.center = (head.centerx + speed, head.centery)
        elif self.direction == "Up" or self.direction == "Down":
            if action == "Left":
                self.direction = "Left"
                head.center = (head.centerx - speed, head.centery)
            elif action == "Right":
                self.direction = "Right"
                head.center = (head.centerx + speed, head.centery)
            else :
                if self.direction == "Up":
                    head.center = (head.centerx, head.centery - speed)
                else :
                    head.center = (head.centerx, head.centery + speed)
        self.body.appendleft(head)
        self.new_tail = self.body.pop()  # remove the tail segment to maintain the length of the snake

    def grow(self):
       self.body.append(self.new_tail)  # add a new segment at the tail position


class SnakeGame:
    def __init__(self):
        self.snake = Snake()
        self.foodpos , self.food = None, None
        self.food_generate()

    def check_collision(self):
        head = self.snake.body[0]
        # Check if the snake collides with the walls
        if head.left < 0 or head.right > width or head.top < 0 or head.bottom > height:
            print("Collision with wall")
            return True
        # Check if the snake collides with itself
        for body in list(self.snake.body)[1:]:
            if head.colliderect(body):
                print("Collision with self")
                return True
        return False

    def check_food_collision(self):
        if self.snake.body[0].colliderect(self.food):
            self.snake.grow()
            self.food_generate()
            print("Food collected!")
            return True
        return False

    def food_generate(self):
        while True:
            self.foodpos = (random.randint(0, width // Cell_size - 1) * Cell_size,
                            random.randint(0, height // Cell_size - 1) * Cell_size)
            self.food = pygame.Rect(self.foodpos[0], self.foodpos[1], Cell_size, Cell_size)
            if not any(self.food.colliderect(body) for body in self.snake.body):
                break


    def reset(self):
        self.snake = Snake()
        self.food_generate()


# set screen title and size
game = SnakeGame()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
running = True
clock = pygame.time.Clock()
            # game loop
font = pygame.font.SysFont(None, 75)
go_text = font.render("Game Over", True, (255, 0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.snake.move("Up")
            elif event.key == pygame.K_DOWN:
                game.snake.move("Down")
            elif event.key == pygame.K_LEFT:
                game.snake.move("Left")
            elif event.key == pygame.K_RIGHT:
                game.snake.move("Right")

    # if no arrow key is pressed, continue moving in the current direction
    if not any(event.type == pygame.KEYDOWN and event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] for event in pygame.event.get()):
            game.snake.move(game.snake.direction)  # continue moving in the current direction if no arrow key is pressed
    # check for collisions
    if game.check_collision():
        # game over text screen pause for 20 seconds
        screen.blit(go_text, (width // 2 - go_text.get_width() // 2, height // 2 - go_text.get_height() // 2))
        message_text = font.render(f"Press any key to restart", True, (255, 255, 255))
        screen.blit(message_text, (width // 2 - message_text.get_width() // 2, height // 2 + go_text.get_height()))
        pygame.display.flip()
        wait = True
        while wait:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                    wait = False
                    running = False
            elif event.type == pygame.KEYDOWN:
                wait = False
                game.reset()
                score = 0
        # wait for key press 
        if event.type == pygame.KEYDOWN:
            game.reset()


    # check for food collision
    if game.check_food_collision():
        score += 1

    # display the snake and food
    screen.fill((0, 0, 0))  # fill the screen with black
    
    pygame.draw.rect(screen, (255, 0, 0), game.food)
    for body in game.snake.body:
        pygame.draw.rect(screen, (0, 255, 0), body)

    # display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(5)

pygame.quit()



