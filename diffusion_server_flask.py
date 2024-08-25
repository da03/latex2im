import base64
import time
import sys
import os
import socket as sock
import torch

import numpy as np
import diffusers

from diffusers import DDPMPipeline
from transformers import AutoTokenizer, AutoModel
from utils import normalize_formula
from flask import Flask, request, render_template, stream_with_context, Response

app = Flask(__name__)

# setup
def setup(device='cuda'):
    device = ("cuda" if torch.cuda.is_available() else "cpu")
    img_pipe = DDPMPipeline.from_pretrained("yuntian-deng/latex2im_ss_finetunegptneo")
    img_pipe.to(device)
    
    model_type = "EleutherAI/gpt-neo-125M"
    #encoder = AutoModel.from_pretrained(model_type).to(device)
    encoder = img_pipe.unet.text_encoder
    if True:
        l = len(img_pipe.unet.down_blocks)
        for i in range(l):
            img_pipe.unet.down_blocks[i] = torch.compile(img_pipe.unet.down_blocks[i])
        l = len(img_pipe.unet.up_blocks)
        for i in range(l):
            img_pipe.unet.up_blocks[i] = torch.compile(img_pipe.unet.up_blocks[i])
    tokenizer = AutoTokenizer.from_pretrained(model_type, max_length=1024)
    eos_id = tokenizer.encode(tokenizer.eos_token)[0]
    
    def forward_encoder(latex):
        encoded = tokenizer(latex, return_tensors='pt', truncation=True, max_length=1024)
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
    print (f'Original input: {latex}')
    try:
        latex_norm = normalize_formula(latex)
        print (f'Normalized input: {latex_norm}')
    except Exception as e:
        latex_norm = latex
        print (f'Exception found, using original input: {latex_norm}')
    sys.stdout.flush()
    latex = latex_norm
    encoder_hidden_states = forward_encoder(latex)
    i = 0
    results = []
    for _, image_clean in img_pipe.run_clean(batch_size=1, generator=torch.manual_seed(0), encoder_hidden_states=encoder_hidden_states, output_type="numpy"):
        i += 1
        image_clean = image_clean[0]
        image_clean = np.ascontiguousarray(image_clean)
        s = base64.b64encode(image_clean).decode('ascii')
        yield s


hostname = sock.gethostname().split('.')[0]

port = int(sys.argv[1])

print (f'listening {port}')

while os.path.exists('hosts.lock'):
    time.sleep(1)
time.sleep(1)
while os.path.exists('hosts.lock'):
    time.sleep(1)
with open('hosts.lock', 'w') as fout:
    with open('hosts', 'a') as fout2:
        fout2.write('http://%s:%d avail\n'%(hostname, port))
if os.path.exists('hosts.lock'):
    os.remove('hosts.lock')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST' or request.method == 'GET':
        formula = request.form['formula']
        print(repr(formula))
        print('-------')
        def generate():
            for image in infer(formula):
                #print ('generating')
                yield image + '\n'
        return Response(stream_with_context(generate()), content_type="text/plain")


if __name__ == '__main__':
    app.run(debug=False, port=sys.argv[1], host='0.0.0.0')
