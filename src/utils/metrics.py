import numpy as np

def calculate_distances(cities):
    """
    Calculate the distance matrix between cities.
    
    Args:
        cities: List of (x, y) coordinates for each city
        
    Returns:
        Matrix of distances between each pair of cities
    """
    n_cities = len(cities)
    distances = np.zeros((n_cities, n_cities))
    
    for i in range(n_cities):
        for j in range(n_cities):
            if i != j:
                distances[i, j] = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
            
    return distances


def tsp_fitness_creator(distances):
    """
    Create a fitness function using a distance matrix.
    
    Args:
        distances: Matrix of distances between cities
        
    Returns:
        Function that calculates fitness of a TSP individual
    """
    def fitness(tsp):
        # Calculate the total route length (negative because we want to maximize fitness)
        route_length = 0
        for i in range(len(tsp.value)):
            from_city = tsp.value[i]
            to_city = tsp.value[(i + 1) % len(tsp.value)]  # Wrap around to the first city
            route_length += distances[from_city, to_city]
        return -route_length
    
    return fitness


def get_route_length(route, distances):
    """
    Calculate the total length of a route.
    
    Args:
        route: List of city indices representing a route
        distances: Matrix of distances between cities
        
    Returns:
        Total length of the route
    """
    length = 0
    for i in range(len(route)):
        from_city = route[i]
        to_city = route[(i + 1) % len(route)]
        length += distances[from_city, to_city]
    return length