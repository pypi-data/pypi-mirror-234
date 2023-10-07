import json

def is_json(string:str) -> bool:
    try:
        json.loads(string)
        return True
    except:
        return False