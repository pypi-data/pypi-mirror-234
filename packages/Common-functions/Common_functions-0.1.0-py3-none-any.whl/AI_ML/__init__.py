import heapq
from tkinter import *
from tkinter import messagebox
import random
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from gtts import gTTS
from playsound import playsound 
from sklearn import datasets
from sklearn.model_selection import train_test_split
import os

import warnings

warnings.filterwarnings("ignore")

class LocalRegression:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def local_regression(self, x0, tau):
        x0 = [1, x0]
        X = [[1, i] for i in self.X]
        X = np.asarray(X)
        xw = (X.T) * np.exp(np.sum((X - x0) ** 2, axis=1) / (-2 * tau))
        beta = np.linalg.pinv(xw @ X) @ xw @ self.Y @ x0
        return beta

    def draw(self, domain, taus):
        plt.plot(self.X, self.Y, 'o', color='black')
        for tau in taus:
            prediction = [self.local_regression(x0, tau) for x0 in domain]
            plt.plot(domain, prediction, label=f'tau={tau}')
        plt.legend()
        plt.show()

def weighted():
    X = np.linspace(-3, 3, num=1000)
    domain = X
    Y = np.log(np.abs(X**2 - 1) + 0.5)
    local_reg = LocalRegression(X, Y)
    tau_input = input("Enter tau values separated by spaces: ")
    taus = [float(tau) for tau in tau_input.split()]
    local_reg.draw(domain, taus)


class KNNClassifier:
    def __init__(self, k=1):
        self.k = k
        self.classifier = KNeighborsClassifier(n_neighbors=k)
        self.iris = datasets.load_iris()
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.iris.data, self.iris.target, test_size=0.1)

    def train_and_predict(self):
        self.classifier.fit(self.x_train, self.y_train)
        y_pred = self.classifier.predict(self.x_test)

        print("Results of classification using k-NN with k={}".format(self.k))
        for r in range(len(self.x_test)):
            print("Sample:", str(self.x_test[r]), "Actual-label:", str(self.y_test[r]), "Predicted-label:", str(y_pred[r]))
        print("Classification Accuracy:", self.classifier.score(self.x_test, self.y_test))

def K_Nearest():
    k = int(input("Enter the value of k for K-NN: "))
    knn_classifier = KNNClassifier(k)
    knn_classifier.train_and_predict()

def is_prime():
    number = int(input("Enter a number: "))

    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def factorial():
    number = int(input("Enter a number: "))

    if number == 0:
        return 1
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result

#simple calculator
def Calculator():
    print("choose operation:")
    temp=0
    print("""
    1. add
    2. Sub
    3. multiply
    4. divide""")
    opr=[(lambda a,b:a+b),(lambda a,b:a-b),(lambda a,b:a*b),(lambda a,b:a/b)]
    opt=int(input())
    
    a=int(input("Enter the value of a:"))
    b=int(input("Enter the value of b:"))
    res=opr[opt-1](a,b)
    print("Answer = ",res)

    

def bfs():
    graph = {}
    num_nodes = int(input("Enter the number of nodes: "))
    for i in range(num_nodes):
        node = input("Enter the node: ")
        neighbors = input(f"Enter the neighbors of node {node} (space-separated): ").split()
        graph[node] = neighbors

    start_node = input("Enter the start node: ")

    visited = set()
    queue = [start_node]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node])
    return visited

def dfs():
    graph = {}
    num_nodes = int(input("Enter the number of nodes: "))
    for i in range(num_nodes):
        node = input("Enter the node: ")
        neighbors = input(f"Enter the neighbors of node {node} (space-separated): ").split()
        graph[node] = neighbors

    start_node = input("Enter the start node: ")

    visited = set()
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            stack.extend(graph[node])
    return visited

def water_jug_problem():
    jug1_capacity = int(input("Enter the capacity of jug 1: "))
    jug2_capacity = int(input("Enter the capacity of jug 2: "))
    target = int(input("Enter the target amount: "))

    jug1 = 0
    jug2 = 0
    steps = []
    while jug1 != target and jug2 != target:
        if jug1 == 0:
            jug1 = jug1_capacity
            steps.append((jug1, jug2))
        elif jug2 == jug2_capacity:
            jug2 = 0
            steps.append((jug1, jug2))
        else:
            amount = min(jug1, jug2_capacity - jug2)
            jug1 -= amount
            jug2 += amount
            steps.append((jug1, jug2))
    return steps

class TicTacToe:
    def __init__(self):
        self.Player1 = 'X'
        self.stop_game = False

        self.b = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.states = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        self.root = Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(0, 0)

        for i in range(3):
            for j in range(3):
                self.b[i][j] = Button(
                    self.root,
                    height=4, width=8,
                    font=("Helvetica", "20"),
                    command=lambda r=i, c=j: self.clicked(r, c)
                )
                self.b[i][j].grid(row=i, column=j)

        self.root.mainloop()

    def clicked(self, r, c):
        if self.Player1 == "X" and self.states[r][c] == 0 and self.stop_game == False:
            self.b[r][c].configure(text="X")
            self.states[r][c] = 'X'
            self.Player1 = 'O'
        elif self.Player1 == 'O' and self.states[r][c] == 0 and self.stop_game == False:
            self.b[r][c].configure(text='O')
            self.states[r][c] = 'O'
            self.Player1 = 'X'

        self.check_if_win()

    def check_if_win(self):
        for i in range(3):
            if self.states[i][0] == self.states[i][1] == self.states[i][2] != 0:
                self.stop_game = True
                winner = messagebox.showinfo("Winner", self.states[i][0] + " Won")
                break
            elif self.states[0][i] == self.states[1][i] == self.states[2][i] != 0:
                self.stop_game = True
                winner = messagebox.showinfo("Winner", self.states[0][i] + " Won!")
                break
            elif self.states[0][0] == self.states[1][1] == self.states[2][2] != 0:
                self.stop_game = True
                winner = messagebox.showinfo("Winner", self.states[0][0] + " Won!")
                break
            elif self.states[0][2] == self.states[1][1] == self.states[2][0] != 0:
                self.stop_game = True
                winner = messagebox.showinfo("Winner", self.states[0][2] + " Won!")
                break
            elif all(self.states[row][col] != 0 for row in range(3) for col in range(3)):
                self.stop_game = True
                winner = messagebox.showinfo("Tie", "It's a tie")
                break

def start_tic_tac_toe():
    game=TicTacToe()



class Graph:
    def __init__(self):
        self.graph = {}

    def create_graph_from_input(self):
        num_nodes = int(input("Enter the number of nodes: "))
        for i in range(num_nodes):
            node = input("Enter the node: ")
            neighbors = input(f"Enter the neighbors of node {node} (space-separated): ").split()
            edges = []
            for neighbor in neighbors:
                edge_cost = float(input(f"Enter the cost of the edge between {node} and {neighbor}: "))
                edges.append((neighbor, edge_cost))
            self.graph[node] = edges
        return self.graph

def uniform_cost_search():
    graph = Graph().create_graph_from_input()
    start = input("Enter the start node: ")
    goal = input("Enter the goal node: ")
    visited = set()
    queue = [(0, start)]
    while queue:
        cost, node = heapq.heappop(queue)
        if node == goal:
            return True
        if node not in visited:
            visited.add(node)
            neighbors = graph[node]
            for neighbor, edge_cost in neighbors:
                heapq.heappush(queue, (cost + edge_cost, neighbor))
    return False

def iterative_deepening_search():
    graph = Graph().create_graph_from_input()
    start = input("Enter the start node: ")
    goal = input("Enter the goal node: ")
    max_depth = int(input("Enter the maximum depth: "))
    
    def depth_limited_search(graph, node, goal, depth):
        if node == goal:
            return True
        if depth == 0:
            return False
        for neighbor in graph[node]:
            if depth_limited_search(graph, neighbor, goal, depth - 1):
                return True
        return False

    for depth in range(max_depth):
        if depth_limited_search(graph, start, goal, depth):
            return True
    return False


#genetic algorithm
def genetic_algorithm():
    def mutation(individual, mutation_rate):
        # Perform mutation on an individual
        # Return the mutated individual
        mutated_individual = []
        for gene in individual:
            if random.random() < mutation_rate:  # Randomly mutate genes based on mutation rate
                mutated_gene = 1 - gene  # Flip the gene (0 to 1 or 1 to 0)
            else:
                mutated_gene = gene
            mutated_individual.append(mutated_gene)
        return mutated_individual

    def crossover(parent1, parent2):
        # Perform crossover between two parents to create offspring
        # Return the offspring
        crossover_point = random.randint(1, len(parent1) - 1)  # Randomly choose a crossover point
        offspring = parent1[:crossover_point] + parent2[crossover_point:]  # Combine parent genes
        return offspring

    def fitness_function(individual):
        # Calculate the fitness value of an individual
        # Return a higher value for fitter individuals
        fitness = sum(individual)  # Fitness is the sum of the genes in the individual
        return fitness

    def selection(population):
        # Perform selection to choose parents for reproduction
        # Return the selected parents
        selected_parents = random.choices(population, k=2)  # Randomly select 2 parents
        return selected_parents
    
    def create_population(population_size, chromosome_length):
            # Create a random population of individuals
            population = []
            for _ in range(population_size):
                individual = [random.randint(0, 1) for _ in range(chromosome_length)]
                population.append(individual)
            return population
    
    population_size = int(input("Enter the population size: "))
    chromosome_length = int(input("Enter the chromosome length: "))
    generations = int(input("Enter the number of generations: "))
    mutation_rate = float(input("Enter the mutation rate: "))


    population = create_population(population_size, chromosome_length)
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(chromosome_length)]
        population.append(individual)

    for _ in range(generations):
        # Evaluate the fitness of each individual
        fitness_values = [fitness_function(individual) for individual in population]

        # Perform selection
        parents = selection(population)

        # Create the next generation through crossover and mutation
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = random.choices(parents, k=2)
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            offspring.append(child)

        # Replace the current population with the offspring
        population = offspring

    # Find the best individual in the final population
    best_individual = max(population, key=fitness_function)
    return best_individual


# 17. Hill Climbing
def hill_climbing():
    def get_neighbors(state):
        # Generate neighboring states by flipping a single bit in the current state
        neighbors = []
        for i in range(len(state)):
            neighbor = state.copy()
            neighbor[i] = 1 - neighbor[i]  # Flip the bit
            neighbors.append(neighbor)
        return neighbors

    initial_state = list(map(int, input("Enter the initial state (space-separated 0s and 1s): ").split()))

    def evaluate(state):
        # Evaluate the current state and return a score
        # Higher score indicates a better state
        # Replace this with your own evaluation function
        return sum(state)

    current_state = initial_state

    while True:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_score = evaluate(current_state)

        for neighbor in neighbors:
            neighbor_score = evaluate(neighbor)
            if neighbor_score > best_score:
                best_neighbor = neighbor
                best_score = neighbor_score

        if best_neighbor is None:
            return current_state

        current_state = best_neighbor



# 18. Neural Network

class NeuralNetwork:
    def __init__(self, num_inputs, num_hidden, num_outputs):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs

        self.hidden_layer = np.random.randn(num_hidden, num_inputs + 1)
        self.output_layer = np.random.randn(num_outputs, num_hidden + 1)

    def forward_propagation(self, inputs):
        inputs = np.append(inputs, 1)  # Add bias term
        hidden_activations = self.hidden_layer @ inputs
        hidden_outputs = self.sigmoid(hidden_activations)

        hidden_outputs = np.append(hidden_outputs, 1)  # Add bias term
        output_activations = self.output_layer @ hidden_outputs
        output_outputs = self.sigmoid(output_activations)

        return output_outputs

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def train(self, inputs, targets, learning_rate, epochs):
        for epoch in range(epochs):
            for i in range(len(inputs)):
                x = inputs[i]
                target = targets[i]

                # Forward propagation
                inputs_with_bias = np.append(x, 1)  # Add bias term
                hidden_activations = self.hidden_layer @ inputs_with_bias
                hidden_outputs = self.sigmoid(hidden_activations)

                hidden_outputs_with_bias = np.append(hidden_outputs, 1)  # Add bias term
                output_activations = self.output_layer @ hidden_outputs_with_bias
                output_outputs = self.sigmoid(output_activations)

                # Backpropagation
                output_errors = target - output_outputs
                output_delta = output_errors * output_outputs * (1 - output_outputs)

                hidden_errors = self.output_layer.T @ output_delta
                hidden_delta = hidden_errors * hidden_outputs * (1 - hidden_outputs)

                # Update weights
                self.output_layer += learning_rate * np.outer(output_delta, hidden_outputs_with_bias)
                self.hidden_layer += learning_rate * np.outer(hidden_delta, inputs_with_bias)
def implement_neural_network():
    num_inputs = int(input("Enter the number of inputs: "))
    num_hidden = int(input("Enter the number of hidden units: "))
    num_outputs = int(input("Enter the number of outputs: "))

    neural_network = NeuralNetwork(num_inputs, num_hidden, num_outputs)

    inputs = []
    targets = []
    num_samples = int(input("Enter the number of training samples: "))
    for _ in range(num_samples):
        input_data = list(map(float, input("Enter the input data (space-separated): ").split()))
        target_data = list(map(float, input("Enter the target data (space-separated): ").split()))
        inputs.append(input_data)
        targets.append(target_data)

    learning_rate = float(input("Enter the learning rate: "))
    epochs = int(input("Enter the number of epochs: "))

    neural_network.train(inputs, targets, learning_rate, epochs)

    while True:
        test_input = list(map(float, input("Enter the test input data (space-separated): ").split()))
        output = neural_network.forward_propagation(test_input)
        print("Output:", output)

        choice = input("Do you want to continue testing? (y/n): ")
        if choice.lower() != 'y':
            break

# 19. Traveling Salesperson Problem

def tsp():
    num_cities = int(input("Enter the number of cities: "))
    start = int(input("Enter the starting city: "))
    
    # Input the graph distances
    graph = []
    for i in range(num_cities):
        row = list(map(float, input(f"Enter the distances from city {i} to other cities (space-separated): ").split()))
        graph.append(row)

    visited = [False] * num_cities
    visited[start] = True
    path = [start]
    total_distance = 0

    while len(path) < num_cities:
        current_city = path[-1]
        min_distance = float('inf')
        next_city = None

        for neighbor in range(num_cities):
            if not visited[neighbor] and graph[current_city][neighbor] < min_distance:
                min_distance = graph[current_city][neighbor]
                next_city = neighbor

        if next_city is None:
            return None

        path.append(next_city)
        visited[next_city] = True
        total_distance += min_distance

    path.append(start)
    total_distance += graph[path[-2]][path[-1]]

    return path, total_distance
class AStarSearch:
    def __init__(self):
        self.graph = {}
        self.heuristic_values = {}

    def aStarAlgo(self, start_node, stop_node):
        open_set = set([start_node])
        closed_set = set()
        g = {start_node: 0}
        parents = {start_node: start_node}

        while len(open_set) > 0:
            n = None
            for v in open_set:
                if n is None or g[v] + self.heuristic_values[v] < g[n] + self.heuristic_values[n]:
                    n = v

            if n == stop_node or n not in self.graph:
                pass
            else:
                for (m, weight) in self.get_neighbors(n):
                    if m not in open_set and m not in closed_set:
                        open_set.add(m)
                        parents[m] = n
                        g[m] = g[n] + weight
                    else:
                        if g[m] > g[n] + weight:
                            g[m] = g[n] + weight
                            parents[m] = n
                            if m in closed_set:
                                closed_set.remove(m)
                                open_set.add(m)

            if n is None:
                print('Path does not exist!')
                return None

            if n == stop_node:
                path = []
                while parents[n] != n:
                    path.append(n)
                    n = parents[n]
                path.append(start_node)
                path.reverse()
                print('Path found:', path)
                return path

            open_set.remove(n)
            closed_set.add(n)

        print('Path does not exist!')
        return None

    def get_neighbors(self, node):
        if node in self.graph:
            return self.graph[node]
        else:
            return []

def astar():
    astar_solver = AStarSearch()

    num_nodes = int(input("Enter the number of nodes in the graph: "))
    for i in range(num_nodes):
        node_name = input(f"Enter the name of node {i+1}: ")
        heuristic_value = int(input(f"Enter the heuristic value for node {node_name}: "))
        astar_solver.heuristic_values[node_name] = heuristic_value
        num_neighbors = int(input(f"Enter the number of neighbors for node {node_name}: "))
        neighbors = []
        for j in range(num_neighbors):
            neighbor_name, weight = input(f"Enter the name of neighbor {j+1} and its weight: ").split()
            weight = int(weight)
            neighbors.append((neighbor_name, weight))
        astar_solver.graph[node_name] = neighbors

    start_node = input("Enter the start node: ")
    goal_node = input("Enter the goal node: ")
    astar_solver.aStarAlgo(start_node, goal_node)

class MinimaxSolver:
    def __init__(self):
        self.values = []
        self.MAX = float('inf')
        self.MIN = float('-inf')

    def get_values(self):
        num_values = int(input("Enter the number of nodes:  "))
        for i in range(num_values):
            value = int(input(f"Enter value for node  {i + 1}: "))
            self.values.append(value)

    def minimax(self, depth, nodeIndex, maximizingPlayer, alpha, beta):
        if depth == 3:
            return self.values[nodeIndex]
        if maximizingPlayer:
            best = self.MIN
            for i in range(0, 2):
                val = self.minimax(depth + 1, nodeIndex * 2 + i, False, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = self.MAX
            for i in range(0, 2):
                val = self.minimax(depth + 1, nodeIndex * 2 + i, True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best

    def solve(self):
        alpha = self.MIN
        beta = self.MAX
        return self.minimax(0, 0, True, alpha, beta)

def Alphabeta():
    solver = MinimaxSolver()
    solver.get_values()
    print("The optimal value is:", solver.solve())



class AOStarSearch:
    def __init__(self):
        self.H_dist = {
            'A': -1,
            'B': 4,
            'C': 2,
            'D': 3,
            'E': 6,
            'F': 8,
            'G': 2,
            'H': 0,
            'I': 0,
            'J': 0
        }

        self.allNodes = {
            'A': {'AND': [('C', 'D')], 'OR': ['B']},
            'B': {'OR': ['E', 'F']},
            'C': {'OR': ['G'], 'AND': [('H', 'I')]},
            'D': {'OR': ['J']}
        }

        self.optimal_child_group = {}


    def recAOStar(self, n):
        and_nodes = []
        or_nodes = []
        if n in self.allNodes:
            if 'AND' in self.allNodes[n]:
                and_nodes = self.allNodes[n]['AND']
            if 'OR' in self.allNodes[n]:
                or_nodes = self.allNodes[n]['OR']
        if len(and_nodes) == 0 and len(or_nodes) == 0:
            return
        solvable = False
        marked = {}
        while not solvable:
            if len(marked) == len(and_nodes) + len(or_nodes):
                min_cost_least, min_cost_group_least = self.least_cost_group(and_nodes, or_nodes, marked)
                solvable = True
                self.change_heuristic(n, min_cost_least)
                self.optimal_child_group[n] = min_cost_group_least
                continue
            min_cost, min_cost_group = self.least_cost_group(and_nodes, or_nodes, marked)
            is_expanded = False
            if len(min_cost_group) > 1:
                if min_cost_group[0] in self.allNodes:
                    is_expanded = True
                    self.recAOStar(min_cost_group[0])
                if min_cost_group[1] in self.allNodes:
                    is_expanded = True
                    self.recAOStar(min_cost_group[1])
            else:
                if min_cost_group in self.allNodes:
                    is_expanded = True
                    self.recAOStar(min_cost_group)
            if is_expanded:
                min_cost_verify, min_cost_group_verify = self.least_cost_group(and_nodes, or_nodes, marked)
                if min_cost_group == min_cost_group_verify:
                    solvable = True
                    self.change_heuristic(n, min_cost_verify)
                    self.optimal_child_group[n] = min_cost_group
            else:
                solvable = True
                self.change_heuristic(n, min_cost)
                self.optimal_child_group[n] = min_cost_group
            marked[min_cost_group] = 1
        return self.heuristic(n)

    def least_cost_group(self, and_nodes, or_nodes, marked):
        node_wise_cost = {}
        for node_pair in and_nodes:
            if not node_pair[0] + node_pair[1] in marked:
                cost = 0
                cost = cost + self.heuristic(node_pair[0]) + self.heuristic(node_pair[1]) + 2
                node_wise_cost[node_pair[0] + node_pair[1]] = cost
        for node in or_nodes:
            if not node in marked:
                cost = 0
                cost = cost + self.heuristic(node) + 1
                node_wise_cost[node] = cost
        min_cost = 999999
        min_cost_group = None
        for costKey in node_wise_cost:
            if node_wise_cost[costKey] < min_cost:
                min_cost = node_wise_cost[costKey]
                min_cost_group = costKey
        return [min_cost, min_cost_group]

    def heuristic(self, n):
        return self.H_dist[n]

    def change_heuristic(self, n, cost):
        self.H_dist[n] = cost

    def print_path(self, node):
        print(self.optimal_child_group[node], end="")
        node = self.optimal_child_group[node]
        if len(node) > 1:
            if node[0] in self.optimal_child_group:
                print("->", end="")
                self.print_path(node[0])
            if node[1] in self.optimal_child_group:
                print("->", end="")
                self.print_path(node[1])
        else:
            if node in self.optimal_child_group:
                print("->", end="")
                self.print_path(node)

def AOstarseachfun():
    astar = AOStarSearch()
    print("Dist variable : ",astar.H_dist)
    print("All Nodes : ",astar.allNodes)
    optimal_cost = astar.recAOStar('A')
    print('Nodes which give optimal cost are:')
    astar.print_path('A')
    print('\nOptimal Cost is:', optimal_cost)





class NeuralNetwork:
    def __init__(self, input_neurons, hidden_neurons, output_neurons):
        self.input_neurons = input_neurons
        self.hidden_neurons = hidden_neurons
        self.output_neurons = output_neurons
        self.wh = np.random.uniform(size=(input_neurons, hidden_neurons))
        self.bh = np.random.uniform(size=(1, hidden_neurons))
        self.wout = np.random.uniform(size=(hidden_neurons, output_neurons))
        self.bout = np.random.uniform(size=(1, output_neurons))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def derivatives_sigmoid(self, x):
        return x * (1 - x)

    def train(self, X, y, learning_rate, epochs):
        for _ in range(epochs):
            hinp1 = np.dot(X, self.wh)
            hinp = hinp1 + self.bh
            hlayer_act = self.sigmoid(hinp)
            outinp1 = np.dot(hlayer_act, self.wout)
            outinp = outinp1 + self.bout
            output = self.sigmoid(outinp)

            EO = y - output
            outgrad = self.derivatives_sigmoid(output)
            d_output = EO * outgrad
            EH = d_output.dot(self.wout.T)
            hiddengrad = self.derivatives_sigmoid(hlayer_act)
            d_hiddenlayer = EH * hiddengrad

            self.wout += hlayer_act.T.dot(d_output) * learning_rate
            self.wh += X.T.dot(d_hiddenlayer) * learning_rate

    def predict(self, X):
        hinp1 = np.dot(X, self.wh)
        hinp = hinp1 + self.bh
        hlayer_act = self.sigmoid(hinp)
        outinp1 = np.dot(hlayer_act, self.wout)
        outinp = outinp1 + self.bout
        return self.sigmoid(outinp)

def BackPro():
    X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
    y = np.array(([92], [86], [89]), dtype=float)

    X = X / np.amax(X, axis=0)
    y = y / 100

    input_neurons = 2
    hidden_neurons = 3
    output_neurons = 1
    

    neural_net = NeuralNetwork(input_neurons, hidden_neurons, output_neurons)

    learning_rate = 0.1
    epochs = 7000
    print("Learning Rate : ",learning_rate)
    print("epochs : ",epochs)
    neural_net.train(X, y, learning_rate, epochs)

    predicted_output = neural_net.predict(X)

    print("Input: \n" + str(X))
    print("Actual Output: \n" + str(y))
    print("Predicted Output: \n", predicted_output)



class HeartDiseaseDiagnosis:
    def __init__(self, data_file='heart_disease_data.csv'):
        self.data = pd.read_csv(data_file)
        self.total_patients = len(self.data)
        self.total_heart_disease = sum(self.data['HeartDisease'])
        self.p_heart_disease = self.total_heart_disease / self.total_patients
        self.p_age_given_heart_disease = self.data.groupby('HeartDisease')['Age'].value_counts(normalize=True).unstack()
        self.p_gender_given_heart_disease = self.data.groupby('HeartDisease')['Gender'].value_counts(normalize=True).unstack()
        self.p_chest_pain_given_heart_disease = self.data.groupby('HeartDisease')['ChestPain'].value_counts(normalize=True).unstack()

    def calculate_probability(self, age, gender, chest_pain):
        p_diagnose_heart_disease = (
            self.p_age_given_heart_disease[age][1] *
            self.p_gender_given_heart_disease[gender][1] *
            self.p_chest_pain_given_heart_disease[chest_pain][1] *
            self.p_heart_disease
        )
        p_no_heart_disease = 1 - p_diagnose_heart_disease
        p_diagnose_heart_disease /= (p_diagnose_heart_disease + p_no_heart_disease)
        return p_diagnose_heart_disease, p_no_heart_disease

def Bayesian():
    heart_disease_diagnosis = HeartDiseaseDiagnosis()
    age = int(input("Enter age: "))
    gender = int(input("Enter gender (0 for female, 1 for male): "))
    chest_pain = int(input("Enter chest pain (0 for no, 1 for yes): "))

    p_diagnose_heart_disease, p_no_heart_disease = heart_disease_diagnosis.calculate_probability(age, gender, chest_pain)

    print("Bayesian network considering medical data")
    print("Probability of heart disease:", p_diagnose_heart_disease)
    print("Probability of no heart disease:", p_no_heart_disease)

# 20. Text-to-Speech Conversion

class ContextManager():
    def __init__(self,text):
        self.text=text
        self.filename="sound.mp3"
         
    def __enter__(self):
        tts = gTTS(text=self.text, lang='en')
        tts.save(self.filename)
        return self.filename

     
    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.remove(self.filename)
        
def text_to_speech():
    text=input("Enter the text to convert it to speech: ")
    with ContextManager(text) as manager:
        playsound("sound.mp3")





# 21. Classification with Multiple Classifiers
def train_classifiers():
    csv_file = input("Enter the path to the CSV file: ")
    data = pd.read_csv(csv_file)
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    classifiers = {
        'Random Forest': RandomForestClassifier(),
        'Decision Tree': DecisionTreeClassifier(),
        'K-Nearest Neighbors': KNeighborsClassifier(),
        'AdaBoost': AdaBoostClassifier(),
        'SGD': SGDClassifier(),
        'Extra Trees': ExtraTreesClassifier(),
        'Gaussian Naive Bayes': GaussianNB()
    }

    for name, classifier in classifiers.items():
        classifier.fit(X, y)
        predictions = classifier.predict(X)
        accuracy = accuracy_score(y, predictions)
        print(f"{name}: Accuracy = {accuracy:.2f}")


