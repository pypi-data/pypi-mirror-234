from flask import Flask, request
import re
import time
import socket
import sys
import requests
import logging
import csv
from subprocess import call   as system_call  # Execute a shell command
import subprocess
from joestools import knx, common
from joestools import credauth as Cra
from joestools import mysqlhome as msh

logging.basicConfig(filename="/home/jochen/scripts/logs/controlhue.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
#credentials = "/etc/Credentials/credentials.csv"
#common.HUEADDRESSFILE
addressnames = common.getaddrnames()

VERSION = '1.1'
CREATED = '18.04.2021'
FILENAME = 'controlhue.py'

logging.info(f"Start {FILENAME} {VERSION} {CREATED}")

DEFFAVHUE = "Fdn2CNYLTfDfp6E"
DEFFAVHUEALL = "Hell"
defshuffle = 0

app = Flask(__name__)

@app.route("/hue/scene/")
def huescene():
    fav = request.args.get('fav')
    grp = request.args.get('group')
    if fav is None:
        fav = DEFFAVHUE
    if grp is None:
        grp = DEFFAVHUEALL
        logging.debug("DEBUG: hue() fav: %s grp: %s" % (fav, grp) )
    row = Cra.cred('hue')
    host, password = row['host'], row['password']
    req = requests.get('http://' + host + '/api/' + password + '/groups/')
    data = req.json()
    for entry in data.items():
        if re.search('^' + grp + '$', entry[1]['name']) is not None:
            group = entry[0]
            logging.info(group)
    req.close()
    req = requests.get('http://' + host + '/api/' + password + '/scenes/')
    data = req.json()
    for entry in data.items():
        #print(entry[0],entry[1]['name'])
        if re.search('^' + fav + '$', entry[1]['name']) is not None:
            if entry[1]['group'] == group:
                sceneid = entry[0]
                logging.info(sceneid)
                break
    req.close()
    payload = " { \"scene\":" + "\"" + sceneid + "\"" + " }"
    headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
            }
    req = requests.put('http://' + host + '/api/' + password + '/groups/%s/action' % group, data = payload, headers=headers)
    data = req.json()
    req.close()
    for entry in data[0].keys():
        if re.search('success', entry) is not None:
            logging.info("INFO: hue() wurde im %s auf Scene %s geschaltet" % (grp, fav) )
            return "Philips Hue im %s wurde auf Scene %s geschaltet" % (grp, fav)
        else:
            logging.error("ERROR: hue() konnte im %s nicht auf Scene %s geschaltet werden" % (grp, fav) )
            return "Philips Hue im %s konnte nicht auf Scene %s geschaltet werden" % (grp, fav)

@app.route("/hue/next/")
def huenext():
    fav = request.args.get('fav')
    grp = request.args.get('group')
    if fav is None or fav == "":
        fav = DEFFAVHUE
    if grp is None:
        grp = DEFFAVHUEALL
        logging.debug("DEBUG: hue/next fav: %s grp: %s" % (fav, grp) )
    row = Cra.cred('hue')
    host, password = row['host'], row['password']
    req = requests.get('http://' + host + '/api/' + password + '/groups/')
    data = req.json()
    for entry in data.items():
        if re.search('^' + grp + '$', entry[1]['name']) is not None:
            group = entry[0]
    req.close()
    req = requests.get('http://' + host + '/api/' + password + '/scenes/')
    data = req.json()
    req.close()
    scenes = []
    for key, value in data.items():
        groups = value.get('group')
        if groups is not None and group in groups:
            scenes.append(key)
            #if value['name'] == fav:
            # EIS 15 only supports 14 Charakters and Sonnenuntergang Savanne will be shorten to Sonnenuntergan
            if fav in value['name']:
                favstr = key
    idx = scenes.index(favstr)
    sidx = len(scenes)
    if idx == (sidx - 1):
        sceneid = scenes[0]
        for key, value in data.items():
            if key == sceneid:
                fav = value['name']
    else:
        idx = idx + 1
        sceneid = scenes[idx]
        for key, value in data.items():
            if key == sceneid:
                fav = value['name']
    payload = " { \"scene\":" + "\"" + sceneid + "\"" + " }"
    headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
            }
    req = requests.put('http://' + host + '/api/' + password + '/groups/%s/action' % group, data = payload, headers=headers)
    data = req.json()
    req.close()
    for entry in data[0].keys():
        if re.search('success', entry) is not None:
            logging.info("INFO: hue/next wurde im %s auf Scene %s geschaltet" % (grp, fav) )
            try:
                addresses = eibp.getknxaddrfromname(addressnames)
                insert = []
                for entry in addresses.items():
                    if grp in entry[1]['Name']:
                        knxint = entry[0]
                        name = entry[1]['Name']
                        state = 'true'
                        insert.append((name, knxint, fav, state))
                        logging.debug(name)
                        break
                for e in insert:
                    format_str = """INSERT INTO hue (name, ga1, scene, state)
                    VALUES ("{name}", "{ga1}", "{scene}", {state}) ON DUPLICATE KEY UPDATE ga1="{ga1}", scene="{scene}", state={state};"""
                    sql = format_str.format(name=e[0], ga1=e[1], scene=e[2], state=e[3])
                    logging.debug(sql)
                result = msh.update(sql)
                logging.debug(result)
            except Exception as e:
                logging.error("ERROR: hue/next mysql update fehlerhaft" % (e) )
            return "Philips Hue im %s wurde auf Scene %s geschaltet" % (grp, fav)
        else:
            logging.error("ERROR: hue/next konnte im %s nicht auf Scene %s geschaltet werden" % (grp, fav) )
            return "Philips Hue im %s konnte nicht auf Scene %s geschaltet werden" % (grp, fav)

@app.route("/hue/prev/")
def hueprev():
    fav = request.args.get('fav')
    grp = request.args.get('group')
    if fav is None or fav == "":
        fav = DEFFAVHUE
    if grp is None:
        grp = DEFFAVHUEALL
        logging.debug("DEBUG: hue/prev fav: %s grp: %s" % (fav, grp) )
    row = Cra.cred('hue')
    host, password = row['host'], row['password']
    req = requests.get('http://' + host + '/api/' + password + '/groups/')
    data = req.json()
    for entry in data.items():
        if re.search('^' + grp + '$', entry[1]['name']) is not None:
            group = entry[0]
    req.close()
    req = requests.get('http://' + host + '/api/' + password + '/scenes/')
    data = req.json()
    req.close()
    scenes = []
    for key, value in data.items():
        groups = value.get('group')
        if groups is not None and group in groups:
            scenes.append(key)
            #if value['name'] == fav:
            # EIS 15 only supports 14 Charakters and Sonnenuntergang Savanne will be shorten to Sonnenuntergan
            if fav in value['name']:
                favstr = key
    idx = scenes.index(favstr)
    sidx = len(scenes)
    if idx == 0:
        sidx = sidx - 1
        sceneid = scenes[sidx]
        for key, value in data.items():
            if key == sceneid:
                fav = value['name']
    else:
        idx = idx - 1
        sceneid = scenes[idx]
        for key, value in data.items():
            if key == sceneid:
                fav = value['name']
    payload = " { \"scene\":" + "\"" + sceneid + "\"" + " }"
    headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
            }
    req = requests.put('http://' + host + '/api/' + password + '/groups/%s/action' % group, data = payload, headers=headers)
    data = req.json()
    req.close()
    for entry in data[0].keys():
        if re.search('success', entry) is not None:
            logging.info("INFO: hue/prev wurde im %s auf Scene %s geschaltet" % (grp, fav) )
            try:
                addresses = eibp.getknxaddrfromname(addressnames)
                insert = []
                for entry in addresses.items():
                    if grp in entry[1]['Name']:
                        knxint = entry[0]
                        name = entry[1]['Name']
                        state = 'true'
                        insert.append((name, knxint, fav, state))
                        logging.debug(name)
                        break
                for e in insert:
                    format_str = """INSERT INTO hue (name, ga1, scene, state)
                    VALUES ("{name}", "{ga1}", "{scene}", {state}) ON DUPLICATE KEY UPDATE ga1="{ga1}", scene="{scene}", state={state};"""
                    sql = format_str.format(name=e[0], ga1=e[1], scene=e[2], state=e[3])
                    logging.debug(sql)
                result = msh.update(sql)
                logging.debug(result)
            except Exception as e:
                logging.error("ERROR: hue/prev mysql update fehlerhaft" % (e) )
            return "Philips Hue im %s wurde auf Scene %s geschaltet" % (grp, fav)
        else:
            logging.error("ERROR: hue/prev konnte im %s nicht auf Scene %s geschaltet werden" % (grp, fav) )
            return "Philips Hue im %s konnte nicht auf Scene %s geschaltet werden" % (grp, fav)



@app.route("/hue/")
def hue():
    #fav = request.args.get('fav')
    groups = request.args.get('groups')
    state = request.args.get('state')
    output = []
    if groups is None:
        groups = defgrouphue
        logging.debug("DEBUG: hue() fav: %s group: %s" % (fav, group) )
    row = Cra.cred('hue')
    host, password = row['host'], row['password']
    req = requests.get('http://' + host + '/api/' + password + '/groups/')
    data = req.json()
    for grp in groups.split(','):
        for entry in data.items():
            if re.search('^' + grp + '$', entry[1]['name']) is not None:
                group = entry[0]
        req.close()
        payload = " { \"on\":" + state + " }"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
            }
        req = requests.put('http://' + host + '/api/' + password + '/groups/%s/action' % group, data = payload, headers=headers)
        data2 = req.json()
        req.close()
        for entry in data2[0].keys():
            if re.search('success', entry) is not None:
                logging.info("INFO: hue() wurde im %s auf %s geschaltet" % (grp, state) )
                output.append("Philips Hue im %s wurde auf %s geschaltet" % (grp, state))
                try:
                    addresses = knx.getknxaddrfromname(addressnames)
                    insert = []
                    for entry in addresses.items():
                        if grp in entry[1]['Name']:
                            knxint = entry[0]
                            name = entry[1]['Name']
                            insert.append((name, knxint, state))
                            logging.debug(name)
                            break
                    for e in insert:
                        format_str = """INSERT INTO hue (name, ga1, state)
                        VALUES ("{name}", "{ga1}", {state}) ON DUPLICATE KEY UPDATE ga1="{ga1}", state={state};"""
                        sql = format_str.format(name=e[0], ga1=e[1], state=e[2])
                        logging.debug(sql)
                    result = msh.update(sql)
                    logging.debug(result)
                except Exception as e:
                    logging.error("ERROR: hue() mysql update fehlerhaft" % (e) )
                #return "Philips Hue im %s wurde auf Scene %s geschaltet" % (group, fav)
            else:
                logging.error("ERROR: hue() konnte im %s nicht auf %s geschaltet werden" % (grp, state) )
                #return "Philips Hue im %s konnte nicht auf Scene %s geschaltet werden" % (group, fav)
                output.append("Philips Hue im %s konnte nicht auf %s geschaltet werden" % (grp, state))
    time.sleep(0.75)
    logging.info(output)
    return '\n'.join(output)

@app.route("/huelights/")
def huelights():
    #fav = request.args.get('fav')
    lights = request.args.get('lights')
    state = request.args.get('state')
    output = []
    if lights is None:
        return ('Keine Lampen ausgewählt')
    row = Cra.cred('hue')
    host, password = row['host'], row['password']
    if state == 'get':
        for light in lights.split(','):
            req = requests.get('http://' + host + '/api/' + password + '/lights/' + light)
            data = req.json()
            for entry in data.items():
                if 'state' in entry is not None:
                    if str(entry[1]['on']) == 'True':
                        on = 'true'
                    elif str(entry[1]['on']) == 'False':
                        on = 'false'
                    if str(entry[1]['reachable']) == 'True':
                        reachable = 'true'
                    elif str(entry[1]['reachable']) == 'False':
                        reachable = 'false'
                    output.append(light + ': state: ' + on + ' reachable: ' + reachable )
        req.close()
    elif state == 'true' or state == 'false':
        for light in lights.split(','):
            payload = " { \"on\":" + state + " }"
            headers = {
                    'content-type': "application/json",
                    'cache-control': "no-cache"
                    }
            req = requests.put('http://' + host + '/api/' + password + '/lights/%s/action' % group, data = payload, headers=headers)
            data2 = req.json()
            req.close()
            for entry in data2[0].keys():
                if re.search('success', entry) is not None:
                    logging.info("INFO: huelights wurde im %s auf %s geschaltet" % (light, state) )
                    output.append("Philips Hue im %s wurde auf %s geschaltet" % (light, state))
                    #return "Philips Hue im %s wurde auf Scene %s geschaltet" % (group, fav)
                else:
                    logging.error("ERROR: huelights konnte im %s nicht auf %s geschaltet werden" % (light, state) )
                    #return "Philips Hue im %s konnte nicht auf Scene %s geschaltet werden" % (group, fav)
                    output.append("Philips Hue im %s konnte nicht auf %s geschaltet werden" %  (light, state))
                time.sleep(0.75)
    return '\n'.join(output)




if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
