class Credentials:

    login:str
    password:str

    def __init__(self, login:str = None, password:str = None):
        self.login = login
        self.password = password