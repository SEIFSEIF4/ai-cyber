import os
import json

def get_default_config():
    """Return the default configuration"""
    return {
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
            "n_offsprings": 30,
            "n_epochs": 500,
            "crossover_alpha": 0.5,
            "verbose": True
        },
        "output": {
            "results_dir": "results",
            "save_plots": True,
            "show_plots": True
        }
    }

def load_config():
    """Load configuration from file or create default"""
    config_path = 'tsp_config.json'
    
    if not os.path.exists(config_path):
        # Create default configuration
        config = get_default_config()
        save_config(config)
        print(f"Created default configuration file: {config_path}")
        return config
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        # Return default configuration if there's an error
        return get_default_config()

def save_config(config):
    """Save configuration to file"""
    config_path = 'tsp_config.json'
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Configuration saved to {config_path}")

def ensure_results_dir(config):
    """Ensure results directory exists"""
    results_dir = config['output']['results_dir']
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        # Create .gitkeep to ensure directory is tracked in git
        with open(f"{results_dir}/.gitkeep", 'w') as f:
            pass