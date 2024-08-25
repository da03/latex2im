# importing the requests library
import requests
import json
import numpy as np
import base64
# defining the api-endpoint
API_ENDPOINT = "http://127.0.0.1:5557"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"

# your source code here
formula = '''a + b'''

# data to be sent to api
data = {'api_dev_key':API_KEY,
        'formula': formula,
        }

# sending post request and saving response as response object
s = requests.Session()
with requests.post(url=API_ENDPOINT, data=data, timeout=600, stream=True) as r:
    import pdb; pdb.set_trace()
    for line in r.iter_lines():
        if line:
            print (line)
    #response = r.text
    #response = json.loads(response)
    #r = base64.decodebytes(response['image'].encode('ascii'))
    #q = np.frombuffer(r, dtype=np.float32).reshape((64, 320))

# extracting response text
print (q)
