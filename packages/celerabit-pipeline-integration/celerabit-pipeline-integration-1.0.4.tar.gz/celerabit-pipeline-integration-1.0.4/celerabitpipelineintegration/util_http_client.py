import requests

from celerabitpipelineintegration.util_configuration import Configuration

class HttpClient:

    __token__:str = None

    def __init__(self, token:str = None):
        self.__token__ = token

    def __get_headers__(self, base_headers:any = None) -> dict:
        new_headers:any = base_headers
        if not new_headers:
            new_headers = {}
        
        new_headers['celerabit-invoker'] = Configuration.instance().get_config_value('INVOKER', 'id')
        
        if self.__token__:
            new_headers['Authorization'] = 'Bearer {}'.format(self.__token__)

        return new_headers

    def post(self, url:str, json:dict = None, data:dict = None, headers:dict = None) -> any:
        headers_to_send:any = self.__get_headers__(headers)
        response:any = requests.post(url, json = json, data = data, headers = headers_to_send)
        return response

    def get(self, url:str, params:dict = None, headers:dict = None) -> any:
        headers_to_send:any = self.__get_headers__(headers)
        response:any = requests.get(url, params = params, headers = headers_to_send)
        return response
