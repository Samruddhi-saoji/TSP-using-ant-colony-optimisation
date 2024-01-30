from tsp import TSP
from aco import ACO
from random import random

##### create the TSP ######
#randomly generate the cities
n = 12 #number of cities
cities = []
max_dist = 2000
for i in range(n) :
    tup = (max_dist*random(), max_dist*random(), i, i+1) #(x, y, index, name)
    cities.append(tup)

#the TSP problem
tsp = TSP(n, cities)

##### run the aco algorithm ######
# Hyper parameters
epochs = 50
ants = 10 #no of ants
alpha = 1
beta = 5
rho = 0.5

aco = ACO(tsp, epochs=epochs, ants=ants, alpha=alpha, beta=beta, rho=rho)
best_route, best_distance = aco.run()
print(f'Best route: {best_route}')
print(f'Best distance: {best_distance}')