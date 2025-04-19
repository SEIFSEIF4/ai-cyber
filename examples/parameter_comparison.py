import time
import sys
import pathlib
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import the package
parent_dir = str(pathlib.Path(__file__).parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.algorithms.tsp import run_tsp_evolution
from src.utils.visualization import plot_comparison
from src.utils.config import load_config, ensure_results_dir

def run_comparison():
    """Run comparison of different parameter settings"""
    # Load configuration
    config = load_config()
    ensure_results_dir(config)
    
    # Get city data from config
    city_data = config['cities']['named_cities']
    city_names = city_data['city_names']
    city_coords = city_data['coordinates']
    
    # Get output settings
    output = config['output']
    
    print("\n=== TSP Algorithm Parameter Comparison ===")
    
    # Get configurations to compare from config if available, or use defaults
    configs = config.get('parameter_comparison', [
        {
            "name": "Default",
            "population_size": 100,
            "tournament_size": 5,
            "mutation_rate": 0.01,
            "n_epochs": 300
        },
        {
            "name": "High Mutation",
            "population_size": 100,
            "tournament_size": 5,
            "mutation_rate": 0.05,
            "n_epochs": 300
        },
        {
            "name": "Large Population",
            "population_size": 200,
            "tournament_size": 5,
            "mutation_rate": 0.01,
            "n_epochs": 300
        },
        {
            "name": "Large Tournament",
            "population_size": 100,
            "tournament_size": 10,
            "mutation_rate": 0.01,
            "n_epochs": 300
        }
    ])
    
    results = []
    histories = {}
    
    for config_item in configs:
        print(f"\nRunning configuration: {config_item['name']}")
        print(f"- Population Size: {config_item['population_size']}")
        print(f"- Tournament Size: {config_item['tournament_size']}")
        print(f"- Mutation Rate: {config_item['mutation_rate']}")
        print(f"- Epochs: {config_item['n_epochs']}")
        
        # Run algorithm with current configuration
        start_time = time.time()
        result = run_tsp_evolution(
            cities=city_coords,
            city_names=city_names,
            population_size=config_item['population_size'],
            tournament_size=config_item['tournament_size'],
            mutation_rate=config_item['mutation_rate'],
            n_epochs=config_item['n_epochs'],
            verbose=False  # Disable verbose output for comparison
        )
        runtime = time.time() - start_time
        
        # Store results and length history
        results.append({
            "config": config_item,
            "best_length": result['best_length'],
            "improvement": result['improvement'],
            "runtime": runtime,
            "improvements": result['improvements'],
            "last_improvement": result['last_improvement']
        })
        
        histories[config_item['name']] = result['length_history']
        
        print(f"Completed in {runtime:.2f} seconds.")
        print(f"Best route length: {result['best_length']:.2f}")
        print(f"Improvement: {result['improvement']:.2f}%")
    
    # Compare results
    print("\n=== Comparison Results ===")
    print(f"{'Configuration':<16} | {'Best Length':>11} | {'Improvement':>11} | {'Runtime (s)':>11} | {'Improvements':>12} | {'Last Improv.':>12}")
    print("-" * 90)
    
    for result in results:
        cfg = result['config']
        print(f"{cfg['name']:<16} | {result['best_length']:11.2f} | {result['improvement']:10.2f}% | {result['runtime']:11.2f} | {result['improvements']:12d} | {result['last_improvement']:12d}")
    
    # Plot comparison
    plot_comparison(
        histories, 
        title='Route Length Improvement by Configuration',
        save_path=f"{output['results_dir']}/parameter_comparison.png",
        show=output['show_plots']
    )

# Add a main function to make the runner script happy
def main():
    run_comparison()

if __name__ == "__main__":
    main()