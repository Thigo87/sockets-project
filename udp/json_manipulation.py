import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOMS_FILE = BASE_DIR / "rooms.json"

def add_data(data, filename=ROOMS_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
        
        existing_data.update(data)
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def read_data(filename=ROOMS_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
        return existing_data
    except Exception as e:
        print(f"Error: {e}")
        return None

def remove_data(key, filename=ROOMS_FILE):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)

        existing_data.pop(key, None)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


#How to work with json_manipulation.py
#add_data({"test" : ["localhost", "12500"]})
#print(read_data())
#remove_data("test")
#print(read_data())