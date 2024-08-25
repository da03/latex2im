import numpy as np
import math
import traceback
import json
import time
import zmq
import sys
import os
import signal
from contextlib import contextmanager
import socket as sock

from flask import Flask, request, render_template
app = Flask(__name__)

hostname = sock.gethostname().split('.')[0]

port = int(sys.argv[1])

print (f'listening {port}')
ctx = zmq.Context()
socket = ctx.socket(zmq.REP)
socket.setsockopt(zmq.SNDTIMEO, 60000)
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

while True:
    try:
        #  Wait for next request from client
        message = socket.recv_string()

        with time_limit(30):
            print("Received request: %s" % message)
            request = json.loads(message)
            formula = request['formula']

            result = dict(err=False, formula=formula+'abcabc')
            message = json.dumps(result)
            print ('sending %s'%message)
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
