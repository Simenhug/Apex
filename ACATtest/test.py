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

   account = yml['test_account']

   entity = yml['entity']

   sharedSecret = yml['secret']

   jwt = yml['jwt']

   clientReferenceId = yml['clientReferenceId']

   accountTitle = yml['accountTitle']

   body = {
      "account": account,
      "disableAutoSign": 'false',
      "clientReferenceId": clientReferenceId,
      "transferType": "FULL_TRANSFER",
      "contraParty": {
         "account": account,
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

   try:
      tifId = responseJSON['tifId']
   except KeyError:
      tifId = responseJSON['errors'][0]['attemptedValue']

   with open('secrets.yml', 'r') as f:
      doc = yaml.load(f)
   doc['tifId'] = tifId
   with open('secrets.yml', 'w') as f:
      yaml.dump(doc, f)

   print('tifid = ' + tifId)

   return tifId

#
#
# For pending transfers
def getControlNumber(accountNumber):

# fill this later

   response = requests.get('https://uat-api.apexclearing.com/alps/api/v1/account_acats_in_progress/%s' % accountNumber)

   details = response.content['transfers'][0]

   controlNumber = details["controlNumber"]

   currentStatus = details["currentStatus"]

   print('controlNumber = %s \n currentStatus = %s' % controlNumber,currentStatus)

   return controlNumber


def reviewACATSummary(controlNumber):

   response = requests.get('https://api.apexclearing.com/alps/api/v2/acats/%s' % controlNumber)

def reviewACATDetail(controlNumber):

   response = requests.get('https://api.apexclearing.com/alps/api/v2/acats/%s/details' % controlNumber)

tifid = createACAT()
#controlNumber = getControlNumber(account)













