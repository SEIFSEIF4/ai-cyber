# Evolutionary Algorithm for TSP

This project implements an evolutionary algorithm for solving the Travelling Salesman Problem (TSP), based on the article from [towardsdatascience.com](https://towardsdatascience.com/an-extensible-evolutionary-algorithm-example-in-python-7372c56a557b/).

## Features

- **Tournament Selection**: Uses tournament selection to maintain diversity in the population
- **Optimized Crossover**: Implements an ordered crossover method optimized for TSP
- **Elitism**: Preserves the best individual in each generation
- **Detailed Progress Tracking**: Tracks improvements, mutations, and convergence
- **Named Cities**: Supports city labels for intuitive visualization
- **Parameter Comparison**: Tools to compare different algorithm configurations
- **Configuration System**: Centralized JSON configuration for all parameters

## Project Structure

```
tsp-evolutionary-algorithm/
│
├── src/                         # Source code
│   ├── algorithms/              # Algorithm implementations
│   │   ├── base.py              # Base classes for EAs
│   │   └── tsp.py               # TSP specific implementation
│   └── utils/                   # Utility functions
│       ├── metrics.py           # Distance calculations
│       ├── visualization.py     # Plotting tools
│       └── config.py            # Configuration management
│
├── examples/                    # Example scripts
│   ├── named_cities.py          # Demo with named cities
│   ├── parameter_comparison.py  # Compare parameters
│   └── simple_tsp.py            # Simple TSP example
│
├── results/                     # Output directory
│
├── tests/                       # Unit tests directory
│
├── run_tsp.py                   # Interactive menu-based runner
├── update_config.py             # Configuration updater/generator
├── cleanup_results_files.py     # Utility to clean result files
├── tsp_config.json              # Configuration file
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SEIFSEIF4/tsp-evolutionary-algorithm.git
   cd tsp-evolutionary-algorithm
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Interactive Runner

The easiest way to run the algorithm is through the interactive menu:

```bash
python run_tsp.py
```

This provides options to:

- Run with named cities or random cities
- Run specific example scripts
- Modify configuration interactively

### Running Examples Directly

```bash
# Demo with named cities (A-T)
python examples/named_cities.py

# Compare different parameter configurations
python examples/parameter_comparison.py

# Simple demonstration
python examples/simple_tsp.py
```

### Using in Your Own Code

```python
from src.algorithms.tsp import run_tsp_evolution

# Define your cities
city_coords = [
    (60, 200), (180, 200), (80, 180), ...
]

# Optional: define city names
city_names = ["A", "B", "C", ...]

# Run the algorithm (uses config file for defaults)
result = run_tsp_evolution(
    cities=city_coords,
    city_names=city_names  # Optional
)

# Access results
best_route = result['best_route']
best_length = result['best_length']
```

## Configuration System

The project uses a centralized configuration file (`tsp_config.json`) to manage all settings:

### Updating Configuration

1. Run the update script to create/update your config file:

   ```bash
   python update_config.py
   ```

2. Modify configuration through the interactive menu:

   ```bash
   python run_tsp.py
   # Select option 6 to modify configuration
   ```

3. Edit the configuration file directly:
   ```bash
   # Open tsp_config.json with any text editor
   ```

### Configuration Structure

The configuration file is organized into sections:

```json
{
  "cities": {
    "named_cities": {
      /* City coordinates and names */
    },
    "random_cities": {
      /* Random city generation settings */
    }
  },
  "algorithm": {
    "population_size": 100,
    "tournament_size": 5,
    "mutation_rate": 0.01
    /* Other algorithm parameters */
  },
  "output": {
    "results_dir": "results",
    "save_plots": true,
    "show_plots": true
  },
  "parameter_comparison": [
    /* Parameter sets for comparison */
  ]
}
```

## Cleaning Up Results

To clean up result images:

```bash
python cleanup_results_files.py
```

This utility provides options to:

- Remove all image files from the results directory
- Reset the configuration file to default settings

## Algorithm Parameters

Key parameters that can be configured:

- **population_size**: Number of individuals in the population (default: 100)
- **tournament_size**: Number of individuals in tournament selection (default: 5)
- **mutation_rate**: Probability of mutation (default: 0.01)
- **n_epochs**: Number of generations to run (default: 500)
- **n_offsprings**: Number of offspring per generation (default: 30)
- **crossover_alpha**: Parameter for crossover point (default: 0.5)

## Example Results

For the 20-city example with named cities (A-T), the algorithm typically finds routes that are 40-50% shorter than random routes within 500 generations.
