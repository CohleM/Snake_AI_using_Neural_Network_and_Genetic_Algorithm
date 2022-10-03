import numpy as np
import random

def sigmoid(Z):
    return 1/(1 + np.exp(-Z))

def relu(Z):
    return np.maximum(0, Z)

def forward_propogation(X,parameters):
  L = len(parameters)//2
  #Relu in hidden layers
  A = X
  for l in range(1,L):
    A_prev = A
    Z = np.dot(parameters['W'+str(l)], A_prev) + parameters['b'+str(l)]
    A = relu(Z)
  #Sigmoid in output layer 
  Z_final = np.dot(parameters['W'+str(L)], A) + parameters['b'+str(L)]
  return sigmoid(Z_final)


