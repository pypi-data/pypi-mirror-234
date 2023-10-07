from celerabitpipelineintegration.model_credentials import Credentials
import json

from celerabitpipelineintegration.util_configuration import Configuration
from celerabitpipelineintegration.util_http import get_error_from_response
from celerabitpipelineintegration.util_http_client import HttpClient

class Authenticator:

    def __do_post__(self, credentials:Credentials):
        url:str = Configuration.instance().get_config_value('CELERABIT-ENDPOINTS', 'authenticate')
        data:any = {
            'username': credentials.login,
            'password': credentials.password
        }
        http_client:HttpClient = HttpClient()
        response:any = http_client.post(url, json = data)
        return response

    def __get_token__(self, credentials:Credentials) -> str:
        response = self.__do_post__(credentials)
        if response.status_code != 200:
            raise Exception(get_error_from_response(response))

        json_object:any = None
        try:
            json_object = json.loads(response.text)
        except Exception as e:
            raise Exception('Invalid response object.  {error}. {json_response}'.format(error = e, json_response = response.text))

        if not 'token' in json_object:
            raise Exception('Response does not include a token')

        return json_object['token']

    def authenticate(self, credentials:Credentials) -> str:
        token:str = self.__get_token__(credentials)
        return token