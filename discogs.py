import requests
import sys
from simple_term_menu import TerminalMenu

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

#Setters

    def set_token(self, token):
        self.token = token
        self.payload["token"] = token
    def set_User(self, username):
        self.User = username
    def set_payload(self, key, value):
        self.payload[key] = value

class menustate():
    def __init__(self):
        self.home = None
        self.search = None

    def set_home(self, state):
        self.home = state
    def set_search(self, state):
        self.search = state


U = Datastore("WickedDiscogsCLI/1.0")
M = menustate()
Search = Datastore.search_url

def main():
    token = input("Visit https://www.discogs.com/settings/developers and input your personal access token here:")
    U.set_token(token)
    r = requests.get(Datastore.identify, headers = U.headers, params = U.payload)
    response = r.json()
    username = response["username"]
    U.set_User(username)
    main2()

def main2():
    print(U.User)
    home_options = ["Exit", "Search"]
    home_menu = TerminalMenu(home_options, title = f"Home: logged in as | {U.User}")
    M.set_home(False)
    while not M.home:
        home_select = home_menu.show()
        if home_select == 0:
            sys.exit("GoodBye :)")
        if home_select == 1:
            M.set_home(True)
            main3()

def main3():
    options = ["<- Return",
               "type",
               "title",
               "release_title",
               "credit",
               "artist",
               "anv",
               "label",
               "genre",
               "style",
               "country",
               "year",
               "format",
               "catno",
               "barcode",
               "track",
               "submitter",
               "contributor"]
    search_menu = TerminalMenu(options, title ="Search By:")
    M.set_search(False)
    while not M.search:
        search_select = search_menu.show()
        if search_select == 0:
            M.set_search(True)
            M.set_home(False)
            main2()
        else:
            index = options[search_select]
            print(f"You have selected {index}!")
            s_string = input(f"What {index} would you like to search for? :")
            search(index, s_string)
            M.set_search(True)


def search(index, s_string):
    U.set_payload(index, s_string)
    r = requests.get(f"{Search}", params=U.payload, headers = U.headers)
    print(r.url)
    print(r.text)


main()

