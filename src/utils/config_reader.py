def read_store_data(file_path):
    """
    Read store IDs from CSV file
    Args:
        file_path: Path to CSV file containing store IDs
    Returns:
        list: List of store IDs
    """
    try:
        with open(file_path, 'r') as file:
            # Read non-empty lines and strip whitespace
            stores = [line.strip() for line in file if line.strip()]
            return stores
    except FileNotFoundError:
        raise FileNotFoundError(f"Store data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading store data: {str(e)}")

def get_all_stores():
    """Get all store IDs from both simulations"""
    stores = read_store_data('src/data/stores.csv')
    return stores