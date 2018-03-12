import base64
from datetime import datetime
import jws
from tzlocal import get_localzone
import json
import requests
import yaml

def createACAT():

   with open("secrets.yml",'r') as stream:
      try:
         yml = yaml.load(stream)
      except yaml.YAMLError as exc:
         print(exc)

   username = yml['username']

   receiver = yml['receive_account']

   deliverer = yml['deliver_account']

   processingCaseId = yml['processingCaseId']

   entity = yml['entity']

   sharedSecret = yml['secret']

   jwt = yml['jwt']

   clientReferenceId = yml['clientReferenceId']

   accountTitle = yml['accountTitle']

   body = {
      "account": receiver,
      "disableAutoSign": 'false',
      "clientReferenceId": clientReferenceId,
      "transferType": "FULL_TRANSFER",
      "contraParty": {
         "account": deliverer,
         "accountTitle": accountTitle,
         "primarySsnOrTaxId": "",
         "secondarySsnOrTaxId": "",
         "accountType": "Single",
         "participant": {
            "participantNumber": "0385"
         }
      }
   }

   headers = {"Authorization": jwt, 'content-type': 'application/json'}

   Url = 'https://uat-api.apexclearing.com/alps/api/v1/tif'

   response = requests.post(Url,data=json.dumps(body),headers=headers)

   responseJSON = json.loads(response.text)

   print(responseJSON)

   try:
      tifId = responseJSON['tifId']
      newCaseId = responseJSON['processingCaseId']
   except KeyError:
      tifId = responseJSON['errors'][0]['attemptedValue']

   with open('secrets.yml', 'r') as f:
      doc = yaml.load(f)
   doc['tifId'] = tifId
   doc['processingCaseId'] = newCaseId
   with open('secrets.yml', 'w') as f:
      yaml.dump(doc, f)

   print('tifid = ' + tifId)
   print('processingCaseId = ' + newCaseId)

   return tifId

def signTif():

   with open("secrets.yml",'r') as stream:
      try:
         yml = yaml.load(stream)
      except yaml.YAMLError as exc:
         print(exc)

   jwt = yml['jwt']

   tifId = yml['tifId']

   headers = {"Authorization": jwt, 'content-type': 'application/json'}

   url = 'https://uat-api.apexclearing.com/alps/api/v1/tif/%s' % tifId

   response = requests.put(url, headers=headers)

   rJSON = json.loads(response.text)

   print(rJSON)
#
# For pending transfers
def getControlNumber():

   with open("secrets.yml",'r') as stream:
      try:
         yml = yaml.load(stream)
      except yaml.YAMLError as exc:
         print(exc)

   accountNumber = yml['receive_account']

   jwt = yml['jwt']

   headers = {"Authorization": jwt, 'content-type': 'application/json'}

   response = requests.get('https://uat-api.apexclearing.com/alps/api/v1/account_acats_in_progress/%s' % accountNumber,headers = headers)

   rJSON = json.loads(response.text)

   print(rJSON)

   try:
      details = rJSON['transfers'][0]
   except KeyError:
      print(KeyError)

   controlNumber = details["controlNumber"]

   currentStatus = details["currentStatus"]

   print('controlNumber = %s \n currentStatus = %s' % controlNumber,currentStatus)

   return controlNumber


def reviewACATSummary(controlNumber):

   response = requests.get('https://api.apexclearing.com/alps/api/v2/acats/%s' % controlNumber)

def reviewACATDetail(controlNumber):

   response = requests.get('https://api.apexclearing.com/alps/api/v2/acats/%s/details' % controlNumber)


#controlNumber = getControlNumber(account)













