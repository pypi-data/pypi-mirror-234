from dataclasses import dataclass
import time
import re
import ssl
import json
from typing import Union
from datetime import datetime
import lxml.etree as ET
from urllib3 import poolmanager, disable_warnings, exceptions
import requests
from requests import adapters
from .credauth import Cred
from .common import DefaultDict
disable_warnings(exceptions.InsecureRequestWarning)

KNXPROJFILE = '/etc/Credentials/knx_addresses.esfx'
EIBPORT = "https://eibport"

class TLSAdapter(adapters.HTTPAdapter):
    """Class for setting the security of the https connection down
       this is currently needed for eibport v3 with Firmware 3.9.5

    Args:
        adapters (HTTPAdapter): HTTPAdpater args
    """ 

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=0)                                                                  ')
        ctx.check_hostname = False
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ssl_context=ctx)

def eibport_req(url):
    """ Create a session object to connect to Eibport which has a reduced ciphers configuration <= Firmware 3.9.3

    Args:
        url (str): URL for eibport

    Returns:
        request: request object to communicate with eibport
    """
    session = requests.session()
    session.mount('https://', TLSAdapter())
    req = session.get(url, timeout=(10,15), verify=False)
    return req

def get_eibport(url: str) -> requests:
    """Get Data from Eibport
       currently there is an issue with the http ciphers
       of eibport firmware 3.9.5 and it is not sure
       when it will be solved. So we have to define
       a SECLEVEL=1 for the used ciphers

    Args:
        url (str): url for Eibport ressources

    Returns:
        request: request object
    """
    session = requests.session()
    session.mount('https://', TLSAdapter())
    req = session.get(url, timeout=(10,15), verify=False)
    return req


def get_knx_length_id(datatype: int) -> tuple:
    """ Get KNX length_id from datatype 

    Args:
        datatype (int): datatype of KNX File

    Returns:
        tuple: length_id, failure
    """
    length_id = -1
    failure = ""
    if datatype == 10000010:
        # EIS 1 => length_id = 1
        length_id = 1
    elif datatype == 10000150 or datatype == 10000060 or datatype == 10000140 or datatype == 10000141:
        # EIS 2, EIS 6, EIS 13, EIS 14
        # 10000021 = EIS 2
        # 10000140 = EIS 14 signed
        # 10000141 = EIS 14 unsigned
        # 10000150 = EIS 15
        # 10000060 = EIS 6
        length_id = 5
    elif datatype == 10000050 or datatype == 10000101:
        # EIS 5, EIS 10
        # 10000050 = EIS 5
        # 10000101 = EIS 10 unsigned
        length_id = 6
    elif datatype == 10000040:
        # EIS 4
        # 10000040 = EIS 4
        length_id = 7
    elif datatype == 10000111 or datatype == 10000090:
        # EIS 9, EIS 11
        # 10000090 = EIS 9
        # 10000111 = EIS 11 unsigned
        length_id = 8
    elif datatype == 0:
        # 0 = unknown
        length_id = 999
        failure = f"Datatype {datatype} is unknown. Please define it first."
    else:
        length_id = 999
        failure = f"Datatype {datatype} is not configured in this python script. Please define it first."
    return length_id, failure

def set_knx_addrs(devices: dict) -> str:
    """ Set KNX Addresses for several devices with several states

    Args:
        devices (dict): _description_

    Returns:
        str: _description_
    """
    credentials = Cred(host=EIBPORT, user="status")
    if credentials.status == 200:
        configstring = credentials.configstring
    else:
        failure = f"Configstring could not be found in Cred, status {credentials.status}"
        return failure
    object = 0
    for device in devices.keys():
        if devices[device].status == 200:
            knxint = devices[device].knxint
            length_id = devices[device].length_id
            value = devices[device].value
            try:
                data
            except NameError:
                data = f"{EIBPORT}/webif/ComObjectState?action=setData&address={knxint}&length_id={length_id}&value={value}"
            else:
                data = f"{data}&address={knxint}&length_id={length_id}&value={value}"
    return data

def get_knx_names(name) -> json:
    """ Get KNX Names from name

    Args:
        name (_type_): _description_

    Returns:
        json: _description_
    """
    back = {}
    tree = ET.parse(KNXPROJFILE)
    start = 1
    for child in tree.iter('address'):
        obj = child.find('name')
        if name.count("/") == 2:
            name = obj.text
        if re.findall(f"{name}".lower(), obj.text.lower()):
            back[start] = obj.text
            start += 1
    #return json.dumps(dict(back))
    return back
    #return json(back)

@dataclass
class KnxDict(DefaultDict):
    """ Knx Dict for knx devices

    Args:
        DefaultDict (_type_): _description_

    Returns:
        _type_: _description_
    """
#class knx_dict(default_dict):

    name: str
    status: int = 500
    failure: str = ""
    addr: str = ""
    value: str = ""
    knxint: int = -1
    datatype: int = -1
    length_id: int = -1
    raddr: int = -1
    generation: str = ""
    timestamp32: int = -1
    timestamp: str = ""
    runtime: float = -1
    get_knx_status_runtime: int = -1
    set_knx_runtime: int = -1
    get_knx_addr_runtime: int = -1
    get_knx_int_runtime: int = -1
    get_knx_attrib_runtime: int = -1

    def __post_init__(self):
        start = time.time()
        if self.get_Credentials():
            self.get_knx_attrib()

            if self.knxint > 0:
                self.addr = self.get_knx_addr(self.knxint)
                self.get_knx_status()
            else:
                self.failure = f"{self.name} is not available in file {KNXPROJFILE}"
        end = time.time()
        self.runtime = round(end - start, 2)

    def get_Credentials(self) -> Union[None, bool]:
        credentials = Cred(host=EIBPORT, usage="eibport")
        #print(f"Status: {credentials}")
        if credentials.status == 200:
            self.__configstring = credentials.configstring
            return True
        else:
            self.failure = f"Credentials Status: {credentials.failure}, {credentials.status}"
            return False

    def get_knx_status(self) -> None:
        """ Get KNX information from eibport
        """
        start_time = time.time()
        objstring=f"&object0={self.knxint}"
        data = f"{EIBPORT}/webif/ComObjectState?action=getData{objstring}{self.__configstring}"
        req = eibport_req(data)
        root = ET.fromstring(req.content)
        self.raddr = int(root.xpath('.//address[@requested="1"]/text()')[0])
        for text in req.text.split("\n"):
            if "generation" in text:
                self.generation = text
        if "ok" in root.xpath('.//object[@key=0]/message/text()'):
            self.value = str(root.xpath('.//object[@key=0]/value/text()')[0])
            self.timestamp32 = int(root.xpath('.//object[@key=0]/timestamp32/text()')[0]) // 1000
            self.timestamp = datetime.fromtimestamp(self.timestamp32).strftime('%d-%m-%Y %H:%M:%S')
            self.status = 200
        else:
            self.status = 500
            self.failure = f"{EIBPORT} is not reachable"
        end_time = time.time()
        self.get_knx_addr_runtime = end_time - start_time


    def set_knx(self, value: str) -> None:
        """ Set KNX Device

        Args:
            value (str): _description_
        """
        start_time = time.time()
        data = f"{EIBPORT}/webif/ComObjectState?action=setData&address={self.knxint}&length_id={self.length_id}&value={value}{self.__configstring}"
        req = eibport_req(data)
        if (req.status_code >= 200 or req.status_code <= 205) and ("exception" or "error" or "failure") not in req.text.lower():
            self.status = 200
            self.value = value
        elif req.status_code >= 200 or req.status_code <= 205:
            self.status = 500
            self.failure = f"{EIBPORT} is responding well {req.status_code} but our Request was not accepted with Error {req.text}."
        else:
            self.failure = f"{EIBPORT} is not responding well, we have got status code {req.status_code} and Error {req.text}."
        end_time = time.time()
        self.set_knx_runtime = end_time - start_time

    def get_knx_addr(self, knxint: int) -> str:
        """ Get KNX Device status

        Args:
            knxint (int): Integer Number from KNX GA Address

        Returns:
            str: address of knxint
        """
        start_time = time.time()
        maingroup = knxint / 2048
        middlegroup = ( knxint - ( maingroup * 2048 ) ) / 256 
        subgroup = ( knxint - ( ( maingroup * 2048 ) + ( middlegroup * 256 ) ) )
        self.addr = f"{int(maingroup)}/{int(middlegroup)}/{int(subgroup)}"
        end_time = time.time()
        self.get_knx_addr_runtime = end_time - start_time
        return self.addr

    def get_knx_int(self, addr: str) -> None:
        """ Get KNX Integer from address

        Args:
            addr (str): KNX GA Address
        """
        maingroup, middlegroup, subgroup = [int(entry) for entry in addr.split("/")]
        self.knxint = ( int(maingroup) * 2048 ) + ( int(middlegroup) * 256 ) + int(subgroup)
        self.status = 200

    def get_knx_attrib(self) -> None:
        """ Get KNX Attribut, transform datatype to length_id
        """
        tree = ET.parse(KNXPROJFILE)
        for child in tree.iter('address'):
            obj = child.find('name')
            if self.name.count("/") == 2:
                self.name = obj.text
            if re.match(f"^{self.name}$", obj.text) is not None:
                self.knxint = int(child.attrib['address'])
                self.datatype = int(child.find('datatype').text)
                self.length_id, self.failure = get_knx_length_id(self.datatype)
