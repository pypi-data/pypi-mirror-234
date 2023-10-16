"""Module for all other stuff like inverter, heating, water and so on"""
from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import re
from datetime import datetime
import time
import serial
from .knx import KnxDict
import logging
import inspect
from .credauth import Cred as Cra
import os
import urllib3.exceptions
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#logging.basicConfig(filename="/scripts/legacy/scripts/logs/kostal-piko-time-chk.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

credentials = '/etc/Credentials/credentials.csv'
host = "https://eibport"

def get_aqaperla_stats():
    # BWT_AQA_PERLA_S CMD_SAEULE1_SOLLKAPAZITAET            0x02 = 2   
    # BWT_AQA_PERLA_S CMD_SAEULE2_SOLLKAPAZITAET            0x03 = 3   
    # BWT_AQA_PERLA_S CMD_MAX_DURCHFLUSS_HEUTE_LITER        0x05 = 5   
    # BWT_AQA_PERLA_S CMD_MAX_DURCHFLUSS_GESTERN_LITER      0x06 = 6   
    # BWT_AQA_PERLA_S CMD_MAX_DURCHFLUSS_SEIT_IBN_LITER     0x07 = 7   
    # BWT_AQA_PERLA_S CMD_Wasser_Verbrauch_24h			    0x08 = 8   
    # BWT_AQA_PERLA_S CMD_VERBRAUCH_SEIT_IBN                0x10 = 16
    # BWT_AQA_PERLA_S CMD_REGENERATIONEN_SEIT_IBN           0x11 = 17  
    # BWT_AQA_PERLA_S CMD_SALZVERBRAUCH_GRAMM_SEIT_IBN      0x13 = 19  
    # BWT_AQA_PERLA_S CMD_Wasser_Kapazität Säule 1          0x25 = 37  
    # BWT_AQA_PERLA_S CMD_Wasser\Kapazität Säule 2          0x26 = 38  
    # BWT_AQA_PERLA_S CMD_ALARM                             0x20 = 32  
    try:
        counter = 0
        output = {}
        # define serial port and get data from aqaperla
        ser_port = "/dev/ttyACM0"
        ser_speed = 19200
        ser = serial.Serial(ser_port, ser_speed, timeout=0.5)
        logging.info(f"{serial.name} connected")
        cmds = [0x02, 0x03, 0x05, 0x06, 0x07, 0x08, 0x10, 0x11, 0x13, 0x25, 0x26, 0x12, 0x19, 0x15, 0x21, 0x24] # list of all commands to execute
        cmds_name = ["SAEULE1_SOLLKAPAZITAET", "SAEULE2_SOLLKAPAZITAET", "MAX_DURCHFLUSS_HEUTE_LITER", "MAX_DURCHFLUSS_GESTERN_LITER","MAX_DURCHFLUSS_SEIT_IBN_LITER", "Wasser_Verbrauch_24h", "VERBRAUCH_SEIT_IBN", "REGENERATIONEN_SEIT_IBN", "SALZVERBRAUCH_GRAMM_SEIT_IBN", "SAEULE1_RESTKAPAZITAET", "SAEULE2_RESTKAPAZITAET", "REGENERATIONEN_SEIT_SERVICE", "SOFTWARE_VERSION", "IBN_DATUM", "LOG", "KW"]
        for command in cmds:
            ser.flushInput()  #flush input buffer, remove all entries
            ser.flushOutput() #flush output buffer, abort and remove all entries in buffer

            # define start and stop bytes
            start_byte = 0x0D
            stop_byte = 0x0A

            value = 0

            collection = 0
            collection = start_byte + command + value
            run = bytearray([start_byte, command, value, collection, stop_byte])

            # run command in Aqa Perla
            ser.write(run)

            # read results
            results = ser.read(size=256)

            # calculate integers
            result = results[3] + results[4]*256
            logging.info(f"{cmds_name[counter]}={result}")
            output[cmds_name[counter]] = result
            counter += 1

        # close connection
        ser.close()
    except Exception as e:
        logging.error(f"Exception in {inspect.stack()[0][3]}: {e}")
        try:
            ser.close()
        except Exception as e:
            logging.error(f"Exception while closing serial connection in {inspect.stack()[0][3]}: {e}")

def get_kostal_energy(server="kostal", URL="http://kostal/index.fhtml") -> bool:
    output = []
    row = Cra(host=server, usage="html")
    username, password = row["user"], row["password"]
    req = requests.get(URL, auth=HTTPBasicAuth(username, password))
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")

        for i in "Gesamtenergie", "Tagesenergie", "aktuell":
            try:
                #x = soup.find(text=re.compile(i)).find_next().find(text=re.compile('\d')).split()[0]
                # Find i in the html output, needs to be searched with re
                x = soup.find(text=re.compile(i)).find_next().get_text(strip=True)
                #print(i, x)
                if re.match(".*energie", i):
                    output.append(f"{i}: {x} kWh")
                else:
                    output.append(f"{i}: {x} W")
            except Exception as e:
                #print("not")
                logging.error(f"Exception: {e}")
                continue
        logging.info(output)

        Spannung = " ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[1].split()[0:3])
        Strom = " ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[1].split()[6:9])
        logging.info(f"String 2: Spannung: {Spannung} Strom: {Strom}")
        Spannung2 = " ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[2].split()[0:3])
        Strom2 = " ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[2].split()[6:9])
        logging.info(f"String 2: Spannung: {Spannung2} Strom: {Strom2}")

        for i in 1,2,3:
            #print(f"Ausgangsleistung L{i}:")
            #print(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[i].split()[3:6])
            if i == 3:
                Spannung = " ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[i].split()[0:3])
                Leistung = " ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[i].split()[3:6])
                logging.info(f"Ausgangsleistung L{i}: Spannung: {Spannung} Leistung: {Leistung}")
            else:
                a = re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[i].split()[3:6]
                #print(" ".join(a))
                Spannung = (" ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[i].split()[3:6]))
                Leistung = (" ".join(re.split(" L\d", " ".join(soup.get_text().encode().decode("utf-8").split()))[i].split()[9:12]))
                logging.info(f"Ausgangsleistung L{i}: Spannung: {Spannung} Leistung: {Leistung}")

        #print(output)
        return True
    return False

def get_chunk(bytes=400):
    """Get chunk will give you x bytes from a http request 

    Returns:
        header or False
    """    
    try:
        with requests.get(url, stream=True, auth=HTTPBasicAuth(username, password)) as r:
            header = next(r.iter_content(chunk_size=bytes))
            return header
    except Exception as e:
        return False
    
def kostal_get_current_time() -> bool:
    """Get current time from Kostal inverter and send message via eibport/push/mail if time is different to current time

    Returns:
        bool: _description_
    """    
    acttime = 0
    header = get_chunk()
    if header:
        data = header.decode("utf-8")
        for line in data.splitlines():
            if 'akt. Zeit' in line:
                acttime = int(line.split()[-1])
        tsnow = int(datetime.now().timestamp())
        diff = tsnow - acttime
        if diff > 86400:
            ts = hex(int(acttime)).strip("0x")
            eibp = KnxDict(knxint=19400, length_id=8)
            eibp.set_knx(value=ts)
            if eibp.status == 200:
                logging.info("Kostal Piko has wrong time, diff is {} seconds between current and Kostal time {}.".format(diff,acttime))
                # wait for 24 hours to check again and send email again, if issue persists
                #time.sleep(86400)
                return False
            else:
                logging.info("Eibport is not available it seems, wait 60 Seconds and try again")
                #time.sleep(60)
                return False
        return True

