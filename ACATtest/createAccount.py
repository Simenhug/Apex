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
timeoutSeconds: 60

def readACATMessage(partition):

	response = requests.get('https://api.apexclearing.com/ale/api/v1/read/alps-acat-status/' + /
		'%s?hightWaterMark=%s&sinceDateTime=%s' % partition, hightWaterMark, sinceDateTime)

	print response

