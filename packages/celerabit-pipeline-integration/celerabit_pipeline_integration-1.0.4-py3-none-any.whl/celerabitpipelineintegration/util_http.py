import json

def get_error_from_response(response:any) -> str:
    response_text:str = response.text
    json_object:any = None
    try:
        json_object = json.loads(response_text)
    except:
        return response_text
    
    if 'message' in json_object:
        return json_object['message']

    if 'error' in json_object:
        return json_object['error']

    return response_text

