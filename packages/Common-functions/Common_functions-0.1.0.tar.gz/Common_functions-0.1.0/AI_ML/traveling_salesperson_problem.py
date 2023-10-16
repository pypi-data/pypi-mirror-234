import itertools

def tsp(cities, start_city):
    num_cities = len(cities)
    all_cities = set(range(num_cities))
    best_path = None
    best_distance = float('inf')

    for perm in itertools.permutations(all_cities - {start_city}):
        current_path = [start_city] + list(perm) + [start_city]
        current_distance = calculate_distance(cities, current_path)

        if current_distance < best_distance:
            best_distance = current_distance
            best_path = current_path

    return best_path, best_distance

def calculate_distance(cities, path):
    distance = 0
    num_cities = len(cities)

    for i in range(num_cities - 1):
        start_city = path[i]
        end_city = path[i + 1]
        distance += cities[start_city][end_city]

    return distance
