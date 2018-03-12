import base64
from datetime import datetime
import jws
from tzlocal import get_localzone
import json
import requests
import yaml

hightWaterMark = ''
sinceDateTime = ''
limit = 1000
streamType = 'NONE'
timeoutSeconds= 60
partition = '0158'

def readACATMessage():

	with open("secrets.yml", 'r') as stream:
		try:
			yml = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)

   	accountNumber = yml['receive_account']

   	jwt = yml['jwt']

	headers = {'content-type': 'application/json', 'Authorization': jwt}

	params = {'hightWaterMark': hightWaterMark, 'streamType': streamType}

	response = requests.get('https://api.apexclearing.com/ale/api/v1/read/alps-acat-status/%s' % partition, params=params, headers=headers)

	rJSON = json.loads(response.text)

	print(rJSON)

   	try:
   		details = rJSON['transfers'][0]
   	except KeyError:
   		print(KeyError)

	print rJSON

