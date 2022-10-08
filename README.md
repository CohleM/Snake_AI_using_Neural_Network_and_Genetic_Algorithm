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

![alt text](https://drive.google.com/file/d/1I9vUTOQ0V9P2si2_uInH5a8TVvBkc5Ti/view?usp=sharing)

The input of our neural network is what the snake sees. Our snake has vision along eight direction d1 to d8. Along each vision, snake sees 3 different things, **Wall**, **Body** and **Food**. Since the neural network only understands numbers we represent them with a metric, 1 for favorable conditions and 0 for unfavorable. 

**Metric for body:**
One is given when no body is present in that direction and Zero is given when no blocks are present in between Head and Body.


$body = number of blocks between head and body/(total number of blocks - 1 )$.


**Metric for Wall:**
One is given when the number of blocks between Head and Wall are maximum and Zero is given when no blocks are present in between Head and Wall.


$Wall = number of blocks between head and wall/(total number of blocks - 1 )$.


**Metric for Food:**
It is good for snake to move in the direction of food, so One is given when no blocks are present in between Head and Food and Zero is given when no food is present in that direction.


$Food = (total number of blocks - number of blocks between head and wall - 1)/(total number of blocks - 1 )$.

The another input to our snake is the it's directions. It should keep. track of where it currently is to make move in another direction. 

**Value for Head Direction:** This is a simple one-hot encoding for the direction.  

![alt text](https://drive.google.com/file/d/1_XKc26GR8DEqfxT9tPmb2rZVR-J1VjFQ/view?usp=sharing)


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

wight size is 268 and population_size is the total number of snakes we want to train. I've trained 500 snakes in each generations.

#### Fitness function

We have to differentiate the great Snake from weak. snake's fitness is based on its score and number of steps it taken to achieve that score, so we created a function by using Steps and Score as variables which will helps the Snake in getting maximum score in less steps.
A function was created from which we will differentiate the snakes based on steps and it gives a values between -1 to 1   
Selection. 
Crossover. 
Mutation. 

### TBC