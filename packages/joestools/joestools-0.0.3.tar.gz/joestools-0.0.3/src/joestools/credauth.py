"""This Module provides Credentials for all modules"""
#from .common import DefaultDict
from dataclasses import dataclass
import csv
import os
import time
from flask_httpauth import HTTPDigestAuth, HTTPTokenAuth, MultiAuth

CREDENTIALS = "/etc/Credentials/credentials.csv"
EIBPORT = "https://eibport"

digest_auth = HTTPDigestAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(digest_auth, token_auth)

@digest_auth.get_password
def get_digest(username, host="pyfhem"):
    #result = get_cred(username, host)
    result = Cred(host=host, user=username)
    return result

def get_pw(username):
    if username in users:
        print(f"{users.get(username)}")
        return users.get(username)

@token_auth.verify_token
def verify_token(token, host="pyfhem", username="SECRET_KEY"):
    #result = get_cred(host, username)
    result = Cred(host=host, user=username)
    if token == result['password']:
        return result['password'] 

@dataclass
class DefaultDict():
    """ Default Dict with functions

    Returns:
        _type_: _description_
    """
    name: str | None = None
    status: int = 500
    failure: str = ""
    runtime: str | None = None

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    #def __cmp__(self, dict_):
    #    return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)


def cred(host):
    """ Get Credentials for given host from file

    Args:
        host (string): hostname

    Returns:
        dict: dict from credentials 
    """
    try:
        FOUND = 0
        with open (CREDENTIALS, 'r') as myfile:
            router_dict = csv.DictReader(myfile)
            for row in router_dict:
                if host in row['host']:
                    FOUND = 1
                    if "lancom" in row['host']:
                        # we need to give back the line back to netmiko
                        # and need to modifiy it
                        host, username, key, password, devtype = row['host'], row['username'], row['key'], row['password'], row['devtype']
                        if row['key'] == 'no':
                            router = { 'device_type' : devtype, 'ip' : host, 'username' : username, 'password' : password }
                        elif row['key'] == 'yes':
                            router = { 'device_type' : devtype, 'ip' : host, 'username' : username, 'use_keys' : True, 'key_file' : password }
                        return router
                    else:
                        return row
            if FOUND == 0:
                return f"Host: {host} not found."
    except Exception as e:
        return f"Exception {e}"  

@dataclass
class Cred(DefaultDict):
    """ Get Credentials for given host and user from file

    Args:
        host (string): hostname
        user (string): username

    Returns:
        dict: dict from credentials 
    """
    host: str | None = None
    user: str | None = "athome@mishki.de"
    usage: str | None = None
    password: str | None = None
    configstring: str | None = None
    receiver: str | None = None
    devtype: str | None = None
    usage: str | None = None
    runtime: int | None = None
    found: int = 0
    failure: str = ""
    status: int = 500

    def __post_init__(self):
        start = time.time()
        #print(start)
        self.check_entry()
        end = time.time()
        self.runtime = round(end - start, 2)
        #print(self.runtime)

    def check_file(self):
        if os.path.exists(CREDENTIALS):
            #print("hier")
            self.status = 200

    def check_entry(self):
        self.check_file()
        if self.status == 200:
            with open (CREDENTIALS, 'r') as myCred:
                user_dict = csv.DictReader(myCred)
                self.status = 500
                if (self.usage == "ssh" and isinstance(self.host, str) and isinstance(self.user, str)):
                    for row in user_dict:
                        if "#" not in row['host'] and self.host in row['host'] and self.user in row['username']:
                            self.status = 200
                            self.user, self.password, self.devtype = row['username'], row['password'], row['devtype']
                            self.found = 1
                elif self.usage == "mail":
                    for row in user_dict:
                        if "#" not in row['host'] and self.host in row['host'] and self.user in row['username']:
                            self.user, self.password, self.receiver = row['username'], row['password'], row['devtype']
                            self.status = 200
                            self.found = 1
                            break
                elif self.usage == "eibport":
                    for row in user_dict:
                        if "#" not in row['host'] and self.host in row['host']:
                            self.configstring = row['password']
                            self.status = 200
                            self.found = 1
                            break
                elif self.usage == "push" or self.usage == "html":
                    for row in user_dict:
                        if "#" not in row['host'] and self.host in row['host']:
                            self.user = row["username"]
                            self.password = row["password"]
                            self.found = 1
                            break
                else:
                    if self.usage is None:
                        self.failure = f"No usage was given."
                    else:
                        self.failure = f"No usage {self.usage} was found in logic."
                if self.found == 0 and self.usage != None:
                    self.failure = f"Host: {self.host} with User: {self.user} not found."
        else:
            self.failure = f"Status is {self.status}"
            self.status = 500



def getconfigstring(filename=CREDENTIALS, host=EIBPORT) -> str:
    """ Get Config String as credential to connect to eibport

    Args:
        filename (_type_, optional): credentials filename. Defaults to CREDENTIALS.
        host (_type_, optional): for which host we want to get the credentials. Defaults to EIBPORT.

    Returns:
        str: configstring
    """
    try:
        count = 0
        configstring = None
        with open (filename, 'r', encoding="utf8") as myfile:
            router_dict = csv.DictReader(myfile)
            for row in router_dict:
                if host in row['host']:
                    configstring = row['password']
                    host = row['host']
                    count += 1
        if count > 0:
            return configstring
        else:
            try:
                logger.error(f"(getconfigstring): in getconfigstrings, host {host} was not found")
            except Exception as ex:
                print(f"(getconfigstring): in getconfigstrings, host {host} was not found. Exception {ex}")
            return configstring
    except Exception as ex:
        logging.error(f"Exception {ex}")
        configstring = None
        try:
            logger.error(f"(getconfigstring): Host or filename {host}, {filename} not available.")
        except Exception as ex:
            print(f"(getconfigstring): Host or filename {host}, {filename} not available. Exception {ex}")
        return configstring


if __name__ == "__main__":
    CREDENTIALS = "/etc/Credentials/credentials.csv"
    EIBPORT = "https://eibport"
