import random
import numpy as np
import time
import matplotlib.pyplot as plt
from .base import Individual, Evolution

class TSP(Individual):
    """
    Implementation of Individual for the Travelling Salesman Problem.
    
    The value is a permutation of city indices representing a route.
    """
    def pair(self, other, pair_params):
        """
        Ordered crossover with set optimization for TSP routes.
        
        Args:
            other: Another TSP individual to pair with
            pair_params: Dictionary with 'alpha' parameter for crossover point
            
        Returns:
            A new TSP individual
        """
        size = len(self.value)
        start, end = sorted(random.sample(range(size), 2))
        
        # Get segment from first parent
        child_p1 = self.value[start:end].copy()
        child_p1_set = set(child_p1)
        
        # Get remaining elements in order from second parent
        child_p2 = [city for city in other.value if city not in child_p1_set]
        
        # Combine segments
        child = np.array(child_p2[:start] + child_p1.tolist() + child_p2[start:])
        
        return TSP(child)

    def mutate(self, mutate_params):
        """
        Swap two cities with probability based on mutation rate.
        
        Args:
            mutate_params: Dictionary with 'rate' parameter for mutation probability
            
        Returns:
            Boolean indicating whether mutation occurred
        """
        if random.random() < mutate_params['rate']:
            i, j = random.sample(range(len(self.value)), 2)
            self.value[i], self.value[j] = self.value[j], self.value[i]
            return True
        return False

    def _random_init(self, init_params):
        """
        Create a random permutation of city indices.
        
        Args:
            init_params: Dictionary with 'n_cities' parameter
            
        Returns:
            Random permutation of city indices
        """
        return np.random.permutation(init_params['n_cities'])


def run_tsp_evolution(cities, city_names=None, population_size=100, 
                      tournament_size=5, mutation_rate=0.01, n_offsprings=30,
                      n_epochs=500, crossover_alpha=0.5, verbose=True):
    """
    Run the TSP evolutionary algorithm.
    
    Args:
        cities: List of (x, y) coordinates for each city
        city_names: Optional list of names for cities
        population_size: Size of population
        tournament_size: Number of individuals in tournament selection
        mutation_rate: Probability of mutation
        n_offsprings: Number of offspring per generation
        n_epochs: Number of generations
        crossover_alpha: Parameter for crossover point
        verbose: Whether to print progress
        
    Returns:
        Dictionary with results of evolution
    """
    from ..utils.metrics import calculate_distances, tsp_fitness_creator
    from ..utils.visualization import plot_route, get_route_length
    
    n_cities = len(cities)
    
    if city_names is None:
        city_names = [str(i) for i in range(n_cities)]
    
    if verbose:
        print("\n=== Evolutionary Algorithm for TSP ===")
        print(f"Parameters:")
        print(f"- Population Size: {population_size}")
        print(f"- Tournament Size: {tournament_size}")
        print(f"- Mutation Rate: {mutation_rate}")
        print(f"- Number of Epochs: {n_epochs}")
        print(f"- Number of Cities: {n_cities}")
    
    # Calculate distances
    start_time = time.time()
    distances = calculate_distances(cities)
    
    # Create fitness function
    fitness = tsp_fitness_creator(distances)
    
    # Initialize evolution
    evo = Evolution(
        pool_size=population_size, 
        fitness=fitness, 
        individual_class=TSP, 
        n_offsprings=n_offsprings,
        pair_params={'alpha': crossover_alpha},
        mutate_params={'rate': mutation_rate},
        init_params={'n_cities': n_cities},
        tournament_size=tournament_size
    )
    
    init_time = time.time() - start_time
    if verbose:
        print(f"\nInitialization completed in {init_time:.4f} seconds")
    
    # Get initial best route
    best_individual = evo.pool.get_best_individual()
    best_route = best_individual.value
    initial_length = -evo.pool.fitness(best_individual)
    
    if verbose:
        print(f"Initial best route length: {initial_length:.2f}")
    
    # Track metrics
    best_lengths = [initial_length]
    improvements = 0
    last_improvement = 0
    total_mutations = 0
    
    evolution_start_time = time.time()
    
    if verbose:
        print("\nStarting evolution...")
        print(f"{'Epoch':>5} | {'Length':>10} | {'Mutations':>9} | {'Time (s)':>8} | {'Improved':>8}")
        print("-" * 55)
    
    # Run evolution
    for epoch in range(n_epochs):
        epoch_start = time.time()
        
        # Take evolution step and track mutations
        mutations = evo.step()
        total_mutations += mutations
        
        # Get current best
        current_best = evo.pool.get_best_individual()
        current_length = -evo.pool.fitness(current_best)
        best_lengths.append(current_length)
        
        # Check if improved
        improved = ""
        if current_length < best_lengths[-2]:
            improvements += 1
            last_improvement = epoch
            best_route = current_best.value.copy()
            improved = "✓"
        
        epoch_time = time.time() - epoch_start
        
        # Log progress
        if verbose and (epoch % 10 == 0 or improved):
            print(f"{epoch:5d} | {current_length:10.2f} | {mutations:9d} | {epoch_time:8.4f} | {improved:8}")
    
    total_time = time.time() - evolution_start_time
    final_length = best_lengths[-1]
    improvement_pct = ((initial_length - final_length) / initial_length) * 100
    
    if verbose:
        print("\n=== Evolution Complete ===")
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Initial length: {initial_length:.2f}")
        print(f"Final length: {final_length:.2f}")
        print(f"Improvement: {improvement_pct:.2f}%")
        print(f"Number of improvements: {improvements}")
        print(f"Last improvement at epoch: {last_improvement}")
        print(f"Stagnant epochs: {n_epochs - last_improvement - 1}")
        print(f"Total mutations: {total_mutations}")
        print(f"Average mutations per epoch: {total_mutations / n_epochs:.2f}")
    
    # Save final route to results directory
    plt.figure(figsize=(12, 8))
    plot_route(cities, best_route, city_names, 
                title=f"Best Route (Length: {final_length:.2f})")
    plt.savefig('results/tsp_final_route.png')
    plt.close()
    
    # Save length history to results directory
    plt.figure(figsize=(12, 6))
    plt.plot(best_lengths, 'b-')
    plt.title('Route Length over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Route Length (shorter is better)')
    plt.grid(True, alpha=0.3)
    plt.savefig('results/tsp_length_history.png')
    plt.close()
    
    # Create a fresh figure for display
    plt.figure(figsize=(12, 8))
    plot_route(cities, best_route, city_names, 
                title=f"Best Route (Length: {final_length:.2f})")
    
    return {
        'best_route': best_route,
        'best_length': final_length,
        'improvement': improvement_pct,
        'length_history': best_lengths,
        'runtime': total_time,
        'improvements': improvements,
        'last_improvement': last_improvement,
        'total_mutations': total_mutations
    }