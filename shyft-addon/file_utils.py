import json

def read_file_to_json(file_path):
    """
    Reads the content of a file and returns it as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return "Error: The file was not found."
    except Exception as e:
        return f"An error occurred: {e}"
