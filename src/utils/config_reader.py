import os


def read_store_data(file_path):
    absolute_path = file_path
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        absolute_path = os.path.join(project_root, file_path)

        with open(absolute_path, 'r') as file:
            stores = [line.strip() for line in file if line.strip()]
            return stores
    except FileNotFoundError:
        raise FileNotFoundError(f"Store data file not found. \nTried paths:\n- {file_path}\n- {absolute_path}")
    except Exception as e:
        raise Exception(f"Error reading store data from {absolute_path}: {str(e)}")


def get_all_stores():
    stores = read_store_data('src/data/stores.csv')
    return stores