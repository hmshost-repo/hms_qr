def read_store_data(file_path):
    """Read store IDs from CSV file"""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_all_stores():
    """Get all store IDs from both simulations"""
    sim1_stores = read_store_data('src/data/sim1_stores.csv')
    sim2_stores = read_store_data('src/data/sim2_stores.csv')
    return sim1_stores + sim2_stores 