import requests
import json
import sys


def main():
    useragent_ = "WickedDiscogsCLI/1.0"
    api_url = "https://api.discogs.com"
    identify = "https://api.discogs.com/oauth/identity"
    headers = {"user-agent": useragent_,
               }
    token = input("Visit https://www.discogs.com/settings/developers and input your personal access token here:")
    payload = {"token": token}
    r = requests.get(identify , headers = headers, params = payload)
    response = r.json()
    user = response["username"]
    print(response)
    print(f"You are logged in as {user}")


main()

