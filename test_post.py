# importing the requests library
import requests
import json
import numpy as np
import base64
# defining the api-endpoint
API_ENDPOINT = "http://127.0.0.1:3001"
API_ENDPOINT = "http://aichatbeyond.com"
#http://54.202.209.190
# your API key here
API_KEY = "MIIEpAIBAAKCAQEAxNJYsX2DT+EPHCDyrobRX6/mAh+i5qD/uP425SaphpXZEBGE"

# your source code here
formula = '''a + b'''

# data to be sent to api
data = {'api_key':API_KEY,
        'formula': formula,
        }

# sending post request and saving response as response object
with requests.post(url=API_ENDPOINT, data=data, timeout=600, stream=True) as r:
    import pdb; pdb.set_trace()
    for line in r.iter_lines():
        response = line.decode('ascii').strip()
        #response = line.decode('ascii').strip()
        r = base64.decodebytes(response.encode('ascii'))
        q = np.frombuffer(r, dtype=np.float32).reshape((64, 320, 3))
        #r = base64.decodebytes(response.encode('ascii'))
        #q = np.frombuffer(r, dtype=np.float32).reshape((64, 320))

# extracting response text
print (q)
