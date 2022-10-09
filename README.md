# Snake_AI_using_Neural_Network_and_Genetic_Algorithm

This project is a simple demonstration of how neural network can be used along with genetic algorithm to play snake game. We have a snake that has a brain, we use genetic algorithm to evolve that brain and use Neural Network to make predictions using the same brain.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r /path/to/requirements.txt
```

## Run 

```bash
python3 run_game.py
```

## Demo 
GIF file



## Explanation
Following are the explanations and steps I've gathered along the way.

### Snake Game
This is the first step of the project. This is a straight forward process which you can build easily with simple google search.

### Neural Network Architecture

We use a simple two layer neural network. The first layer has 8 hidden layers and the second is output layer of 4 units. We only use the feed forward part of neural network and discard all the other backpropagation part. We will later use genetic algorithm to improve our weights. 

The figure below explains the basic anatomy of snake. The are two part to it.

#### Input to neural network


![brian](/img/brain.png)

The input of our neural network is what the snake sees. Our snake has vision along eight direction d1 to d8. Along each vision, snake sees 3 different things, **Wall**, **Body** and **Food**. Since the neural network only understands numbers we represent them with a metric, 1 for favorable conditions and 0 for unfavorable. 

**Metric for body:**
One is given when no body is present in that direction and Zero is given when no blocks are present in between Head and Body.


$body = number of blocks between head and body/(total number of blocks - 1 )$.


**Metric for Wall:**
One is given when the number of blocks between Head and Wall are maximum and Zero is given when no blocks are present in between Head and Wall.


$Wall = number of blocks between head and wall/(total number of blocks - 1 )$.


**Metric for Food:**
It is good for snake to move in the direction of food, so One is given when no blocks are present in between Head and Food and Zero is given when no food is present in that direction.


$Food = ( total number of blocks - number of blocks between head and wall - 1)/(total number of blocks - 1 )$.

The another input to our snake is the it's directions. It should keep. track of where it currently is to make move in another direction. 

**Value for Head Direction:** This is a simple one-hot encoding for the direction.  


![head_direction](/img/head_direction.png)


#### Brain of Snake

The brain of our snake is the weights inside our hidden layers and output layers. 

Our first hidden layer will have 8 * 28 weights with 8 bias. 
Our second layer will have 4 * 8 weights with 4 bias. 

So, the total weights + bias counts to 268 which is the actual brain of our snake. So our neural network uses that brain to make a prediction in 4 directions. [Up, Right, Down, Left]


### Genetic Algorithm
Since we do not use the backpropagation of our neural network to improve weights we will use use Genetic algorithm to improve weights. 

Five phases are considered in a genetic algorithm.  
#### Initial brain  
We randomly generate the brain of size (1,268) .
```python
np.random.choice(np.arange(-1,1, step = 0.001),size = (population_size,weight_size), replace= True)
```

weight size is 268 and population_size is the total number of snakes we want to train. I've trained 500 snakes in each generations. The above random function generates a linear vector which is later converted to matrices of sizes (8,28) for weights, (8,1) for bias  and (4,8) for weights and (4,1) for bias  using vector_to_matrix() function. The first two matrices is for hidden layer whereas the other two are for output layer.

#### Fitness function

We have to differentiate the great Snake from weak. snake's fitness is based on its score and number of steps it taken to achieve that score, so we created a function by using Steps and Score as variables which will helps the Snake in getting maximum score in less steps.  
I've used the following fitness function that evaluates fitness of snakes relative to score and steps taken. 


![fitness_function](/img/fitness_function.png)


If two snakes have the same score then the snake that achieves the score in less number of steps is considered. 

####  Selection
The process selects the best fit snakes from the entire population according to their fitness value. It is then used produce a new population of offspring which will be used in a next generation. I've selected 50 snakes initially according to their fitness value. The selected snakes will be called parents.

####  Crossover
We take the parents selected from the above process to produce a new set of offsprings. We take 50 parents and iterate over (population_size - parent_length) times and use uniform crossover method to produce new offspring from these parents. 
we later add our 50 parents to the population set. This process will preserve the best fit snakes, even if the crossover and mutation yield bad set of population.
The unifrom crossover can be explained likewise. 


![crossover](/img/crossover.png)

#### Mutation 
This example explains mutating by flipping bits.     
1	0	1	0	0	1	0   
                
↓
         		
1	0	1	0	1	1	0

But in our case we change the value of our snake's brain. Among 268 brain cells we will change 13 of them randomly between -0.5 to 0.5. 


#### Running
We run the game through many generation to evolve our snake's brain by applying the method explained above. We do it until the snake has learned to score desired number of points. 