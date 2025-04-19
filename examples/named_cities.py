import time
import sys
import pathlib
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the package
parent_dir = str(pathlib.Path(__file__).parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.algorithms.tsp import run_tsp_evolution
from src.utils.visualization import plot_convergence
from src.utils.config import load_config, ensure_results_dir

def main():
    """Run the TSP algorithm with named cities."""
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
    
    print("\n=== TSP Evolutionary Algorithm with Named Cities ===")
    print(f"Running with {len(city_names)} cities (A-T)...")
    
    # Record start time
    start_time = time.time()
    
    # Run the algorithm
    result = run_tsp_evolution(
        cities=city_coords,
        city_names=city_names,
        population_size=algorithm['population_size'],
        tournament_size=algorithm['tournament_size'],
        mutation_rate=algorithm['mutation_rate'],
        n_offsprings=algorithm['n_offsprings'],
        n_epochs=algorithm['n_epochs'],
        verbose=algorithm['verbose']
    )
    
    # Calculate total runtime
    total_time = time.time() - start_time
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total runtime: {total_time:.2f} seconds")
    print(f"Best route length: {result['best_length']:.2f}")
    print(f"Improvement: {result['improvement']:.2f}%")
    print(f"Best route: {' -> '.join([city_names[city] for city in result['best_route']])}")
    print(f"\nAll visualizations have been saved to the '{output['results_dir']}' directory.")
    
    # Plot length history separately to ensure it displays
    if output['show_plots']:
        plot_convergence(
            result['length_history'], 
            title='Route Length over Epochs', 
            save_path=f"{output['results_dir']}/named_cities_convergence.png"
        )
    
    # Keep the plot window open if configured to show plots
    if output['show_plots']:
        plt.show()

if __name__ == "__main__":
    main()