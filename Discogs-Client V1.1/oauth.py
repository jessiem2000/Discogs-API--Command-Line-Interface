import requests
import webbrowser
from requests_oauthlib import OAuth1
from urllib.parse import parse_qs
from consumer_keys import KeyStore

K = KeyStore()

def Oauth_token():
    oauth_headers = {"useragent":"WickedCli/1.1/Beta"}
    consumer_key, consumer_secret = K.load_credentials()
    auth = OAuth1(client_key=consumer_key,
                  client_secret=consumer_secret,
                  signature_method="PLAINTEXT")

    r = requests.get("https://api.discogs.com/oauth/request_token", headers = oauth_headers, auth = auth)
    resp = r.text
    print(resp)
    access = parse_qs(resp)
    oauth_token = access.get("oauth_token")[0]
    oauth_token_secret = access.get("oauth_token_secret")[0]
    print(f"Please Verify your login! https://discogs.com/oauth/authorize?oauth_token={oauth_token}")
    webbrowser.open(f"https://discogs.com/oauth/authorize?oauth_token={oauth_token}")

    oauth_verify = input("Please authorize and input the code here!: ")
    if not oauth_verify:
        print("Verification code cannot be empty")
    auth_2 = OAuth1(client_key=consumer_key,
                         client_secret=consumer_secret,
                         resource_owner_key=oauth_token,
                         resource_owner_secret=oauth_token_secret,
                         verifier=oauth_verify,
                         signature_method="PLAINTEXT")
    r_auth2 = requests.post("https://api.discogs.com/oauth/access_token", headers = oauth_headers, auth = auth_2 )
    access2 = parse_qs(r_auth2.text)
    access_key = access2.get("oauth_token")[0]
    access_key_secret = access2.get("oauth_token_secret")[0]
    K.save_access_credentials(access_key, access_key_secret)
    finalauth = OAuth1(client_key=consumer_key,
                       client_secret=consumer_secret,
                       resource_owner_key=access_key,
                       resource_owner_secret=access_key_secret,
                       signature_method="PLAINTEXT")
    verify = requests.get("https://api.discogs.com/oauth/identity", headers = oauth_headers, auth = finalauth)
    user = verify.json()
    username = user["username"]
    return username
