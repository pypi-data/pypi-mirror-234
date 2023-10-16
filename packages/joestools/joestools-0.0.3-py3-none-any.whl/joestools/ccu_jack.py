"""Module to access ccu3 via ccu-jack"""
from dataclasses import dataclass
import json
import time
from typing import Union
import requests
from urllib3 import disable_warnings, exceptions
disable_warnings(exceptions.InsecureRequestWarning)

def get_ccu_data(path: str, url: str) -> requests:
    """ Get Data from CCU3 via ccu-jack API

    Args:
        path (str): href for device
        url (str, optional): _description_. Defaults to URL.

    Returns:
        requests: _description_
    """
    req = requests.get(f"{url}/{path}", verify=False, timeout=30)
    #req.status_code
    #if req.status_code >= 200 or req.status_code <= 204:
    return req

def set_ccu_data(path: str, data: json, url: str) -> requests:
    """ Set CCU Data with ccu-jack in CCU3 for given path

    Args:
        path (str): href for device
        data (json): body of request
        url (str, optional): _description_. Defaults to URL.

    Returns:
        requests: _description_
    """
    req = requests.put(f"{url}/{path}", data=data, verify=False, timeout=30)
    return req

def check_ccu_device(name: str, url: str) -> Union[str, list, None]:
    """ Check if given name is available in ccu3

    Args:
        name (str): name of the device
        url (str, optional): URL of ccu-jack. Defaults to URL.

    Returns:
        Union[str, list, None]: it can return string = 1 device found
                                              list   = 2 or more devices found
                                              none   = no device with the name found
    """
    devices = []
    found = None
    req = requests.get(f"{url}/device", verify=False, timeout=30)
    for entry in req.json()["~links"]:
        device = entry['title']
        if name.lower() in device.lower():
            found = device
            devices.append(device)
    if len(devices) > 1:
        return devices
    else:
        return found

def get_ccu_all(attribute: str = None, url: str = None) -> Union[str, dict, None]:
    """ Check all Battery States in ccu3

    Args:
        attribute (str): attribute which match on different devices
        url (str, optional): URL of ccu-jack.

    Returns:
        result: All matching devices with attribute state
    """
    if attribute is None:
        return "attribute is missing, please use for example: LOW_BAT as attribute"
    result = {}
    req = requests.get(f"{url}/~query?~path=/device/*/*/{attribute}/", verify=False, timeout=30)
    for device in req.json():
        req2 = requests.get(f"{url}/{device['~path']}/~pv", verify=False, timeout=30)
        title = device["title"].rstrip(f":0 - {attribute}")
        result[title] = req2.json()["v"]
    return result

@dataclass
class CCUJackDevice():
    """ Device, creates a ccu-jack device

    Returns:
        _type_: _description_
    """

    # pylint: disable=too-many-instance-attributes

    name: str = ""  # Name of the device
    address: str = ""  # Device-ID
    host: str = "" # CCU3 Host IP Address
    state: int = -1 # which number need to be checked for status
    state1: int = -1 # which number need to be checked for status
    rel: str = ""   # which relation
    title: str = ""   # title in ccu-jack
    path: str = "" # path for request to ccu-jack
    type: str  = "" # HmIP-SRH, usw.
    status: int = 500 # status of the overall actions
    failure: str = ""
    firmware: str = "" # firmware of the device
    #children: List = field(default_factory=[0]) # possible ressources
    children: list = list[0] # possible ressources
    value: int = -1 # value is the string of ValueList index
    #value_list: List = field(default_factory=[0]) # ValueList out of 1/STATE
    value_list: list = list[0] # ValueList out of 1/STATE
    ts_ccuj: int = -1 # timestamp sometimes 0, if reboot happend and no change
    v_ccuj: int = -1 # value is index of ValueList state
    s_ccuj: int = -1 # Low Battery or Communication Issues for example is 100, 0 is good
    batcom: bool = True # are there any battery or communication issues
    runtime: float = -1

    def __post_init__(self):
        start = time.time()

        self.host = f"https://{self.host}:2122"
        # get type, address, firmware, children
        #self.get_address()
        #if self.status == 200:
        #    self.get_type_state()
        #if self.status == 200:
        #    self.get_status()

        end = time.time()
        self.runtime = end - start

    def get_address(self) -> None:
        """ get address of device
        """
        self.path = "device"
        req = get_ccu_data(self.path, self.host)
        if req.status_code == 200:
            for entry in req.json()['~links']:
                if self.name == entry['title']:
                    self.address = entry['href']
                    self.rel = entry['rel']
                    self.title = entry['title']
                    self.status = 200
        else:
            self.failure = req.text
            self.status = req.status_code
        if self.address == "":
            check = check_ccu_device(self.name, self.host)
            if isinstance(check, str):
                # one device was found, which we can use, even if the name was not complete
                self.name = check
                self.status = 200
                req = get_ccu_data(self.path, self.host)
                if req.status_code == 200:
                    for entry in req.json()['~links']:
                        if self.name == entry['title']:
                            self.address = entry['href']
                            self.rel = entry['rel']
                            self.title = entry['title']
                            self.status = 200
                else:
                    self.failure = req.text
                    self.status = req.status_code
            elif isinstance(check, list):
                self.failure = f"We have found more than one entry in list {check}."
                self.status = 500
            else:
                self.failure = f"{self.name} was not found in {self.host}."
                self.status = 404

    def get_type_state(self) -> None:
        """ get type state, type, firmware, children
        """
        # get type, address, firmware, children
        path = f"device/{self.address}"
        req = get_ccu_data(path, self.host)
        if req.status_code == 200:
            try:
                self.type = req.json()['type']
                self.firmware = req.json()['firmware']
                self.children = req.json()['children']
                # we need to get the ValueList from the device
                if self.type == "HMIP-PSM":
                    self.state = 3
                    self.state1 = 6
                    #self.get_hmip_psm()
                elif self.type == "HmIP-STHD":
                    #print("hier")
                    self.state = 1
                    self.state1 = 0
                    #self.get_hmip_sthd()
                    #CCUTemperature.get_hmip_sthd()
                #elif self.type == "HmIP-SRH":
                #    self.state = 1
                #    self.get_hmip_srh()
                else:
                    self.state = 1
                    #self.get_hmip_srh()
                self.status = 200
            except:
                self.status = 500
                self.failure = req.text


    def get_status(self) -> None:
        """ get general status, like battery, match with value_list if HMIP-SRH is used
        """
        if self.type == "HmIP-STHD":
            path = f"device/{self.address}/{self.state1}/LOW_BAT/~pv"
        elif self.type == "HmIP-MOD-HO":
            path = f"device/{self.address}/{self.state}/DOOR_STATE/~pv"
        else:
            path = f"device/{self.address}/{self.state}/STATE/~pv"
        req = get_ccu_data(path, self.host)
        #print(req.text)
        if req.status_code == 200:
            self.ts_ccuj = req.json()["ts"]
            self.v_ccuj = req.json()["v"]
            if self.type == "HmIP-SRH" or self.type == "HmIP-MOD-HO":
                self.value = self.value_list[self.v_ccuj]
            else:
                self.value = req.json()["v"]
            self.s_ccuj = req.json()["s"]
            if self.s_ccuj == 0:
                self.batcom = False # False => no communication or battery issues
        else:
            self.failure = req.text
        self.status = req.status_code


    def set(self, value:str) -> None:
        """set device

        Args:
            value (str): on/off True/False

        Returns:
            _type_: request
        """
        # req = requests.put(f"{url}/device/{link}/3/STATE/~pv", json={"v":True}, verify=False)
        path = f"device/{self.address}/{self.state}/STATE/~pv"
        if value == "on":
            value = True
        elif value == "off":
            value = False
        payload = json.dumps({"v": value})
        req = set_ccu_data(path, payload)
        if req.status_code == 200:
            self.get_status()
        else:
            self.failure = req.text
        self.status = req.status_code
        #
        # return req


@dataclass
class CCUSRH(CCUJackDevice):
    """ Device, creates a ccu-jack device Temperature

    Returns:
        _type_: _description_
    """

    # pylint: disable=too-many-instance-attributes

    temperature: float = -1
    temperature_status: int = -1
    temperature_ts: int = -1
    humidity: int = -1
    humidity_status: int = -1
    humidity_ts: int = -1

    def __post_init__(self):
        start = time.time()

        self.host = f"https://{self.host}:2122"
        # get type, address, firmware, children
        self.get_address()
        #self.name 
        if self.status == 200:
            self.get_type_state()
            if "HmIP-SRH" not in self.type:
                self.failure = f"Wrong Class CCUSRH choosen for type: {self.type}."
            else:
                self.get_hmip_sthd()
        if self.status == 200:
            self.get_status()

        end = time.time()
        self.runtime = end - start

    def get_hmip_sthd(self) -> None:
        """ get hmip sthd (Temperature) values"""
        for entry in "ACTUAL_TEMPERATURE", "HUMIDITY":
            path = f"device/{self.address}/{self.state}/{entry}/~pv"
            req = get_ccu_data(path, self.host)
            if req.status_code == 200:
                if entry == "ACTUAL_TEMPERATURE":
                    self.temperature = req.json()["v"]
                    self.temperature_status = req.json()["s"]
                    self.temperature_ts = req.json()["ts"]
                elif entry == "HUMIDITY":
                    self.humidity = req.json()["v"]
                    self.humidity_status = req.json()["s"]
                    self.humidity_ts = req.json()["ts"]
                self.status = 200
            else:
                self.failure = req.text
                self.status = req.status_code


@dataclass
class CCUPSM(CCUJackDevice):
    """ Device, creates a ccu-jack device

    Returns:
        _type_: _description_
    """

    # pylint: disable=too-many-instance-attributes

    power: float = -1
    power_status: int = -1
    power_ts: int = -1
    energy: float = -1
    energy_status: int = -1
    energy_ts: int = -1
    energy_overflow: float = -1
    energy_overflow_status: int = -1
    energy_overflow_ts: int = -1

    def __post_init__(self):
        start = time.time()

        self.host = f"https://{self.host}:2122"
        # get type, address, firmware, children
        self.get_address()
        print(self.address)
        if self.status == 200:
            print("here")
            self.get_type_state()
            print(self.type)
            if "HMIP-PSM" not in self.type:
                self.failure = f"Wrong Class CCUSRH choosen for type: {self.type}."
            else:
                self.get_hmip_psm()
        if self.status == 200:
            self.get_status()

        end = time.time()
        self.runtime = end - start

    def get_hmip_psm(self) -> None:
        """ get hmip psm values
        """
        # Power Sockets
        for entry in "POWER", "ENERGY_COUNTER", "ENERGY_COUNTER_OVERFLOW":
            path = f"device/{self.address}/{self.state1}/{entry}/~pv"
            req = get_ccu_data(path, self.host)
            if req.status_code == 200:
                if entry == "POWER":
                    self.power = req.json()["v"]
                    self.power_status = req.json()["s"]
                    self.power_ts = req.json()["ts"]
                elif entry == "ENERGY_COUNTER":
                    self.energy = req.json()["v"]
                    self.energy_status = req.json()["s"]
                    self.energy_ts = req.json()["ts"]
                elif entry == "ENERGY_COUNTER_OVERFLOW":
                    self.energy_overflow = req.json()["v"]
                    self.energy_overflow_status = req.json()["s"]
                    self.energy_overflow_ts = req.json()["ts"]
                self.status = 200
            else:
                self.failure = req.text
                self.status = req.status_code

    def get_all_psm(self) -> list:
        """Get all HMIP-PSM Sockets with title HMIP-PSM from CCU-Jack"""
        output = []
        path = "device"
        req = get_ccu_data(path, self.host)
        if req.status_code == 200:
            for entry in req.json()['~links']:
                if "HMIP-PSM" in entry['title']:
                    output.append(entry["title"])
        else:
            output.append(f"Status Code was {req.status_code}")
        return output


@dataclass
class CCUModHo(CCUJackDevice):
    """ Device, creates a ccu-jack device for Garage door

    Returns:
        _type_: _description_
    """

    # pylint: disable=too-many-instance-attributes

    def __post_init__(self):
        start = time.time()
        self.host = f"https://{self.host}:2122"

        # get type, address, firmware, children
        self.get_address()
        if self.status == 200:
            self.get_type_state()
            if "MOD-HO" not in self.type:
                self.failure = f"Wrong Class CCUSRH choosen for type: {self.type}."
            else:
                self.get_hmip_modho()
        if self.status == 200:
            self.get_status()

        end = time.time()
        self.runtime = end - start

    def get_hmip_modho(self) -> None:
        """ get hmip srh values (Garage Door)"""
        # Window Contacts
        path = f"device/{self.address}/{self.state}/DOOR_STATE"
        req = get_ccu_data(path, self.host)
        if req.status_code == 200:
            self.value_list = req.json()["valueList"]
            self.status = 200
        else:
            self.failure = req.text
            self.status = req.status_code
    
    def set_door_state(self, value:str) -> None:
        """set device door state

        Args:
            value (str): NOP|OPEN|STOP|CLOSE|PARTIAL_OPEN
 
        Returns:
            _type_: request
        """
        # req = requests.put(f"{url}/device/{link}/3/STATE/~pv", json={"v":True}, verify=False)
        path = f"device/{self.address}/{self.state}/DOOR_COMMAND/~pv"
        if not value.isnumeric():
            for idx, name in enumerate(['CLOSED', 'OPEN', 'VENTILATION_POSITION', 'POSITION_UNKNOWN']):
                if value in name:
                    value = idx
        payload = json.dumps({"v": value})
        req = set_ccu_data(path, payload)
        if req.status_code == 200:
            self.failure = req.status_code
            self.v_ccuj = value
        else:
            self.failure = req.status_code

def __main__():
    """ Main Function
    """
