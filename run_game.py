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
  population,all_metrics = data['population'], data['all_metrics']
  generation = len(all_metrics)
  print((generation))
  max_score, avg_score = all_metrics[generation -1][0] , all_metrics[generation -1][1]
#   population, statis = data['POPULATION'], data['STATIS']
#   max_score,max_fitness = 0,0
#   generation = statis[-1][0]+1
else:
    print('doesnot exist')
    population = generate_population(population_size, layer_dimension)
    generation = 0
    all_metrics = np.array([[0,0]])
    avg_score = 0
    max_score = 0

while generation <= generation_length:

#for i in range(generation_length):
    generation += 1
    fitness = []
    parents = []

    print('###################### ','Generation ',generation,' ######################', 'max_score ', max_score, 'avg_score' , avg_score)
    for j in range(population_size):
        
        parameters = vector_to_matrix(population[j], layer_dimension)
        #play_snake(parameters)
        f,score,steps = play_snake(parameters)
        fitness.append(f)
        max_score = max(score,max_score)
        avg_score += score
        print('Chromosome ', j, 'has score ' , score, ' with steps ', steps)
    for _ in range(parents_length):
        parents.append(population[fitness.index(max(fitness))])
        fitness[fitness.index(max(fitness))] = -99999
    
    avg_score /= population_size
    #Crossover and mutation
    X = crossover1(parents, 268)
    Y = mutation(X)

    all_metrics = np.append(all_metrics, [[max_score,avg_score/population_size]], axis = 0 )

    print('all_metrics' , all_metrics)
    population = np.concatenate((Y,parents), axis = 0 ) #shape of 500,268

    np.savez(saved_weights, population = population, all_metrics = all_metrics)












    


        

