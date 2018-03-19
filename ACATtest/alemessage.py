import base64
from datetime import datetime
import jws
from tzlocal import get_localzone
import json
import requests
import yaml

highWaterMark = ''
sinceDateTime = ''
limit = 1000
streamType = 'NONE'
timeoutSeconds= 60

def readACATMessage():

	with open("secrets.yml", 'r') as stream:
		try:
			yml = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)

	with open("ale.yml", 'r') as s:
		try:
			ale = yaml.load(s)
		except yaml.YAMLError as exc:
			print(exc)

   	accountNumber = yml['receive_account']

   	jwt = yml['jwt']

   	highWaterMark = ale['highWaterMark']

   	sinceDateTime = ale['dateTime'][:10]

   	# 'dateTime' format is something like 2015-01-03T01:14:31.697-06:00,
   	# we only need year-month-date, need to parse

   	partition = yml['clientReferenceId']

	headers = {'content-type': 'application/json', 'Authorization': jwt}

	params = {'highWaterMark': highWaterMark, 'streamType': streamType}

	response = requests.get('https://uat-api.apexclearing.com/ale/api/v1/read/alps-acat-status/%s' % partition, params=params, headers=headers)

	rJSON = json.loads(response.text)

	for acat in rJSON:
		try:
			highWaterMark = acat['id']
			dateTime = acat['dateTime']
			payload = json.loads(acat['payload'])
			tifId = payload['tifId']
			controlNumber = payload['acatsControlNumber']
			accountNumber = payload['account']
			currentState = payload['currentState']
			previousState = payload['previousState']
		except KeyError:
			print KeyError

	with open('ale.yml', 'r') as f:
		doc = yaml.load(f)
	doc['highWaterMark'] = highWaterMark
   	doc['dateTime'] = dateTime
   	doc['tifId'] = tifId
   	doc['controlNumber'] = controlNumber
   	doc['accountNumber'] = accountNumber
   	doc['currentState'] = currentState
   	doc['previousState'] = previousState
   	with open('ale.yml', 'w') as f:
   		yaml.dump(doc, f)

   	# try:
   	# 	details = rJSON['transfers'][0]
   	# except KeyError:
   	# 	print(KeyError)

	print rJSON


# listen to ale message while creating new ACAT
def streamACAT():

	with open("secrets.yml", 'r') as stream:
		try:
			yml = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)

	with open("ale.yml", 'r') as s:
		try:
			ale = yaml.load(s)
		except yaml.YAMLError as exc:
			print(exc)

   	accountNumber = yml['receive_account']

   	jwt = yml['jwt']

   	highWaterMark = ale['highWaterMark']

   	sinceDateTime = ale['dateTime'][:10]

   	# 'dateTime' format is something like 2015-01-03T01:14:31.697-06:00,
   	# we only need year-month-date, need to parse

   	partition = yml['clientReferenceId']

	headers = {'content-type': 'application/json', 'Authorization': jwt, 'connection': 'keep-alive'}

	params = {'highWaterMark': highWaterMark, 'streamType': 'LONG_POLL', 'timeoutSeconds': 3600}

	s = requests.Session()

	print('success so far')

	s.get('https://uat-api.apexclearing.com/ale/api/v1/read/alps-acat-status/%s' % partition, params=params, headers=headers, stream=True)

	print('ended')

	

