import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "data" #data directory

def file_path(filename): #function to return the path of a file
    return BASE_DIR / filename

def add_data(data, filename): #function to add data to a json file
    try:
        with open(file_path(filename), "r", encoding="utf-8") as file:
            existing_data = json.load(file)
        
        existing_data.update(data)
        
        with open(file_path(filename), "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return True
    
    except Exception as e: 
        print(f"Error: {e}")
        return False

def read_data(filename): #function to read data from a json file
    try:
        with open(file_path(filename), "r", encoding="utf-8") as file:
            existing_data = json.load(file)

        return existing_data
    
    except Exception as e:
        print(f"Error: {e}")

        return None

def remove_data(key, filename): #function to remove data from a json file
    try:
        with open(file_path(filename), "r", encoding="utf-8") as file:
            existing_data = json.load(file)

        existing_data.pop(key, None)

        with open(file_path(filename), "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return True
    
    except Exception as e:
        print(f"Error: {e}")
        
        return False


#How to work with json_manipulation.py
#add_data({"test" : ["localhost", "12500"]}, filename)
#print(read_data(filename))
#remove_data("test", filename)