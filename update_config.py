import os
import json
from src.utils.config import get_default_config, save_config


def update_config():
    """Update or create the config file with the new format"""
    print("=== Updating Config File ===")
    
    if os.path.exists('tsp_config.json'):
        try:
            # Load existing config
            with open('tsp_config.json', 'r') as f:
                existing_config = json.load(f)
                
            print("Found existing config file. Updating...")
            
            # Get default config for reference
            default_config = get_default_config()
            
            # Merge existing config with default config
            updated_config = default_config.copy()
            
            # Preserve existing values where possible
            if 'cities' in existing_config:
                if 'named_cities' in existing_config['cities']:
                    updated_config['cities']['named_cities'] = existing_config['cities']['named_cities']
                if 'random_cities' in existing_config['cities']:
                    updated_config['cities']['random_cities'] = existing_config['cities']['random_cities']
            
            if 'algorithm' in existing_config:
                for key in existing_config['algorithm']:
                    if key in updated_config['algorithm']:
                        updated_config['algorithm'][key] = existing_config['algorithm'][key]
            
            if 'output' in existing_config:
                for key in existing_config['output']:
                    if key in updated_config['output']:
                        updated_config['output'][key] = existing_config['output'][key]
            
            if 'parameter_comparison' in existing_config:
                updated_config['parameter_comparison'] = existing_config['parameter_comparison']
            
            # Save updated config
            save_config(updated_config)
            print("Config file updated successfully!")
            
        except Exception as e:
            print(f"Error updating config: {e}")
            print("Creating new config file...")
            save_config(get_default_config())
            print("New config file created successfully!")
    else:
        print("No existing config file found. Creating new one...")
        save_config(get_default_config())
        print("New config file created successfully!")

if __name__ == "__main__":
    update_config()