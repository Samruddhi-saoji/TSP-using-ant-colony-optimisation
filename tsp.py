import numpy as np
import matplotlib.pyplot as plt #to plot the graph

#######################################################################
# cities = list of cities in the TSP
class TSP:
    #city = (x,y) point
    class City:
        def __init__(self, x, y, index, name) -> None:
            self.x = x
            self.y = y
            self.index = index #index of the city in the TSP city list
            self.name = name #name of the point

        #print(city) should print the name of the city
        def __repr__(self) -> str:
            return f"{self.name}"


    def __init__(self, n , city_list) -> None:
        self.n = n
        #city_list = [(x,y, name)]
        self.cities = [] #list of cities in the problem

        for c in city_list :
            x = c[0]
            y = c[1]
            index = c[2]
            name = c[3]
            self.cities.append(self.City(x,y,index, name))


    #return distance btw 2 cities
    def distance_btw(self, c1, c2):
        dist = np.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)
        return dist


    # route = list of cities in order of visit
    def cost(self, route) :
        dist = 0
        n = self.n
        for i in range(0, n-1) :
            #add distance btw city i and city i+1 to the total distance
            city1 = route[i]
            city2 = route[i+1]
            dist = dist + self.distance_btw(city1, city2)

        #now only distance btw last city and first city is left
        dist = dist + self.distance_btw(route[n-1] , route[0])
        return dist


    #plot the graph
    def display(self, route) :
        x_coord = []
        y_coord = []
        names = []

        #add each city's coordinates to the list, in sequence
        for city in route:
            x_coord.append(city.x)
            y_coord.append(city.y)
            names.append(city.name)

        #add the first city again at the end
        x_coord.append(route[0].x)
        y_coord.append(route[0].y)
        names.append(route[0].name)

        #scatter plot
        plt.scatter(x_coord, y_coord)

        #label all points
        for i in range(len(x_coord)):
            plt.annotate(names[i], (x_coord[i], y_coord[i] + 0.2))

        #connect the points with lines
        plt.plot(x_coord, y_coord)
        plt.show()