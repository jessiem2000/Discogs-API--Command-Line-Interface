import json
import os
import keyring
from platformdirs import user_data_dir

class KeyStore:
    Discogsclient = "WickedCli"
    ''' backup directories for running in virtual env or linux/container'''
    B_DIR = user_data_dir("WickedDiscogsCLi", "WickedCli")
    B_FILE = os.path.join(B_DIR, "config.json")

    @classmethod
    def save_credentials(cls, consumer_key: str, consumer_secret: str) -> None:
        try:  #'''system storage'''
            keyring.set_password(cls.Discogsclient, "consumer_key", consumer_key)
            keyring.set_password(cls.Discogsclient, "consumer_secret", consumer_secret)
        except Exception: #'''json file backup'''
            os.makedirs(cls.B_DIR,exist_ok = True)
            with open(cls.B_FILE, "w", encoding="utf-8") as j:
                json.dump({"consumer_key":consumer_key,"consumer_secret":consumer_secret}, j)
    @classmethod
    def save_access_credentials(cls, access_key: str, access_key_secret: str) -> None:
        try:  #'''system storage'''
            keyring.set_password(cls.Discogsclient, "access_key", access_key)
            keyring.set_password(cls.Discogsclient, "access_key_secret", access_key_secret)
        except Exception: #'''json file backup'''
            os.makedirs(cls.B_DIR,exist_ok = True)
            with open(cls.B_FILE, "w", encoding="utf-8") as j:
                json.dump({"access_key":access_key,"access_key_secret":access_key_secret}, j)


    @classmethod
    def load_credentials(cls) -> tuple[str | None, str | None]:
        try: #check system storage
            key = keyring.get_password(cls.Discogsclient, "consumer_key")
            secret = keyring.get_password(cls.Discogsclient, "consumer_secret")
            return key, secret
        except Exception: #check Json if storage fails
            if os.path.exists(cls.B_FILE):
                with open(cls.B_FILE,"r", encoding ="utf-8") as j:
                    k = json.load(j)
                    return k.get("consumer_key"), k.get("consumer_secret")
            return None, None
    @classmethod
    def load_access_credentials(cls) -> tuple[str | None, str | None]:
        try: #check system storage
            access_key = keyring.get_password(cls.Discogsclient, "access_key")
            access_secret = keyring.get_password(cls.Discogsclient, "access_key_secret")
            return access_key, access_secret
        except Exception: #check Json if storage fails
            if os.path.exists(cls.B_FILE):
                with open(cls.B_FILE,"r", encoding ="utf-8") as j:
                    k = json.load(j)
                    return k.get("access_key"), k.get("access_key_secret")
            return None, None
    @classmethod
    def clear_credentials(cls) -> None:
        """Deletes keys when the user chooses to log out."""
        try:
            keyring.delete_password(cls.Discogsclient, "consumer_key")
            keyring.delete_password(cls.Discogsclient, "consumer_secret")
            keyring.delete_password(cls.Discogsclient, "access_key")
            keyring.delete_password(cls.Discogsclient, "access_key_secret")
        except Exception:
            pass
        try:
            if os.path.exists(cls.B_FILE):
                os.remove(cls.B_FILE)
        except OSError:
            pass
