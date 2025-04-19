# cleanup_results_files.py
# Script to clean up image files in the results folder and reset configuration

import os
import glob
import json
import sys

def cleanup_results_images():
    """Clean up image files in the results folder"""
    if not os.path.exists('results'):
        print("Results directory not found.")
        return 0
    
    # Get all image files
    image_patterns = ['results/*.png', 'results/*.jpg', 'results/*.pdf', 'results/*.svg']
    image_files = []
    
    for pattern in image_patterns:
        image_files.extend(glob.glob(pattern))
    
    if not image_files:
        print("No image files found in results directory.")
        return 0
    
    # Ask for confirmation
    print("\nWARNING: This will permanently delete the following image files:")
    for file in image_files:
        print(f"  - {file}")
    
    confirmation = input("\nAre you sure you want to delete these image files? (y/n): ")
    
    if confirmation.lower() != 'y':
        print("Image cleanup cancelled.")
        return 0
    
    # Remove image files
    images_removed = 0
    for file in image_files:
        os.remove(file)
        print(f"Removed: {file}")
        images_removed += 1
    
    # Create .gitkeep to ensure directory is tracked in git
    with open('results/.gitkeep', 'w') as f:
        pass
    print("Created results/.gitkeep file")
    
    print(f"\nImage cleanup completed. {images_removed} image files removed.")
    return images_removed

def reset_config_file():
    """Reset the tsp_config.json file to default settings"""
    # Default configuration
    default_config = {
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
    
    # Check if config file exists
    if os.path.exists('tsp_config.json'):
        confirmation = input("Do you want to reset the tsp_config.json file to default settings? (y/n): ")
        if confirmation.lower() != 'y':
            print("Config reset cancelled.")
            return False
    
    # Write default config
    with open('tsp_config.json', 'w') as f:
        json.dump(default_config, f, indent=2)
    
    print("Reset tsp_config.json to default settings.")
    return True

def main():
    print("=== Cleanup Utility ===")
    print("1. Clean up image files in results directory")
    print("2. Reset tsp_config.json file")
    print("3. Do both")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == '1':
        cleanup_results_images()
    elif choice == '2':
        reset_config_file()
    elif choice == '3':
        cleanup_results_images()
        reset_config_file()
    elif choice == '4':
        print("Exiting...")
        return
    else:
        print("Invalid choice.")
    
    print("\nCleanup completed.")

if __name__ == "__main__":
    main()