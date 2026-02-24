import os
import json

def create_config_folder_and_file(config_filename, config_data=None, config_folder='data\config_files'):
    """
    Create a configuration folder and write a configuration file with specified data.
    
    Parameters:
        config_folder (str): The name of the folder to create.
        config_filename (str): The name of the config file to create.
        config_data (dict): The configuration data to write to the config file.
        
    Returns:
        str: The path to the created config file.
    """
    # Step 1: Create the config folder if it does not exist
    os.makedirs(config_folder, exist_ok=True)

    # Step 2: Define the path for the config file
    config_file_path = os.path.join(config_folder, config_filename)

    # Step 3: Write the configuration data to the config file
    if config_data is not None:
        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        print(f"Config file created at: {config_file_path}")
    else:
        print("No configuration data provided. Config file was not created.")

    return config_file_path


def load_config(config_filename, config_folder=None):
    if config_folder is None:
        config_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'config_files')
    """
    Load configuration from a specified folder and file.
    
    Parameters:
        config_folder (str): The folder where the config file is located.
        config_filename (str): The name of the config file.
        
    Returns:
        dict: The configuration data as a dictionary.
    """
    # Construct the full path to the config file
    config_file_path = os.path.join(config_folder, config_filename)

    # Read and return the config data
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)

# Example usage
if __name__ == "__main__":
    # Define some example configuration data
    config_data = {
        "reference_data_excel": "data/sypher-rater-reference_data.xlsx",
    }
    
    # Create the config folder and file
    create_config_folder_and_file(config_data=config_data)
    config = load_config()
    print(config)


