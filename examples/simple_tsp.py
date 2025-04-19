import sys
import pathlib
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the package
parent_dir = str(pathlib.Path(__file__).parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.algorithms.tsp import run_tsp_evolution
from src.utils.config import load_config, ensure_results_dir

def main():
    """Run a simple TSP example without extensive plotting"""
    # Load configuration
    config = load_config()
    ensure_results_dir(config)
    
    # Get city data from config
    city_data = config['cities']['named_cities']
    city_names = city_data['city_names']
    city_coords = city_data['coordinates']
    
    # Get algorithm parameters from config
    algorithm = config['algorithm']
    output = config['output']
    
    print("\n=== Simple TSP Example ===")
    
    # Run the TSP algorithm
    result = run_tsp_evolution(
        cities=city_coords,
        city_names=city_names,
        population_size=algorithm['population_size'],
        tournament_size=algorithm['tournament_size'],
        mutation_rate=algorithm['mutation_rate'],
        n_epochs=algorithm['n_epochs'],
        verbose=algorithm['verbose']
    )
    
    # Print final results
    print("\n=== Final Results ===")
    print(f"Best route length: {result['best_length']:.2f}")
    print(f"Improvement: {result['improvement']:.2f}%")
    print(f"Total mutations: {result['total_mutations']}")
    print(f"Number of improvements: {result['improvements']}")
    print(f"Last improvement at epoch: {result['last_improvement']}")
    
    # Display the best route visualization if configured to show plots
    if output['show_plots']:
        plt.show()

if __name__ == "__main__":
    main()