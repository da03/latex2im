import numpy as np
import base64
import math
import traceback
import json
import uuid
import time
import zmq
import sys
import os
import signal
from contextlib import contextmanager
import socket as sock
import torch

from PIL import Image
import numpy as np
from io import BytesIO
import os

from diffusers import DDPMPipeline
from transformers import AutoTokenizer, AutoModel

import diffusers
print (diffusers.__file__)

# setup
def setup(device='cuda'):
    img_pipe = DDPMPipeline.from_pretrained("yuntian-deng/latex2im_ss_100")
    img_pipe.to(device)
    
    model_type = "EleutherAI/gpt-neo-125M"
    encoder = AutoModel.from_pretrained(model_type).to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_type, max_length=512)
    eos_id = tokenizer.encode(tokenizer.eos_token)[0]
    
    def forward_encoder(latex):
        encoded = tokenizer(latex, return_tensors='pt', truncation=True, max_length=512)
        input_ids = encoded['input_ids']
        input_ids = torch.cat((input_ids, torch.LongTensor([eos_id,]).unsqueeze(0)), dim=-1)
        input_ids = input_ids.to(device)
        attention_mask = encoded['attention_mask']
        attention_mask = torch.cat((attention_mask, torch.LongTensor([1,]).unsqueeze(0)), dim=-1)
        attention_mask = attention_mask.to(device)
        with torch.no_grad():
            outputs = encoder(input_ids=input_ids, attention_mask=attention_mask)
            last_hidden_state = outputs.last_hidden_state 
            last_hidden_state = attention_mask.unsqueeze(-1) * last_hidden_state # shouldn't be necessary
        return last_hidden_state
    return img_pipe, forward_encoder

img_pipe, forward_encoder = setup()

# infer
def infer(latex): 
    encoder_hidden_states = forward_encoder(latex)
    i = 0
    results = []
    for image, image_clean in img_pipe.run_clean(batch_size=1, generator=torch.manual_seed(0), encoder_hidden_states=encoder_hidden_states, output_type="numpy"):
        i += 1
        image_clean = image_clean[0]
        image_clean = np.ascontiguousarray(image_clean)
        s = base64.b64encode(image_clean).decode('ascii')
        yield s
        #yield i, [image[0], image_clean[0]]
        #results.append(image_clean[0])
    #return results


hostname = sock.gethostname().split('.')[0]

port = int(sys.argv[1])

print (f'listening {port}')
ctx = zmq.Context()
socket = ctx.socket(zmq.REP)
socket.setsockopt(zmq.SNDTIMEO, 600000)
socket.bind("tcp://*:%d"%port)

while os.path.exists('hosts.lock'):
    time.sleep(1)
time.sleep(1)
while os.path.exists('hosts.lock'):
    time.sleep(1)
with open('hosts.lock', 'w') as fout:
    with open('hosts', 'a') as fout2:
        fout2.write('tcp://%s:%d avail\n'%(hostname, port))
if os.path.exists('hosts.lock'):
    os.remove('hosts.lock')


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise Exception("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
def numpy_to_pil(images):
    #import pdb; pdb.set_trace()
    images = (images * 255).round().astype("uint8")
    if images.shape[-1] == 1:
        images = np.squeeze(images, -1)
    pil_images = Image.fromarray(images)

    return pil_images

while True:
    try:
        #  Wait for next request from client
        message = socket.recv_string()

        with time_limit(600):
            print("Received request: %s" % message)
            request = json.loads(message)
            formula = request['formula']
            for image in infer(formula):
                pass
            #results = infer(formula)
            #images = [np.ascontiguousarray(image) for image in results]
            #last_image = images[-1]
            #print (last_image.dtype)
            #pil_image = numpy_to_pil(last_image)
            #pil_image.save(filename)

            #f = open(filename,'rb')
            #bytes = bytearray(f.read())
            #s = base64.b64encode(last_image).decode('ascii')

            result = dict(err=False, formula=formula, image=image)
            #print (last_image.shape)
            message = json.dumps(result)
            print ('sending')
            #print ('sending %s'%message)
            #  Send reply back to client
            socket.send_string(message, zmq.NOBLOCK)
    except Exception as e:
        traceback.print_exc()
        try:
            socket.close()
        except Exception as e:
            traceback.print_exc()
            pass
        time.sleep(2)
        try:
            socket = ctx.socket(zmq.REP)
            socket.setsockopt(zmq.SNDTIMEO, 60000)
            #socket.setsockopt(zmq.RCVTIMEO, 60000) 
            socket.bind("tcp://*:%d"%port)
        except Exception as e:
            traceback.print_exc()
            while os.path.exists('hosts.lock'):
                time.sleep(1)
            time.sleep(1)
            while os.path.exists('hosts.lock'):
                time.sleep(1)
            with open('hosts.lock', 'w') as fout2:
                with open('hosts') as fin:
                    with open('hosts.tmp', 'w') as fout:
                        for line in fin:
                            items = line.strip().split()
                            if items[0] == 'tcp://%s:%d'%(hostname, port):
                                fout.write('tcp://%s:%d unavail\n'%(hostname, port))
                            else:
                                fout.write('tcp://%s:%d %s\n'%(hostname, port, items[1]))
            os.rename('hosts.tmp', 'hosts')
            if os.path.exists('hosts.lock'):
                os.remove('hosts.lock')
            break
    time.sleep(1)
