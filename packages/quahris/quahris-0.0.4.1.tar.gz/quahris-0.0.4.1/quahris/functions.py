import requests 
import urllib3
import xml.etree.ElementTree as ET
from itertools import islice
import pandas as pd

global cred

def qualys_cred(username, api_key):
    global cred
    cred = (username, api_key)

def listAssetGroup(ids, title, trunc, show_attributes, do_xml):
    #This function will help to list asset groups in Qualys with differing options
    global cred
    headers = {
        'X-Requested-With': 'Curl',
    }
    url = f"https://qualysguard.qg4.apps.qualys.com//api/2.0/fo/asset/host/?action=list&ids={ids}&title={title}&trunc={trunc}&show_attributes={show_attributes}"
    response = requests.get(url, headers=headers, auth=cred)
    return response.text

#show_asset. (we do either 0 or 1 in string)
def listUsers(search):
    global cred
    mySearch = []
    headers = {
        'X-Requested-With': 'Curl',
    }
    url = f'https://qualysguard.qg4.apps.qualys.com/msp/user_list.php'
    response = requests.get(url, headers=headers, auth = cred)
    with open('users.xml', 'w') as f:
        f.write(response.text)
    users_strings = ET.parse('users.xml').getroot()
    for i in users_strings.iter():
        if i.tag == search:
            mySearch.append(i.text)
    return mySearch




def friendprint():
    print("What's up man! Thanks for downloading my library\n\n--Chris Nam")

def personalTest():
    print("Im going to personally test things out. This is for 0.0.3.3")