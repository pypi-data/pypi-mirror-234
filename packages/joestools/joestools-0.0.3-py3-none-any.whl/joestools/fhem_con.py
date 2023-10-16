'''API from joestools for connection to fhem servers at home.'''
from dataclasses import dataclass, field
import time
import logging
from datetime import datetime
import re
import fhem
from .credauth import cred
from .common import DefaultDict
import subprocess
import sys
from io import TextIOWrapper, BytesIO


@dataclass
class FhemCon(DefaultDict):
    """Control FHEM

    Args:
        DefaultDict (_type_): _description_
    """
    host: str | None = None
    port: int = 8084
    protocol: str = "https"
    search: str | None = None
    device: str | None =  None
    deviceo: str | None = None
    pca301: dict = field(default_factory=dict)
    readings: str | None = None
    jeelink: str | None = None
    jeelinkoutage: int | None = None
    status: int = 500
    status_code: int = 500
    failure: str = ""
    runtime: float = -1

    def __post_init__(self):
        start = time.time()
        #if self.get_Credentials() and not self.check_Connection():
        #self.failure = f"check_Connection had issues. {self.check_Connection()}"
        self.get_credentials()
        self.check_connection()
        end = time.time()
        self.runtime = round(end - start, 2)

    def get_credentials(self) -> bool:
        """Get Credentials for host

        Returns:
            bool: Successful or Not
        """
        try:
            row = cred('fhem')
            self.__pwd, self.__user = row['password'], row['username']
            return True
        except Exception as e:
            self.failure = f"get_Credentials failed with {e}"
            self.status = 500
            return False

    def check_connection(self) -> bool:
        """Check if Connection to host is up or reestablish session

        Returns:
            bool: _description_
        """
        # pyfhem1
        try:
            if self.__connection.connected() is False:
                self.__connection.connect()
                if self.__connection.connected() is True:
                    self.status = 200
                    return True
                else:
                    return False
            else:
                self.status = 200
        except Exception as e:
            self.__connection = fhem.Fhem(self.host,
                                            port = self.port,
                                            protocol = self.protocol,
                                            csrf=True,
                                            username = self.__user,
                                            password = self.__pwd,)
            self.__connection.connect()
            if self.__connection.connected():
                self.failure = ""
                self.status = 200
                return True
            else:
                self.failure = "Not connected"
                self.status = 500
                return False

    def check_pwrJee(self) -> None:
        """Check PwrJee is working

        Returns:
            bool: _description_
        """
        nowts = datetime.timestamp(datetime.now())
        self.check_connection()
        #for value in self.__connection.get_internals('Pwrjee_TIME', name="PCA301.*").values():
        #    d = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        #    dts = datetime.timestamp(d)
        dts = self.__connection.get_internals(name=f"{self.jeelink}")
        timestr = self.jeelink + "_TIME"
        diff = dts[self.jeelink][timestr] - nowts
        if diff >= 300:
            # jeelink is running out of time and fix is needed
            if dts[self.jeelink]["STATE"] == 'initialized':
                init = self.__connection.send_cmd(f"get {self.jeelink} initJeeLink")
                print(init)
                time.sleep(5)
                get = self.__connection.get_internals(name=f"{self.jeelink}")
                print(get)
                self.jeelinkoutage = 1
                # send E-Mail about it
        else:
            # jeelink is normal
            self.jeelinkoutage = 0

    def get_name(self) -> str:
        """Get Name from Fhem Host for self.device

        Returns:
            str: Name of Fhem Device
        """
        self.check_connection()
        devices = self.__connection.get_readings('state')
        #print(devices)
        special_char_map = {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss'}
        found = []
        for device in devices:
            if self.device.translate(special_char_map) in device:
                found.append(device)
        if len(found) > 1:
            return f"We have found more than 1 device: {found}, please choose one of them."
        else:
            return found[0]

    def get_status(self, value: str ="state") -> str:
        """Get Status of Device

        Returns:
            str: State of Device
        """
        self.check_connection()
        if "PCA301" in self.device:
            self.status = self.__connection.get_device_reading(self.device, value)
            #self.status = self.__connection.get_device_reading(self.device, "state", value_only=True)
            return self.status
    
    def set_status(self, value: str | None = None) -> None:
        """Set Status of Device
        """
        self.check_connection()
        if "PCA301" in self.device:
            if isinstance(value, str):
                if value == "True":
                    value = "on"
                elif value == "False":
                    value = "off"
            elif isinstance(value, bool):
                if value is True:
                    value = "on"
                elif value is False:
                    value = "off"
            else:
                return "Please use value=True/False,on/off to set a device."
            #send = self.__connection.send_cmd(f"set {self.device} {value}")
            
            #proc = subprocess.Popen(["python", "-c", "import writer; writer.write()"], stdout=subprocess.PIPE)
            #out = proc.communicate()[0]
            # setup the environment
            #old_stdout = sys.stdout
            #sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

            send = self.__connection.send_cmd(f"set {self.device} {value}")
            #print(type(send))
            # get output
            #sys.stdout.seek(0)      # jump to the start
            #send1 = sys.stdout.read() # read output
            
            # restore stdout
            #sys.stdout.close()
            #sys.stdout = old_stdout

            if re.match(b"exception|unknown|Unknown|Exception", send) is None:
            #if "exception" in send:
                self.status = 200
            else:
                #print("da")
                self.failure = send
                self.status = 500
            #print(f"Send: {send1} {send}")

    def get_power(self, device: str = "empty") -> int:
        """Get Power Uasage of Device

        Returns:
            int: Power Usage of Device
        """
        self.check_connection()
        if self.device is not None or "PCA301" in device or "PCA301" in self.device:
            self.device = device
            self.status = self.__connection.get_device_reading(self.device, "power")
            #self.status = self.__connection.get_device_reading(self.device, "state", value_only=True)
            return self.status

    def get_all_pca301(self, value=None) -> dict:
        """Get all PCA301 Sockets with related value(s)
           value = None => all Values
           value = "power" => all PCA301 Sockets with power output
           value = "consumption" => all PCA301 Sockets with consumption output
           value = "state" => state of all PCA301 Sockets
        """
        self.check_connection()
        if value is None:
            self.pca301 = self.__connection.get_readings(name="PCA301.*")
        else:
            self.pca301 = self.__connection.get_readings(value, name="PCA301.*")
        self.pca301.pop("PCA301.ntfy")
        return self.pca301

if __name__ == "__main__":
    print("ok")


#dts = fh.get_internals(filters={"state": "initialized" }, name="Pwrjee")




#fh.get_internals('Pwrjee_TIME', name="PCA301.*")
#{'PCA301_AVR_Onkyo_Wohnzimmer': datetime.datetime(2023, 2, 23, 16, 4, 23), 'PCA301_Bad_Glaetteisen': datetime.datetime(2023, 2, 23, 16, 4, 11), 'PCA301_Buero_Drucker_exHDDs_Arbeit': datetime.datetime(2023, 2, 23, 16, 4, 18), 'PCA301_Buero_Jochens_PC_usw': datetime.datetime(2023, 2, 23, 16, 4, 4), 'PCA301_Buero_Tanias_PC_usw': datetime.datetime(2023, 2, 23, 16, 4, 12), 'PCA301_Kueche_Ofen_Router_Pi': datetime.datetime(2023, 2, 23, 16, 4, 3), 'PCA301_Novus_Paul_F300': datetime.datetime(2023, 2, 23, 16, 4, 22), 'PCA301_SB_NAS_N5550': datetime.datetime(2023, 2, 23, 16, 4), 'PCA301_SB_Router_Switches_NAS': datetime.datetime(2023, 2, 23, 16, 4, 3), 'PCA301_Spuelmaschine': datetime.datetime(2023, 2, 23, 16, 4, 14), 'PCA301_TR_Aqa_Perla': datetime.datetime(2023, 2, 23, 16, 3, 56), 'PCA301_TR_HP_Micro_PIs': datetime.datetime(2023, 2, 23, 16, 4, 16), 'PCA301_TR_HP_Micro_Server': datetime.datetime(2023, 2, 23, 16, 4, 2), 'PCA301_TR_Waschmaschine_u_Trockner': datetime.datetime(2023, 2, 23, 16, 4, 9), 'PCA301_WZ_TV_AVR1': datetime.datetime(2023, 2, 23, 16, 4, 22)}
#>>> for value in fh.get_internals('Pwrjee_TIME', name="PCA301.*").values():
#...     print(value)
#... 
#2023-02-23 16:04:54
#2023-02-23 16:04:43
#2023-02-23 16:04:48
#2023-02-23 16:04:37
#2023-02-23 16:04:44
#2023-02-23 16:04:34
#2023-02-23 16:04:52
#2023-02-23 16:04:49
#2023-02-23 16:04:33
#2023-02-23 16:04:46
#2023-02-23 16:04:27
#2023-02-23 16:04:47
#2023-02-23 16:04:34
#2023-02-23 16:04:42
#2023-02-23 16:04:54


#fh.get_readings('consumption', name="PCA301.*")
#{'PCA301_AVR_Onkyo_Wohnzimmer': {'Value': 5.79, 'Time': datetime.datetime(2023, 2, 23, 3, 18, 5)}, 'PCA301_Bad_Glaetteisen': {'Value': 2.69, 'Time': datetime.datetime(2023, 2, 21, 13, 33, 5)}, 'PCA301_Buero_Drucker_exHDDs_Arbeit': {'Value': 93.91, 'Time': datetime.datetime(2023, 2, 23, 16, 1, 6)}, 'PCA301_Buero_Jochens_PC_usw': {'Value': 208.68, 'Time': datetime.datetime(2023, 2, 23, 15, 59, 22)}, 'PCA301_Buero_Tanias_PC_usw': {'Value': 87.93, 'Time': datetime.datetime(2023, 2, 23, 15, 59, 34)}, 'PCA301_Kueche_Ofen_Router_Pi': {'Value': 376.23, 'Time': datetime.datetime(2023, 2, 23, 15, 38, 21)}, 'PCA301_Novus_Paul_F300': {'Value': 85, 'Time': datetime.datetime(2023, 2, 23, 15, 55)}, 'PCA301_SB_NAS_N5550': {'Value': 117.7, 'Time': datetime.datetime(2022, 9, 9, 20, 49, 32)}, 'PCA301_SB_Router_Switches_NAS': {'Value': 0, 'Time': datetime.datetime(2023, 1, 18, 20, 27, 30)}, 'PCA301_Spuelmaschine': {'Value': 333.91, 'Time': datetime.datetime(2023, 2, 23, 0, 35, 41)}, 'PCA301_TR_Aqa_Perla': {'Value': 0.18, 'Time': datetime.datetime(2023, 2, 21, 19, 34, 42)}, 'PCA301_TR_HP_Micro_PIs': {'Value': 5.74, 'Time': datetime.datetime(2023, 2, 23, 15, 32, 11)}, 'PCA301_TR_HP_Micro_Server': {'Value': 8.74, 'Time': datetime.datetime(2023, 2, 18, 16, 0, 49)}, 'PCA301_TR_Waschmaschine_u_Trockner': {'Value': 574.08, 'Time': datetime.datetime(2023, 2, 21, 11, 56, 5)}, 'PCA301_WZ_TV_AVR1': {'Value': 33.81, 'Time': datetime.datetime(2023, 2, 23, 5, 38, 3)}}
#>>> 

#>>> fh.get_device_reading("PCA301_Spuelmaschine", 'consumption')
#{'Value': 333.91, 'Time': datetime.datetime(2023, 2, 23, 0, 35, 41)}
#>>> 

#>>> fh.get_readings(name="PCA301.*")
#{'PCA301.ntfy': {'state': {'Value': 'active', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 15)}, 'triggeredByDev': {'Value': 'Heizung', 'Time': datetime.datetime(2023, 2, 23, 9, 46, 3)}, 'triggeredByEvent': {'Value': 'heatSourceMotor: off', 'Time': datetime.datetime(2023, 2, 23, 9, 46, 3)}}, 'PCA301_AVR_Onkyo_Wohnzimmer': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 5.79, 'Time': datetime.datetime(2023, 2, 23, 3, 18, 5)}, 'consumptionTotal': {'Value': 260.129999999895, 'Time': datetime.datetime(2023, 2, 23, 3, 18, 5)}, 'power': {'Value': 0, 'Time': datetime.datetime(2023, 2, 23, 3, 20, 6)}, 'state': {'Value': 'off', 'Time': datetime.datetime(2023, 2, 23, 3, 20, 5)}, 'waitforACK': {'Value': 'ACK:off', 'Time': datetime.datetime(2023, 2, 23, 3, 20, 5)}}, 'PCA301_Bad_Glaetteisen': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 2.69, 'Time': datetime.datetime(2023, 2, 21, 13, 33, 5)}, 'consumptionTotal': {'Value': 9.71999999999991, 'Time': datetime.datetime(2023, 2, 21, 13, 33, 5)}, 'power': {'Value': 0, 'Time': datetime.datetime(2023, 2, 23, 15, 47, 37)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 12)}, 'waitforACK': {'Value': 'ACK:off', 'Time': datetime.datetime(2022, 3, 19, 20, 20, 37)}}, 'PCA301_Buero_Drucker_exHDDs_Arbeit': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 93.9, 'Time': datetime.datetime(2023, 2, 23, 15, 43, 31)}, 'consumptionTotal': {'Value': 1993.87999999986, 'Time': datetime.datetime(2023, 2, 23, 15, 43, 31)}, 'power': {'Value': 34.4, 'Time': datetime.datetime(2023, 2, 23, 15, 56, 22)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 2, 0, 9, 19)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2019, 1, 3, 0, 40, 59)}}, 'PCA301_Buero_Jochens_PC_usw': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 208.67, 'Time': datetime.datetime(2023, 2, 23, 15, 53, 36)}, 'consumptionTotal': {'Value': 4959.36000003923, 'Time': datetime.datetime(2023, 2, 23, 15, 53, 36)}, 'power': {'Value': 106.2, 'Time': datetime.datetime(2023, 2, 23, 15, 56, 17)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 12)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2019, 3, 19, 10, 27, 42)}}, 'PCA301_Buero_Tanias_PC_usw': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 87.92, 'Time': datetime.datetime(2023, 2, 23, 15, 55, 24)}, 'consumptionTotal': {'Value': 44339.2900000835, 'Time': datetime.datetime(2023, 2, 23, 15, 55, 24)}, 'power': {'Value': 162.6, 'Time': datetime.datetime(2023, 2, 23, 15, 55, 55)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 33)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2018, 2, 15, 16, 54, 7)}}, 'PCA301_Kueche_Ofen_Router_Pi': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 376.23, 'Time': datetime.datetime(2023, 2, 23, 15, 38, 21)}, 'consumptionTotal': {'Value': 1695.40999999939, 'Time': datetime.datetime(2023, 2, 23, 15, 38, 21)}, 'power': {'Value': 10.1, 'Time': datetime.datetime(2023, 2, 23, 15, 55, 38)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 13)}, 'waitforACK': {'Value': 'ACK:off', 'Time': datetime.datetime(2017, 8, 27, 3, 42, 21)}}, 'PCA301_Novus_Paul_F300': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 85, 'Time': datetime.datetime(2023, 2, 23, 15, 55)}, 'consumptionTotal': {'Value': 2713.25000001041, 'Time': datetime.datetime(2023, 2, 23, 15, 55)}, 'power': {'Value': 72, 'Time': datetime.datetime(2023, 2, 23, 15, 56, 2)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 14)}}, 'PCA301_SB_NAS_N5550': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 117.7, 'Time': datetime.datetime(2022, 9, 9, 20, 49, 32)}, 'consumptionTotal': {'Value': 515.589999999697, 'Time': datetime.datetime(2022, 9, 9, 20, 49, 32)}, 'power': {'Value': 0, 'Time': datetime.datetime(2022, 9, 9, 20, 49, 32)}, 'state': {'Value': 'off', 'Time': datetime.datetime(2022, 9, 9, 20, 49, 32)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2023, 2, 6, 11, 23, 26)}}, 'PCA301_SB_Router_Switches_NAS': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 0, 'Time': datetime.datetime(2023, 1, 18, 20, 27, 30)}, 'consumptionTotal': {'Value': 6820.1200000556, 'Time': datetime.datetime(2023, 1, 18, 20, 27, 30)}, 'power': {'Value': 0, 'Time': datetime.datetime(2023, 1, 18, 20, 28, 14)}, 'state': {'Value': 'off', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 14)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2022, 10, 4, 18, 57, 25)}}, 'PCA301_Spuelmaschine': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 333.91, 'Time': datetime.datetime(2023, 2, 23, 0, 35, 41)}, 'consumptionTotal': {'Value': 1227.34999999948, 'Time': datetime.datetime(2023, 2, 23, 0, 35, 41)}, 'power': {'Value': 3.4, 'Time': datetime.datetime(2023, 2, 23, 15, 56, 22)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 15)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2019, 1, 3, 0, 40, 59)}}, 'PCA301_TR_Aqa_Perla': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 0.18, 'Time': datetime.datetime(2023, 2, 21, 19, 34, 42)}, 'consumptionTotal': {'Value': 976.669999999636, 'Time': datetime.datetime(2023, 2, 21, 19, 34, 42)}, 'power': {'Value': 3.5, 'Time': datetime.datetime(2023, 2, 23, 15, 56, 5)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 1, 4, 56, 27)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2022, 4, 23, 11, 17, 29)}}, 'PCA301_TR_HP_Micro_PIs': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 5.74, 'Time': datetime.datetime(2023, 2, 23, 15, 32, 11)}, 'consumptionTotal': {'Value': 4892.08000005992, 'Time': datetime.datetime(2023, 2, 23, 15, 32, 11)}, 'power': {'Value': 17.1, 'Time': datetime.datetime(2023, 2, 23, 15, 55, 54)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 15)}, 'waitforACK': {'Value': 'ACK:off', 'Time': datetime.datetime(2022, 10, 4, 18, 35, 29)}}, 'PCA301_TR_HP_Micro_Server': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 8.74, 'Time': datetime.datetime(2023, 2, 18, 16, 0, 49)}, 'consumptionTotal': {'Value': 1137.97999999936, 'Time': datetime.datetime(2023, 2, 18, 16, 0, 49)}, 'power': {'Value': 0.7, 'Time': datetime.datetime(2023, 2, 23, 15, 56, 12)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 1, 4, 56, 41)}, 'waitforACK': {'Value': 'ACK:off', 'Time': datetime.datetime(2021, 12, 12, 17, 16, 21)}}, 'PCA301_TR_Waschmaschine_u_Trockner': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 574.08, 'Time': datetime.datetime(2023, 2, 21, 11, 56, 5)}, 'consumptionTotal': {'Value': 1083.91999999938, 'Time': datetime.datetime(2023, 2, 21, 11, 56, 5)}, 'power': {'Value': 0.7, 'Time': datetime.datetime(2023, 2, 23, 15, 55, 57)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 16)}, 'waitforACK': {'Value': 'ACK:on', 'Time': datetime.datetime(2018, 2, 26, 20, 3, 32)}}, 'PCA301_WZ_TV_AVR1': {'IODev': {'Value': 'Pwrjee', 'Time': datetime.datetime(2022, 11, 25, 11, 57, 22)}, 'consumption': {'Value': 33.81, 'Time': datetime.datetime(2023, 2, 23, 5, 38, 3)}, 'consumptionTotal': {'Value': 1381.38999999927, 'Time': datetime.datetime(2023, 2, 23, 5, 38, 3)}, 'power': {'Value': 3.8, 'Time': datetime.datetime(2023, 2, 23, 15, 55, 57)}, 'state': {'Value': 'on', 'Time': datetime.datetime(2023, 2, 23, 0, 45, 16)}, 'waitforACK': {'Value': 'ACK:off', 'Time': datetime.datetime(2022, 8, 26, 22, 52, 44)}}}
#>>> 