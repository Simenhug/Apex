import base64
from datetime import datetime
import jws
from tzlocal import get_localzone
import json
import requests
import yaml


def getJWS():

	with open("secrets.yml",'r') as stream:
		try:
			yml = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)

	username = yml['username']

	entity = yml['entity']

	sharedSecret = yml['secret']

	header = {'alg': 'HS512'}

	body = {'username':username,'entity':entity,'datetime':datetime.now(get_localzone()).isoformat('T')}

	signature = jws.sign(header,body,sharedSecret)

	encoded_header = to_base64(json.dumps(header))
	encoded_body = to_base64(json.dumps(body))

	JWS = '%s.%s.%s' % (encoded_header, encoded_body, signature)

	return JWS

def to_base64(s):

	return base64.urlsafe_b64encode(s).replace('=', '')

def getJWT():
	jws = getJWS()
	requestJWT = requests.get('https://uat-api.apexclearing.com/legit/api/v1/cc/token?jws=%s' % jws)
	jwt = requestJWT.content
	print ('jwt = '+jwt)
	with open('secrets.yml', 'r') as f:
		doc = yaml.load(f)
	doc['jwt'] = jwt
	with open('secrets.yml', 'w') as f:
		yaml.dump(doc, f)
	return jwt

if __name__ == '__main__':
	getJWT()