class Datastore:
    search_url = "https://api.discogs.com/database/search"
    api_url = "https://api.discogs.com"
    identify = "https://api.discogs.com/oauth/identity"
    useragent = "WickedDiscogsCLI/1.0"
    headers = {"user-agent": useragent}
    def __init__(self, useragent , headers = headers, token = None, User = None):
        self.User = User
        self.token = token
        self.useragent = useragent
        self.headers = headers
        self.payload = {}
        self.search_keys = ["id", "title", "genre", "format", "type"]
    def get_token(self):
        return self._token

    def get_user(self):
        return self.User
    def get_useragent(self):
        return self.useragent

    def get_headers(self):
        return self.headers

    def get_payload(self):
        return self.payload
    def get_search_keys(self):
        return self.search_keys
#Setters

    def set_token(self, token):
        self.token = token
        self.payload["token"] = token
    def set_User(self, username):
        self.User = username
    def set_payload(self, key, value):
        self.payload[key] = value
    def reset_payload(self):
        self.payload.clear()
        self.payload["token"] = self.token
class menustate():
    def __init__(self):
        self.home = None
        self.search = None
        self.search_results = None

    def set_home(self, state):
        self.home = state
    def set_search(self, state):
        self.search = state
    def set_search_results(self, state):
        self.search_results = state
