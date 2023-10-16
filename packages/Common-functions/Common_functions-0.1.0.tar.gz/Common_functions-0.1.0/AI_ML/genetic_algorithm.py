import random

def create_population(population_size, chromosome_length):
    # Create a random population of individuals
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(chromosome_length)]
        population.append(individual)
    return population

def fitness_function(individual):
    # Calculate the fitness value of an individual
    # Return a higher value for fitter individuals
    # You can customize this function based on your problem domain
    # Example: Fitness function for maximizing the number of ones in the chromosome
    return sum(individual)

def selection(population):
    # Perform selection to choose parents for reproduction
    # You can use different selection strategies like roulette wheel selection or tournament selection
    # For simplicity, we will use roulette wheel selection in this example
    total_fitness = sum(fitness_function(individual) for individual in population)
    probabilities = [fitness_function(individual) / total_fitness for individual in population]
    parents = random.choices(population, weights=probabilities, k=len(population))
    return parents

def crossover(parent1, parent2):
    # Perform crossover between two parents to create offspring
    # You can use different crossover techniques like one-point crossover or uniform crossover
    # For simplicity, we will use one-point crossover in this example
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutation(individual, mutation_rate):
    # Perform mutation on an individual
    # You can use different mutation techniques like bit flip or swap mutation
    # For simplicity, we will use bit flip mutation in this example
    mutated_individual = individual.copy()
    for i in range(len(mutated_individual)):
        if random.random() < mutation_rate:
            mutated_individual[i] = 1 - mutated_individual[i]
    return mutated_individual

def genetic_algorithm(population_size, chromosome_length, generations, mutation_rate):
    population = create_population(population_size, chromosome_length)

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
