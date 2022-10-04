import pygame
import random
from genetic_algorithm import *
from feedforward_NN import *

class Snake:

    def __init__(self,row = 10,column = 10):
        self.head = [random.randint(3,8), random.randint(3,8)]
        self.body = []
        self.speedx, self.speedy = 0,-1
        self.row,self.column = row,column
        self.fruit = []
        self.score = 0
        self.fitness = 0
        self.steps = 0
    
    def genFruit(self):
        self.fruit  =  [random.randint(0,9), random.randint(0,9)]
    
    def ifEaten(self):
        self.body.insert(0, (self.head[0], self.head[1])) 
        self.head = self.fruit
        self.score +=1

    def atEachFrame(self):
        self.body.insert(0,(self.head[0], self.head[1]))
        self.head[0],self.head[1] = self.head[0] + self.speedx, self.head[1] + self.speedy
        self.body.pop()

    def obstacles(self): 
        if (self.head[0] < 0 or self.head[0] >= self.column ) or (self.head[1] >= self.row or self.head[1] < 0 ): return True
        if (self.head[0], self.head[1]) in self.body[1:]: return True
    

    

def play_snake(parameters):
    pygame.init() 
    s = Snake()
    s.genFruit()
    s.body.append((s.head[0],s.head[1]-1))
    blue,red = (0, 0, 255) , (255, 0, 0) # hex code for blue
    grid_size,snake_speed = 25,10000
    screen = pygame.display.set_mode((s.column*grid_size, s.row*grid_size))
    s.speedx,s.speedy = 0,-1
    game_over,running = False,True
    clock = pygame.time.Clock()
    while running:
      if not game_over:

        #Input to our Neural Network, X = input, Y = output
        X = generate_input(s.head,s.body, [(s.fruit[0],s.fruit[1] )],s.row,s.column)
        Y = forward_propogation(X, parameters)
        dir_out = [(0,-1),(1,0),(0,1),(-1,0)]    #U R D L 

        #Making sure it doesnot run in opposite direction 
        if (-1*s.speedx,-1*s.speedy) == dir_out[np.argmax(Y)]:
            b = Y.reshape(4)
            c = (-b).argsort()[:2]
            s.speedx, s.speedy = dir_out[c[1]]
        else:
            s.speedx, s.speedy = dir_out[np.argmax(Y)]

        #print([(s.fruit[0],s.fruit[1] )] , ' gg ')
        s.steps +=1
        screen.fill((0,0,0)) 
        
        #When snake eats some fuit
        if( s.head == [s.fruit[0], s.fruit[1] ] ):
            print('True Eaten')
            s.ifEaten()
            s.genFruit()
        
        #When it collides with itself or walls
        if s.obstacles() or s.steps >= 200:
            game_over = True
            s.fitness = (s.score + 0.5 + (0.5* ((s.score - (s.steps/(s.score + 1) ))/(s.score + (s.steps/ (s.score + 1) ) ) ) ))*1000000
            return s.fitness,s.score,s.steps
        s.atEachFrame()

        pygame.draw.rect(screen, (255,255,255), [s.head[0]*grid_size, s.head[1]*grid_size, grid_size, grid_size]) 
        for parts in s.body:
            pygame.draw.rect(screen, red, [parts[0]*grid_size, parts[1]*grid_size, grid_size, grid_size])
        pygame.draw.rect(screen, blue, [s.fruit[0]*grid_size, s.fruit[1]*grid_size, grid_size, grid_size])
      
      pygame.display.flip()
      clock.tick(snake_speed)

      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_LEFT:
                s.speedx = -1
                s.speedy = 0
            elif event.key == pygame.K_RIGHT:
                s.speedx = 1
                s.speedy = 0
            elif event.key == pygame.K_UP:
                s.speedx = 0
                s.speedy = -1
            elif event.key == pygame.K_DOWN:
                s.speedx = 0
                s.speedy = 1
        # If the event is "QUIT" (when user clicks X on window)
        if event.type == pygame.QUIT:
          # Set running to False, stop event loop
          running = False
