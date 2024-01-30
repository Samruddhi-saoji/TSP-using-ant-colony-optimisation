import numpy as np 
from random import choices

''' Note
- route = [C1, C2, C3, C4]; path = (C2, C3)
- thus, route = group/sequence of paths
'''

class ACO:
    def __init__(self, tsp, epochs, ants=10, alpha=1, beta=5, rho=0.5):
        # n = no of cities
        self.tsp = tsp
        self.ants = ants    #number of ants
        self.epochs = epochs
        self.alpha = alpha  # Pheromone weight
        self.beta = beta    # Heuristic weight
        self.rho = rho      #rate of evaporation
        self.pheromone = np.ones((tsp.n, tsp.n)) #2d matrix of shape (n,n)
            # pheromone[i][j] = amt of pheromone on the path btw city 'i' and city 'j'
            # i, j --> indexes of the cities in TSP cities list


    ######################### solve TSP #########################
    def run(self):
        #best solution found yet
        best_route = None
        best_distance = float('inf')

        #run the algorithm
        for _ in range(self.epochs):
            # for each ant
            for ant in range(self.ants):
                route = self.get_route() #route taken by this ant
                distance = self.tsp.cost(route)

                #if this is the best path yet
                if distance < best_distance:
                    best_distance = distance
                    best_route = route

        return best_route, best_distance


    ########################## get the route #########################
    def get_route(self):
        ########### Step 1: start from random city #######
        current_city = choices(self.tsp.cities)[0]
        route = [current_city] #list of visited cities

        #list of unvisited cities
        remaining = set(self.tsp.cities)
        remaining.remove(current_city)

        ########### Step 2: visit one city at a time #######
        while remaining:
            #select the next city to visit based on f value
            next_city = self.select_next_city(current_city, remaining)

            # add it to the route, and remove from list of unvisited cities
            route.append(next_city)
            remaining.remove(next_city)

            #update
            current_city = next_city
        #all cities have been visited exactly once

        ########### Step 3: update pheromone level for this route #######
        # one route contains n-1 paths
        self.update_pheromone(route) #update for all paths

        return route


    ######################### select the next city/path #########################
    '''
        - ant is currently at city "current_city". it has to go to one of its neighbours.
        - neighbours = list of unvisited neighbour
        - the probability of selecting a neighbour as the next city to visit depends on its f value
        '''

    def select_next_city(self, current_city, neighbours):
        m = len(neighbours) #tot no. of unvisited neighbours

        ##### Step 1: calculate f values for each neighbour #####
        f_values = [] #same order as neighbours list

        for nbr in neighbours:
            # path = edge btw current_city and nbr
            h = self.pheromone[current_city.index][nbr.index] #pheromone
            d = self.tsp.distance_btw(current_city, nbr) #path length
            g = 1/d
            f = (h ** self.alpha)*(g ** self.beta)

            f_values.append(f)

        ##### Step 2: calculate probabilities for all neighbours #####
            # prob of nbr1 = f1/(f1 + f2 + .. fm)
            # where f1 = f val of nbr1
        f_values = np.array(f_values) #convert to array
        probabilities = f_values/f_values.sum()

        ##### Step 3: select next city based on f values #####
        next_city = np.random.choice(list(neighbours), p=probabilities)
        return next_city
        #index = np.random.choice(m, p=probabilities)
        #return list(neighbours)[index]


    ######################### update pheromone on path #########################
    def update_pheromone(self, route):
        dist = self.tsp.cost(route) #tot distance of the route

        #for each path (i,j) in the route
        for c in range(self.tsp.n - 1):
            #cities c1 and c2
            c1, c2 = route[c], route[c+1]
            i, j = c1.index, c2.index #indices a/c to TSP

            #calculate h (pheromone amt)
            h_old = self.pheromone[i][j]
            h_new = h_old*(1-self.rho) + (self.rho/dist)
                # rho/dist = amt of pheromone evaporated per unit time per unit length (dist)

            #update pheromone amt
            self.pheromone[i][j] = h_new
            self.pheromone[j][i] = h_new


