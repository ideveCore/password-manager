import requests
import json
import warnings
warnings.filterwarnings("ignore")



def EmailValidate(email):
    url = f"https://api.eva.pingutil.com/email?email={email}"
    resp = requests.get(url,verify=False)
    respo = resp.content
    x = json.loads(respo)
    return x['data']

def isDisposable(email):
    url = f"https://api.eva.pingutil.com/email?email={email}"
    resp = requests.get(url,verify=False)
    respo = resp.content
    x = json.loads(respo)
    return x['data']['disposable']

def isDeliverable(email):
    url = f"https://api.eva.pingutil.com/email?email={email}"
    resp = requests.get(url,verify=False)
    respo = resp.content
    x = json.loads(respo)
    return x['data']['deliverable']

def isSpam(email):
    url = f"https://api.eva.pingutil.com/email?email={email}"
    resp = requests.get(url,verify=False)
    respo = resp.content
    x = json.loads(respo)
    return x['data']['spam']
