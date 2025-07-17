import json
import os


class JsonDataManager:


    def __init__(self):
        pass


    def read_data(self, filepath):
        if not os.path.exists(filepath):
            return []
    
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(f"Fehler beim Dekodieren der JSON-Datei: {filepath}. Bitte JSON-Syntax überprüfen!")
            return []
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist beim Lesen von {filepath}: {e} aufgetreten")
            return []
    
    
    def write_data(self, filepath, data):
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
                return True
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist beim Schreiben von {filepath}: {e} aufgetreten")
            return False    