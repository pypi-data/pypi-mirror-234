"""Control Hue Light bulbs at home"""
from collections import defaultdict
from dataclasses import dataclass, field
import re
import time
import logging
import requests
import urllib3
from werkzeug import datastructures as ds
from .credauth import cred as Cra
from .common import DefaultDict
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HUEADDRESSFILE = '/etc/Credentials/hueaddressnames.csv'
DEFFAVHUE = "Fdn2CNYLTfDfp6E"
DEFFAVHUEALL = "Hell"

def getaddrnames(addressfile=HUEADDRESSFILE):
    """Get Addressnames from file, which should be recorded in mysql

    Args:
        addressfile (list): _description_. Defaults to HUEADDRESSFILE.
    """    
    addressnames = []
    try:
        with open (addressfile, "r", encoding="utf-8") as myaddr:
            for line in myaddr.readlines():
                for entry in line.split(','):
                    if re.match("^#", entry) is None:
                        addressnames.append(entry.strip())
        logging.debug("(getaddrnames): Addressnames {}".format(addressnames))
    except Exception as e:
        logging.error(f'(getaddrnames): File {addressfile} could not be read')
        return(f'(getaddrnames): File {addressfile} could not be read')
    return(addressnames)

@dataclass
class Hue(DefaultDict):
    """Control Hue

    Args:
        DefaultDict (_type_): _description_
    """    
    group: str | None =  None
    groupadd: str |None = None
    state: str | bool = ""
    new_state: str | None = None
    req: ds.MultiDict | None = None
    status: int = 500
    status_code: int = 500
    scenes: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
    defscene: str = "Hell"
    scene: str | None = None
    sceneid: int | None = None
    newsceneid: int | None = None
    newscene: str | None = None
    failure: str = ""
    header1: str = 'content-type,cache-control'
    header2: str = "application/json,no-cache"
    url: str = "https://hue"
    #__url1: str | None = None
    payload: str = " { \"on\":" + state + " }"
    data: dict | None = field(default_factory=lambda: defaultdict(dict))
    #_host: str | None = None
    #_pwd: str | None = None
    runtime: float = -1

    def __post_init__(self):
        start = time.time()
        self.get_credentials()
        self.get_group()
        if self.groupadd is None:
            if self.failure == "":
                self.failure = f"Cannot create Hue, because groupadd is {self.groupadd}"
        else:
            self.get_status()
        end = time.time()
        self.runtime = round(end - start, 2)

    def get_credentials(self) -> bool:
        try:
            row = Cra('hue')
            self.__host, self.__pwd = row['host'], row['password']
            self.__url = f"{self.url}/api/{self.__pwd}"
            return True
        except Exception as e:
            self.failure = f"get_Credentials failed with {e}"
            self.status = 500
            return False

    def get_group(self) -> None:
        try:
            if isinstance(self.group, (str, int)):
                req = requests.get(f'{self.__url}/groups/', verify=False, timeout=15)
                if req.status_code == 200:
                    #if isinstance(self.group, str):
                    names = []
                    ids = []
                    #print(req.json())
                    for entry in req.json().items():
                        #if re.search(f'^{self.group}$', entry[1]['name']) is not None:
                        if re.search(f'{self.group}', entry[1]['name']) is not None:
                            names.append(entry[1]['name'])
                            ids.append(entry[0])
                    if len(names) == 1:
                        self.groupadd = int(ids[0])
                        self.status = 200
                        self.group = names[0]
                    elif len(names) == 0:
                        self.failure = f"We cannot find any group name matching {self.group}"
                        self.status = 500
                    else:
                        self.failure = f"We have found {len(names)} entries {names} instead of 1."
                        self.status = 500
                    print(names, ids)
                else:
                    self.failure = f"Request to {self.url} was not successfull. Status Code: {req.status_code}"
                    self.status = 500
            if not isinstance(self.groupadd, int):
                self.failure = f"Could not find address {self.group} in {self.url}"
        except Exception as e:
            self.failure = f"Exception in get_Group {e}"
            self.status = 500

    def get_status(self) -> None:
        try:
            req = requests.get(f"{self.__url}/groups/{self.groupadd}", verify=False, timeout=15)
            print("hier")
            print(req.json())
            status = list(req.json().keys())[0]
            print(f"Status: {status}")
            if status != "error" and req.status_code == 200:
                print(req.json())
                c1 = list(req.json()["state"].values()).count(False)
                c2 = list(req.json()["state"].values()).count(True)
                if c1 == 2:
                    state = False
                elif c2 == 2:
                    state = True
                else:
                    # all_on
                    state = list(req.json()["state"].values())[0]                
                self.state = state
                self.status = 200
                self.status_code = req.status_code
            else:
                self.failure = f"{self.url} had issues with status_code {self.status_code}"
                self.status = 500
        except Exception as e:
            self.failure = f"Exception in get_Status {e}"
            self.status = 500

    def set_status(self, value: str) -> None:
        try:
            print(value)
            if isinstance(value, (str, bool)):
                self.new_state = str(value).lower()
                self.payload = '{ "on": ' +  self.new_state + ' }'
                headers = dict(zip(list(self.header1.split(",")), list(self.header2.split(","))))
                req = requests.put(f"{self.__url}/groups/{self.groupadd}/action", data = self.payload, headers=headers, verify=False, timeout=15)
                status = list(req.json()[0].keys())[0]
                if req.status_code == 200 and status == 'success':
                    # config was successful
                    self.data = req.json()
                    self.status = 200
                    logging.info(f"INFO: {self.url} wurde im {self.group} von {self.state} auf {self.new_state} geschaltet")
                    self.state = self.new_state
                else:
                    self.status = 500
                self.status_code = req.status_code
                # add logging to mysql
            else:
                self.failure = f"new_state is not set"
                self.status = 500
        except Exception as e:
            self.failure = f"Exception in set {e}"
            self.status = 500

    def get_scenes(self) -> None:
        # get all Scenes from Hue which are realted with self.groupadd
        req = requests.get(f'{self.__url}/scenes/', verify=False, timeout=15)
        if req.status_code == 200:
            for sceneid, value in req.json().items():
                try:
                    group = int(value.get('group'))
                except:
                    continue
                else:
                    if self.groupadd == group:
                        self.scenes[sceneid] = value.get("name")
                        #if self.scene is None:
                        #    if value.get("name") == self.defscene:
                        #        self.scene = 
                        #if self.scene in value.get("name"):
                        #    favstr = value.get("name")   
        else:
            self.failure = f"Could not get a successful respsonse from {self.url}."
            self.status = 500

    def set_scene(self, direction: str) -> None:
        if not isinstance(self.scene, str):
            self.scene = self.defscene
            #self.failure = f"No Scene was set, but it is needed to rotate Scenes."
            #self.status = 500
        if isinstance(direction, str):
            if direction.lower() == "up":
                self.__next_scene()
            elif direction.lower() == "down":
                self.__prev_scene()
            else:
                self.failure = f"Function {direction} is not implemented. Use up or down as direction."
                self.status = 200            

    def __prev_scene(self) -> None:
        """ get Scenes from Hue for Group (room)
        """
        self.get_scenes()
        if len(self.scenes) > 0:
            idx = list(self.scenes.values()).index(self.scene)
            sidx = len(self.scenes)
            if idx == 0:
                sidx = sidx - 1
                self.newsceneid = list(self.scenes.keys())[sidx]
                self.newscene = list(self.scenes.values())[sidx]
            else:
                idx = idx - 1
                self.newsceneid = list(self.scenes.keys())[idx]
                self.newscene = list(self.scenes.values())[idx]
        else:
            self.failure = f"Could not find Scenes {self.scenes} in {self.url}."
            self.status = 500
        if isinstance(self.group, (str, int)):
            self.payload = '{ "scene": ' + "\"" + self.newsceneid + "\"" + ' }'
            headers = dict(zip(list(self.header1.split(",")), list(self.header2.split(","))))
            req = requests.put(f"{self.__url}/groups/{self.groupadd}/action", data = self.payload, headers=headers, verify=False, timeout=15)
            status = list(req.json()[0].keys())[0]
            if req.status_code == 200 and status == 'success':
                # config was successful
                self.data = req.json()
                self.status = 200
                self.scene = self.newscene
                self.sceneid = self.newsceneid
                #logging.info(f"INFO: {self.url} wurde im {self.group} auf Szene {self.scene} mit ID: {self.sceneid} geschaltet")
            else:
                self.status = 500
                self.failure = req.text
            self.status_code = req.status_code
        else:
            self.failure = f"{self.group} is not set."
            self.status = 500


    def __next_scene(self) -> None:
        """ get Scenes from Hue for Group (room)
        """
        self.get_scenes()
        #print(self.scenes)
        if len(self.scenes) > 0:
            idx = list(self.scenes.values()).index(self.scene)
            sidx = len(self.scenes)
            if idx == (sidx - 1):
                self.newsceneid = list(self.scenes.keys())[0]
                self.newscene = list(self.scenes.values())[0]
            else:
                idx = idx + 1
                self.newsceneid = list(self.scenes.keys())[idx]
                self.newscene = list(self.scenes.values())[idx]
        else:
            self.failure = f"Could not find {self.scene} in Scenes."
            self.status = 500
        if isinstance(self.group, (str, int)) and self.newsceneid is not None:
            self.payload = '{ "scene": ' + "\"" + self.newsceneid + "\"" + ' }'
            headers = dict(zip(list(self.header1.split(",")), list(self.header2.split(","))))
            req = requests.put(f"{self.__url}/groups/{self.groupadd}/action", data = self.payload, headers=headers, verify=False, timeout=15)
            status = list(req.json()[0].keys())[0]
            if req.status_code == 200 and status == 'success':
                # config was successful
                self.data = req.json()
                self.status = 200
                self.scene = self.newscene
                self.sceneid = self.newsceneid
                #logging.info(f"INFO: {self.url} wurde im {self.group} auf Szene {self.newscene} mit ID: {self.newsceneid} geschaltet")
            else:
                self.status = 500
                self.failure = req.text
            self.status_code = req.status_code
        else:
            self.failure = f"Group: {self.group} or NewSceneid: {self.newsceneid} is not set."
            self.status = 500

    def prev_sceneee(self) -> None:
        try:
            if isinstance(self.group, (str, int)) and isinstance(self.scene, str):
                req = requests.get(f'{self.__url}/scenes/', verify=False, timeout=15)
                print(req.status_code)
                #if isinstance(self.group, str):
                names = []
                ids = []
                #print(req.json())
                for key, value in req.json().items():
                    #if re.search(f'^{self.group}$', entry[1]['name']) is not None:
                    if re.search(f'{self.scene}', value.get('name')) is not None:
                        names.append(value.get('name'))
                        ids.append(key)
                if len(names) == 1:
                    self.sceneid = ids[0]
                    self.status = 200
                    self.scene = names[0]
                    self.payload = '{ "scene": ' +  self.sceneid + ' }'
                    headers = dict(zip(list(self.header1.split(",")), list(self.header2.split(","))))
                    req = requests.put(f"{self.__url}/groups/{self.groupadd}/action", data = self.payload, headers=headers, verify=False, timeout=15)
                    status = list(req.json()[0].keys())[0]
                    if req.status_code == 200 and status == 'success':
                        # config was successful
                        self.data = req.json()
                        self.status = 200
                        logging.info(f"INFO: {self.url} wurde im {self.group} auf Szene {self.scene} mit ID: {self.sceneid} geschaltet")
                    else:
                        self.status = 500
                    self.status_code = req.status_code
                elif len(names) == 0:
                    self.failure = f"We cannot find any scene name matching {self.scene}"
                    self.status = 500
                else:
                    self.failure = f"We have found {len(names)} entries {names} instead of 1."
                    self.status = 500
                print(names, ids)
            if not isinstance(self.sceneid, str):
                self.failure = f"Could not find address{self.scene} in {self.url}"
        except Exception as e:
            self.failure = f"Exception in prev_scene {e}"
            self.status = 500


