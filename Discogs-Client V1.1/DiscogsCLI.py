import requests
import sys
from simple_term_menu import TerminalMenu
from consumer_keys import KeyStore
from datastore import Datastore
from datastore import menustate
from oauth import Oauth_token

K = KeyStore()
U = Datastore("WickedDiscogsCLI/1.1")
M = menustate()
Search = Datastore.search_url

def oauth_menu():
    authtype = ["Token", "Oauth"]
    authmenu = TerminalMenu(authtype, title = "How would you like to authenticate?")
    auth_select = authmenu.show()
    if auth_select == 0:
        token()
    if auth_select == 1:
        print("Oauth!")
        print("Please go to https://www.discogs.com/settings/developers and create an application!")
        consumer_key = input("Put your Consumer Key here!:")
        consumer_secret = input("Put your Consumer Secret key here!:")
        K.save_credentials(consumer_key, consumer_secret)
        username = Oauth_token()
        U.set_User(username)
        homemenu()

def token():
    token = input("Visit https://www.discogs.com/settings/developers and input your personal access token here:")
    U.set_token(token)
    r = requests.get(Datastore.identify, headers = U.headers, params = U.payload)
    response = r.json()
    username = response["username"]
    U.set_User(username)
    homemenu()

def homemenu():
    print(U.User)
    home_options = ["Exit", "Search", "Logout"]
    home_menu = TerminalMenu(home_options, title = f"Home: logged in as | {U.User}")
    M.set_home(False)
    while not M.home:
        home_select = home_menu.show()
        if home_select == 0:
            sys.exit("GoodBye :)")
        if home_select == 1:
            M.set_home(True)
            searchmenu()
        if home_select == 3:
            K.clear_credentials()


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




oauth_menu()
