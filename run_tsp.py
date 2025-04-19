# run_tsp.py
# Runner script for TSP evolutionary algorithm examples with customizable parameters

import os
import sys
import importlib
import json
import numpy as np
import matplotlib.pyplot as plt
import time

# Ensure src is in the path
sys.path.insert(0, os.path.abspath('.'))

from src.algorithms.tsp import run_tsp_evolution
from src.utils.visualization import plot_convergence

def create_default_config():
    """Create a default configuration file if it doesn't exist"""
    config = {
        "cities": {
            "named_cities": {
                "city_names": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
                             "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
                "coordinates": [
                    [60, 200], [180, 200], [80, 180], [140, 180], [20, 160],
                    [100, 160], [200, 160], [140, 140], [40, 120], [100, 120],
                    [180, 100], [60, 80], [120, 80], [180, 60], [20, 40],
                    [100, 40], [200, 40], [20, 20], [60, 20], [160, 20]
                ]
            },
            "random_cities": {
                "count": 20,
                "min_x": 0,
                "max_x": 200,
                "min_y": 0,
                "max_y": 200
            }
        },
        "algorithm": {
            "population_size": 100,
            "tournament_size": 5,
            "mutation_rate": 0.01,
            "n_epochs": 500,
            "verbose": True
        }
    }
    
    with open('tsp_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Created default configuration file: tsp_config.json")
    return config

def load_config():
    """Load configuration from file or create default"""
    if not os.path.exists('tsp_config.json'):
        return create_default_config()
    
    try:
        with open('tsp_config.json', 'r') as f:
            config = json.load(f)
        print("Loaded configuration from tsp_config.json")
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return create_default_config()

def generate_random_cities(config):
    """Generate random cities based on configuration"""
    random_config = config['cities']['random_cities']
    count = random_config['count']
    min_x = random_config['min_x']
    max_x = random_config['max_x']
    min_y = random_config['min_y']
    max_y = random_config['max_y']
    
    # Generate random coordinates
    x_coords = np.random.uniform(min_x, max_x, count)
    y_coords = np.random.uniform(min_y, max_y, count)
    
    # Create city names
    city_names = [f"City_{i+1}" for i in range(count)]
    
    # Combine into coordinates
    coordinates = list(zip(x_coords, y_coords))
    
    return city_names, coordinates

def run_named_cities(config):
    """Run TSP with named cities from configuration"""
    print("\n=== Running TSP with Named Cities ===")
    
    # Get city data
    named_config = config['cities']['named_cities']
    city_names = named_config['city_names']
    coordinates = named_config['coordinates']
    
    # Get algorithm parameters
    algorithm_config = config['algorithm']
    
    print(f"Running with {len(city_names)} cities...")
    
    # Run algorithm
    result = run_tsp_evolution(
        cities=coordinates,
        city_names=city_names,
        population_size=algorithm_config['population_size'],
        tournament_size=algorithm_config['tournament_size'],
        mutation_rate=algorithm_config['mutation_rate'],
        n_epochs=algorithm_config['n_epochs'],
        verbose=algorithm_config['verbose']
    )
    
    # Print best route
    print("\n=== Final Route ===")
    print(" -> ".join([city_names[city] for city in result['best_route']]))
    
    # Display plots
    plt.show()

def run_random_cities(config):
    """Run TSP with randomly generated cities"""
    print("\n=== Running TSP with Random Cities ===")
    
    # Generate random cities
    city_names, coordinates = generate_random_cities(config)
    
    # Get algorithm parameters
    algorithm_config = config['algorithm']
    
    print(f"Running with {len(city_names)} random cities...")
    
    # Run algorithm
    result = run_tsp_evolution(
        cities=coordinates,
        city_names=city_names,
        population_size=algorithm_config['population_size'],
        tournament_size=algorithm_config['tournament_size'],
        mutation_rate=algorithm_config['mutation_rate'],
        n_epochs=algorithm_config['n_epochs'],
        verbose=algorithm_config['verbose']
    )
    
    # Print summary
    print("\n=== Final Route ===")
    print(" -> ".join([city_names[city] for city in result['best_route']]))
    
    # Display plots
    plt.show()

def run_example(example_name):
    """Run a specific example from the examples directory"""
    try:
        print(f"\nRunning example: {example_name}.py")
        
        # Import the example module
        module_name = f"examples.{example_name}"
        module = importlib.import_module(module_name)
        
        # Run the main function if it exists
        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"Error: No main function found in {module_name}")
    except ModuleNotFoundError:
        print(f"Error: Example '{example_name}' not found.")
    except Exception as e:
        print(f"Error running example: {e}")
        import traceback
        traceback.print_exc()

def modify_config(config):
    """Allow user to modify configuration"""
    print("\n=== Modify Configuration ===")
    
    # Algorithm parameters
    algorithm = config['algorithm']
    print("\nAlgorithm Parameters:")
    
    try:
        algorithm['population_size'] = int(input(f"Population size [{algorithm['population_size']}]: ") or algorithm['population_size'])
        algorithm['tournament_size'] = int(input(f"Tournament size [{algorithm['tournament_size']}]: ") or algorithm['tournament_size'])
        algorithm['mutation_rate'] = float(input(f"Mutation rate [{algorithm['mutation_rate']}]: ") or algorithm['mutation_rate'])
        algorithm['n_epochs'] = int(input(f"Number of epochs [{algorithm['n_epochs']}]: ") or algorithm['n_epochs'])
    except ValueError as e:
        print(f"Invalid input: {e}. Using previous values.")
    
    # Random cities configuration
    random_cities = config['cities']['random_cities']
    print("\nRandom Cities Generation:")
    
    try:
        random_cities['count'] = int(input(f"Number of cities [{random_cities['count']}]: ") or random_cities['count'])
        random_cities['min_x'] = float(input(f"Min X [{random_cities['min_x']}]: ") or random_cities['min_x'])
        random_cities['max_x'] = float(input(f"Max X [{random_cities['max_x']}]: ") or random_cities['max_x'])
        random_cities['min_y'] = float(input(f"Min Y [{random_cities['min_y']}]: ") or random_cities['min_y'])
        random_cities['max_y'] = float(input(f"Max Y [{random_cities['max_y']}]: ") or random_cities['max_y'])
    except ValueError as e:
        print(f"Invalid input: {e}. Using previous values.")
    
    # Save updated configuration
    with open('tsp_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Configuration updated and saved to tsp_config.json")
    return config

def main():
    """Main function to run the TSP examples"""
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Load configuration
    config = load_config()
    
    while True:
        print("\n=== TSP Evolutionary Algorithm Runner ===")
        print("1. Run with named cities (A-T)")
        print("2. Run with random cities")
        print("3. Run named_cities.py example")
        print("4. Run parameter_comparison.py example")
        print("5. Run simple_tsp.py example")
        print("6. Modify configuration")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == '1':
            run_named_cities(config)
        elif choice == '2':
            run_random_cities(config)
        elif choice == '3':
            run_example('named_cities')
        elif choice == '4':
            run_example('parameter_comparison')
        elif choice == '5':
            run_example('simple_tsp')
        elif choice == '6':
            config = modify_config(config)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()