import numpy as np
import random



def find_block(directions,SorF,head):
  #SorF = Snake or Food points in grid
  arr = [-1]*8
  for k,direction in enumerate(directions):
    for part in SorF:
      if part in direction:
        arr[k] = max( abs( part[0] - head[0] ), abs(part[1] - head[1] )  ) - 1
        break
  return arr


# def generate_input(head,snake_body, foods,M,N):
#   x,y = (head[0],head[1])
#   d2,d6 = [],[]
#   #Generating direction coordinates
#   d1 = [(x-i,y) for i in range(x+1)]
#   #d2
#   for i in range(min(M,N)):
#     if x - i <0 or x - i >9 or y + i < 0 or y + i > 9: break
#     else: d2.append((x - i,y + i))

#   d3 = [(x,y+i) for i in range(N - y )]
#   d4=[(x+i,y+i) for i in range(min(M-x,N-y))]
#   d5 = [(x+i,y) for i in range(M - x)]
#   #d6
#   for i in range(min(M,N)):
#     if x + i <0 or x + i >9 or y - i < 0 or y - i > 9: break
#     else: d6.append((x + i,y - i))

#   d7 = [(x,y-i) for i in range(y + 1)]
#   d8 = [(x-i,y-i) for i in range(min(x+1,y+1))]


#   d = [d1,d2,d3,d4,d5,d6,d7,d8]
#   wall = [ (len(i) - 1) /(min(M,N)-1) for i in d]
#   body = [1 if element == -1 else element/ (min(M,N) - 1) for element in find_block(d,snake_body,(head[0],head[1])) ]
#   all_foods = [0 if element == -1 else (min(M,N) - element - 1 )/ (min(M,N) - 1) for element in find_block(d,foods,(head[0],head[1])) ]
#   vision = [element[i] for i in range(8) for element in [wall,body,all_foods]]

#   coordinates = [[0,1,0,0] , [0,0,1,0] , [0,0,0,1] , [1,0,0,0]] #R D L U
#   dir_out = [(0,1), (1,0), (0,-1) , (-1,0)]
#   #print(head, ' and ' , snake_body)
#   head_direction = coordinates[ dir_out.index( (head[0] - snake_body[0][0], head[1] - snake_body[0][1] ))]
#   return np.array(vision + head_direction).reshape(28,1)

def generate_input(head,snake_body, foods,M,N):
  x,y = (head[0],head[1])
  d2,d6 = [],[]
  #Generating direction coordinates
  d1 = [(x-i,y) for i in range(x+1)]
  #d2
  for i in range(min(M,N)):
    if x - i <0 or x - i >9 or y + i < 0 or y + i > 9: break
    else: d2.append((x - i,y + i))

  d3 = [(x,y+i) for i in range(N - y )]
  d4=[(x+i,y+i) for i in range(min(M-x,N-y))]
  d5 = [(x+i,y) for i in range(M - x)]
  #d6
  for i in range(min(M,N)):
    if x + i <0 or x + i >9 or y - i < 0 or y - i > 9: break
    else: d6.append((x + i,y - i))

  d7 = [(x,y-i) for i in range(y + 1)]
  d8 = [(x-i,y-i) for i in range(min(x+1,y+1))]


  d = [d1,d2,d3,d4,d5,d6,d7,d8]
  wall = [ (len(i) - 1) /(min(M,N)-1) for i in d]
  body = [1 if element == -1 else element/ (min(M,N) - 1) for element in find_block(d,snake_body,(head[0],head[1])) ]
  all_foods = [0 if element == -1 else (min(M,N) - element - 1 )/ (min(M,N) - 1) for element in find_block(d,foods,(head[0],head[1])) ]
  vision = [element[i] for i in range(8) for element in [wall,body,all_foods]]
  
  coordinates = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]  #U R D L
  dir_out = [(0,-1),(1,0),(0,1),(-1,0)]
  
  head_direction = coordinates[ dir_out.index( (head[0] - snake_body[0][0], head[1] - snake_body[0][1] ))]

  return np.array(vision + head_direction).reshape(28,1)
  #print(wall, '\n' , body, '\n' , all_foods )
  print(vision + head_direction)



def generate_population(population_size, layer_dimension):
  weight_size = 0
  for l in range(1,len(layer_dimension)):
    weight_size += layer_dimension[l] * layer_dimension[l-1] + layer_dimension[l]
  x = np.random.choice(np.arange(-1,1, step = 0.001),size = (population_size,weight_size), replace= True)
  return x
   

def vector_to_matrix(population, layer_dimension):
  parameters = {}
  z = 0 
  for l in range(1,len(layer_dimension)):
    x,y = layer_dimension[l], layer_dimension[l-1]
    w,b = population[z: z + x*y ], population[ z+x*y: z + x*y + x]
    parameters['W' + str(l)] = w.reshape(x,y)
    parameters['b' + str(l)] = b.reshape(x,1)
    z =  z + x*y + x
  
  return parameters



def crossover(parents,weight_length):
  #parents length is 21, i[m] using uniform crossover 
  offspring = []
  for i in range(len(parents)):
    for j in range(len(parents)):
      if i == j: continue
      new_weight = [parents[i][l] if random.uniform(0,1) < 0.5 else parents[j][l] for l in range(weight_length)]
      offspring.append(new_weight)
      #print(i,j,new_weight)
      #420 offspring
  return offspring


def mutation(offspring):
  for l in range(len(offspring)):
    for _ in range(15):
      x = random.randint(0,len(offspring[0]) - 1 )
      value = random.choice(np.arange(-0.5, 0.5 , step = 0.001))
      #either change offspring to value or add value to offspring
      offspring[l][x] += value

  n_o = []
  for l in range(59):
    x = random.randint(0,len(offspring[0]) - 1 )
    y = random.randint(0,len(offspring) - 1 )
    value = random.choice(np.arange(-0.5, 0.5 , step = 0.001))
    new_offspring = offspring[y]
    new_offspring[x] += value
    #offspring += new_offspring
    n_o.append(new_offspring)

  return np.concatenate( (offspring,n_o), axis = 0 )



#some work remaining in mutation 21, remaining mutation to be done
