#Algorithm starts from here
from genetic_algorithm import *
from feedforward_NN import *
from snake import *
import os


generation_length,population_size,layer_dimension,parents_length = 2500,500, [28,8,4], 50

#population = generate_population(population_size, layer_dimension)

saved_weights = 'snake_game.npz'
#saved_weights = 'Snake game by GA.npz' 

if os.path.isfile( os.getcwd() + '/' + saved_weights):
  data = np.load(saved_weights)
  print('yes file exists')
  population,generation, max_score,max_fitness = data['population'], data['gameStats'][0], data['gameStats'][1], data['gameStats'][2]
#   population, statis = data['POPULATION'], data['STATIS']
#   max_score,max_fitness = 0,0
#   generation = statis[-1][0]+1
else:
    print('doesnot exist')
    population = generate_population(population_size, layer_dimension)
    generation, max_score,max_fitness = 0,0,0

while generation <= generation_length:

#for i in range(generation_length):
    generation += 1
    fitness = []
    parents = []
    print('###################### ','Generation ',generation,' ######################', 'max_score ', max_score, 'max_fitness' , max_fitness)
    for j in range(population_size):
        parameters = vector_to_matrix(population[j], layer_dimension)
        #play_snake(parameters)
        f,score,steps = play_snake(parameters)
        fitness.append(f)
        max_score,max_fitness = max(score,max_score), max(f,max_fitness)
        print('Chromosome ', j, 'has score ' , score, ' with steps ', steps)
    for _ in range(parents_length):
        parents.append(population[fitness.index(max(fitness))])
        fitness[fitness.index(max(fitness))] = -99999
    
    #Crossover and mutation
    X = crossover1(parents, 268)
    Y = mutation(X)



    population = np.concatenate((Y,parents), axis = 0 ) #shape of 500,268
    gameStats = generation, max_score, max_fitness
    np.savez(saved_weights, population = population, gameStats = gameStats)