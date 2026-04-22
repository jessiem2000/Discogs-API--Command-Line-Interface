import requests
import sys
from simple_term_menu import TerminalMenu
import json

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
    homemenu()

def homemenu():
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
            searchmenu()

def searchmenu():
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
            homemenu()
        else:
            index = options[search_select]
            print(f"You have selected {index}!")
            s_string = input(f"What {index} would you like to search for? :")
            query = query_menu()
            if not query:
                search(index, s_string)
                M.set_search(True)
            if query:
                userquery = input("What Search query would you like to add?:")
                U.set_payload("q", userquery)
                search(index, s_string)
                M.set_search(True)



def search_results_menu(all_options, items_per_page = 10):
    page = 0
    total_pages = (len(all_options) + items_per_page - 1) // items_per_page
    M.set_search_results(False)
    while not M.search_results:
            start = page * items_per_page
            end = start +items_per_page

            view = all_options[start:end]
            menu_items = list(view)
            if page < total_pages -1 :
                menu_items.append("[Next Page] -->")
            if page > 0:
                menu_items.insert(0, "<-- [Prev Page]")
            menu_items.append("[Return to Search]")

            search_results_menu = TerminalMenu(menu_items, title=f"\nPage {page + 1} of {total_pages}\n{'-'*30}")
            results_select = search_results_menu.show()
            if results_select is None: break
            selection = menu_items[results_select]

            if "[Next Page]" in selection:
                page += 1
            elif "[Prev Page]" in selection:
                page -= 1
            elif "[Return to Search]" in selection:
                M.set_search_results(True)
                M.set_search(False)
                U.reset_payload()
                searchmenu()
            else:
                print(f"\nSELECTED ENTRY: {selection}")
                break



def search(index, s_string):
    U.set_payload(index, s_string)
    r = requests.get(Search, params=U.payload, headers = U.headers)
    data = r.json()
    all_options = []
    for entry in data["results"]:
        string = []
        for k in U.search_keys:
            val = str(entry.get(k, "Missing")).strip()
            string.append(f"{k.upper()}: {val}")
        all_options.append("    ".join(string))
    search_results_menu(all_options, items_per_page = 10)

def query_menu():
    options = ["Yes", "No"]
    query_menu = TerminalMenu(options, title = "Would you like to add a search query?")
    query_select = query_menu.show()
    if query_select == 0:
        query = True
        return query
    if query_select == 1:
        query = False
        return query




main()
