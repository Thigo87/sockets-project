import json

def add_data(data, filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
        
        existing_data.update(data)
        
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return True
    except:
        return False

def read_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except:
        return None

add_data({"test" : ["localhost", "12500"]}, "./udp/rooms.json")
print(read_data("./udp/rooms.json"))