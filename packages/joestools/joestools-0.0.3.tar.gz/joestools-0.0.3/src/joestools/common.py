"""Module for common tasks"""
from collections import defaultdict
from dataclasses import dataclass, field
import re
import time
import requests
from requests.auth import HTTPBasicAuth
import logging
from flask import request, copy_current_request_context
#from joestools import knx
from werkzeug import datastructures as ds
import json
import smtplib
import mimetypes
import socket
from email.mime.text import MIMEText
from email.utils import formatdate
from email.message import EmailMessage
from email.utils import make_msgid
from werkzeug.utils import secure_filename
from .credauth import Cred as Cra
import os

hname = socket.gethostname()

def empty_dict_knx(addr: str = "empty") -> dict:
    """Empty dictionary for knx

    Args:
        addr (str): e.g. 0/0/1

    Returns:
        dict: empty dict for knx
    """
    empty_knx = {}
    empty_knx[addr] = { "value" : None, "knxint" : None, "timestamp" : None, "datetime" : None, "status" : None , "failure" : None}
    return empty_knx

def empty_dict(name: str) -> dict:
    """Empty dictionary for knx

    Args:
        name (str): name of empty dict

    Returns:
        dict: _description_
    """
    empty = {}
    empty[name] = { "name" : name }
    #logging.info(t)
    empty[name]["status"] = 500
    empty[name]["failure"] = None
    return empty



def empty_mail() -> dict:
    """Empty dictionary for sending email

    Args:
        name (str): name of empty dict

    Returns:
        dict: _description_
    """
    mail = {}
    mail['Subject'] = None
    mail["status"] = 500
    mail["failure"] = None
    mail["attachments"] = 0
    mail["files"] = None
    mail['Text'] = None
    mail['Sender'] = None
    mail['Receiver'] = None
    mail['Port'] = None
    mail['runtime'] = None
    return mail

def get_path() -> tuple:
    """Get Path and endpoint of your flask request

    Returns:
        tuple: endpoint and path
    """
    endpoint = request.endpoint
    path = request.path
    return endpoint, path

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

@dataclass
class Mailer(DefaultDict):
    """Send E-Mail

    Args:
        DefaultDict (_type_): _description_
    """    
    subject: str | None =  None
    status: int = 500
    failure: str = ""
    attachments: int = 0
    #files: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))
    files: str | None = None
    #req: ds.MultiDict | None = None
    text: str = ""
    sender: str = hname
    server: str = 'smtp.mishki.de'
    username: str = ""
    receivers: str = ""
    port: int = 465
    runtime: float = -1

    def __post_init__(self):
        start = time.time()
        #if self.req is None:
        #    self.failure = f"Cannot create Mailer, because req is {self.req}"
        #    return self
        self.get_credentials()
        self.check_files()
        self.check_subject()
        self.check_text()
        self.check_sender()
        self.check_receivers()
        self.check_server()
        self.check_port()
        self.send_mail()
        end = time.time()
        self.runtime = round(end - start, 2)

    def get_credentials(self) -> bool:
        """Check if Mail Credentials are available"""
        try:
            row = Cra(host=self.server, usage="mail")
            print(row)
            self.server, self.username, self.password, self.receivers = row["host"], row["user"], row["password"], row["receiver"]
            #self.server, self.port, self.username, self.password, self.receivers = row["server"], row["port"], row["username"], row["password"], row["receiver"]
            #self.server, self.__pwd = row['host'], row['password']
            return True
        except Exception as e:
            self.failure = f"get_Credentials failed with {e}"
            self.status = 500
            return False

    def check_files(self) -> None:
        """Check if attachments are present"""        
        #if 'files[]' in self.req.files:
        if isinstance(self.files, str):
            #self.files = self.req.files.getlist('files[]')
            self.attachments = 1
        else:
            self.attachments = 0

    def check_subject(self) -> None:
        """Check if Subject is present"""
        if isinstance(self.subject, str):
            self.status = 200
        else:
            self.failure = "No Subject found in request"
            self.status = 500

    def check_text(self) -> None:
        """Check if Text is present"""
        if isinstance(self.text, str):
            self.status = 200
        else:
            self.text = "No Text found in request"
            self.status = 500
    
    def check_sender(self) -> None:
        """Check if Sender is present"""
        if isinstance(self.sender, str):
            self.status = 200
        else:
            self.sender = "No Sender found in request"
            self.status = 500

    def check_server(self) -> None:
        """Check if Server is present"""
        if isinstance(self.server, str):
            self.status = 200
        else:
            self.server = "No Server found in request"
            self.status = 500

    def check_port(self) -> None:
        """Check if Port is present"""
        if isinstance(self.port, str|int):
            self.status = 200
        else:
            self.port = "No Port found in request"
            self.status = 500

    def check_receivers(self) -> None:
        """Check if Receivers are present"""
        if isinstance(self.receivers, str):
            self.receiverlist = self.receivers.split(",")
            self.status = 200
        else:
            self.receivers = "No Receivers found in request"
            self.status = 500

    def send_mail(self) -> json:
        """Send Mail to one or more Receivers"""
        if self.status == 200:
            try:
                #mail = empty_mail
                msg = EmailMessage()
                msg['Subject'] = self.subject
                msg['From'] = self.sender
                msg['To'] = self.receivers
                msg["Date"] = formatdate(localtime=True)
                text = self.text
                #This is a plain text body.""")
                msg.set_content(f"""{text}""")
                # now create a Content-ID for the image
                mishki_cid = make_msgid(domain='mishki.de')
                # image_cid looks like <long.random.number@xyz.com>
                # to use it as the img src, we don't need `<` or `>`
                # so we use [1:-1] to strip them off
                images = []
                cids = {}
                if self.attachments == 1:
                    for file in self.files.split(","):
                        if re.search("jpg|png", file.split(".")[-1]):
                            #filename = secure_filename(file)
                            filename = os.path.basename(file)
                            cid = mishki_cid=mishki_cid[1:-1]
                            image = f"""<p><img src="cid:{cid}"></p>"""
                            print(image)
                            cids[filename] = mishki_cid
                            images.append(image)
                            imagesj = '\n'.join(images)
                            html = f"""\
                            <html>
                                <body>
                                    <p>{text}
                                    </p>
                                    {imagesj}
                                </body>
                            </html>
                            """ 
                            print(html)
                            msg.add_alternative(html, subtype='html')
                    #for file in self.files.split(","):
                            print(f"file: {file}")
                        # now open the image and attach it to the email
                        #with open(file, 'rb') as f:
                        # know the Content-Type of the image
                        #filename = secure_filename(file)
                        #filename = os.path.basename(file)
                        #print("filename", filename)
                            with open(file, 'rb') as fp:
                                img = fp.read()
                                print("img", img)
                                #img = file.read()
                                print("dat")
                                maintype, subtype = mimetypes.guess_type(filename)[0].split('/')
                                print(maintype, subtype)
                                image_cid = cids[file]
                                print(image_cid)
                                # attach it
                                msg.get_payload()[1].add_related(img, 
                                                                    maintype=maintype, 
                                                                    subtype=subtype, 
                                                                    cid=image_cid)
                                #file.close()
                            print("12")
                            msg.attach(MIMEText(html, "html"))
                            print("33")
                            msg.add_alternative(html, subtype='html')
                        else:
                            print("else")
                            filename = os.path.basename(file)
                            msg.add_attachment(open(filename, "r", encoding="utf8").read(), filename=filename)
                            html = f"""\
                            <html>
                                <body>
                                    <p>{text}
                                    </p>
                                </body>
                            </html>
                            """
                    print("for")
                else:
                    html = f"""\
                    <html>
                        <body>
                            <p>{text}
                            </p>
                        </body>
                    </html>
                    """
                print("new")
                print("again")
                # Convert it as a string
                #email_string = email_message.as_string()
                send = smtplib.SMTP_SSL(self.server, self.port)
                send.login(self.username, self.password)
                send.send_message(msg)
                #s.sendmail(From, To, msg.as_string())
                send.quit()
                return json.dumps({'status': 200, 'message' : 'E-Mail was send successful'})
            except Exception as e:
                logging.error(f"Exception {e}")
                return json.dumps({'status': 500, 'message' : f'E-Mail Send Exception: {e}'})
            #if self.attachments == 1:
            #    mail["files"] = self.files
   # else:
    #    return json.dumps({'status' : self.status, 'failure' : self.failure})

def send_push_message(server="notify.mishki.de", topic="jochens_alerts", data="Default Value, needs to be set", title="Default Title, needs to be set", prio="info", tags="warning"):
    try:
        # prio: max/urgent, high, default, low, min
        # tags: warning, rotating_light, triangular_flag_on_post, skull
        row = Cra(host=server, usage="push")
        username, password = row["user"], row["password"]
        req = requests.post(f"https://{server}/{topic}",
        data = data,
        headers={
            "Title": title,
            "Priority": prio,
            "Tags": tags
        }, auth=HTTPBasicAuth(username, password))
        return req.status_code
    except Exception as e:
        logging.error(f"Exception {e}")
        return e

def get_func_name(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return func.__name__, wrapper

def get_push_message(server="notify.mishki.de", topic="jochens_alerts") -> request:
    """Get requests object for getting Push Messages from server for topic"""
    try:
        fname = get_push_message.__name__
        row = Cra(host=server, usage="push")
        username, password = row["user"], row["password"]
        resp = requests.get(f"https://{server}/{topic}/json", auth=HTTPBasicAuth(username, password), stream=True)
        return resp
    except Exception as e:
        logging.error(f"{fname}: Exception {e}")
        return 