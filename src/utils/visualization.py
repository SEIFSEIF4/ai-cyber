import matplotlib.pyplot as plt
import numpy as np
from .metrics import get_route_length


def plot_route(cities, route, city_names=None, title=None):
    """
    Plot the cities and the route between them.
    
    Args:
        cities: List of (x, y) coordinates for each city
        route: List of city indices representing a route
        city_names: Optional list of names for cities
        title: Optional title for the plot
    """
    # Clear current figure to avoid overlap
    plt.clf()
    
    # Extract coordinates for plotting
    coords = [cities[city] for city in route]
    coords.append(cities[route[0]])  # Add first city again to complete the loop
    xs, ys = zip(*coords)
    
    # Plot cities
    plt.scatter([city[0] for city in cities], [city[1] for city in cities], 
                s=100, c='blue', zorder=2)
    
    # Plot route
    plt.plot(xs, ys, 'k-', alpha=0.5, zorder=1)
    
    # Label cities
    for i, city_idx in enumerate(route):
        x, y = cities[city_idx]
        label = city_names[city_idx] if city_names else str(city_idx)
        plt.text(x + 2, y + 2, label, fontsize=10)
    
    if title:
        plt.title(title)
    else:
        plt.title("TSP Route")
        
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True, alpha=0.3)
    
    # Ensure the plot is rendered
    plt.draw()
    plt.tight_layout()


def plot_convergence(length_history, title=None, show=True, save_path=None):
    """
    Plot the convergence of route length over epochs.
    
    Args:
        length_history: List of route lengths over epochs
        title: Optional title for the plot
        show: Whether to show the plot
        save_path: Optional path to save the plot
    """
    plt.figure(figsize=(12, 6))
    plt.plot(length_history, 'b-')
    plt.title(title if title else 'Route Length over Epochs')
    plt.xlabel('Epoch')
    plt.ylabel('Route Length (shorter is better)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    if show:
        plt.show()
    else:
        plt.close()


def plot_comparison(results_dict, title=None, show=True, save_path=None):
    """
    Plot comparison of multiple runs with different parameters.
    
    Args:
        results_dict: Dictionary mapping run names to lists of route lengths
        title: Optional title for the plot
        show: Whether to show the plot
        save_path: Optional path to save the plot
    """
    plt.figure(figsize=(12, 6))
    
    for name, history in results_dict.items():
        plt.plot(history, label=name)
    
    plt.title(title if title else 'Parameter Comparison')
    plt.xlabel('Epoch')
    plt.ylabel('Route Length (shorter is better)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        
    if show:
        plt.show()
    else:
        plt.close()