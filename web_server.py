import numpy as np
from datetime import datetime
import random
import math
import zmq
import json
import time

from flask import Flask, request, render_template, stream_with_context, Response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/decode', methods=['GET', 'POST'])
def decode():
    print (request)
    if request.method == 'POST' or request.method == 'GET':
        formula = request.form['formula']

        print('-------')
        print(repr(formula))
        print('-------')
        if len(formula.strip()) > 0:
            ctx = zmq.Context()
            socket = ctx.socket(zmq.REQ)
            socket.setsockopt(zmq.SNDTIMEO, 30000)
            socket.setsockopt(zmq.RCVTIMEO, 300000) 
            hostnames = open('hosts').readlines()
            names = set([])
            for hostname_status in hostnames:
                hostname, status = hostname_status.strip().split()
                if status == 'avail':
                    names.add(hostname)
            hostname = random.choice(list(names))
            print (hostname)
            socket.connect(hostname)
            req = dict(formula=formula)
            message = json.dumps(req)
            print (message)
            socket.send_string(message, zmq.NOBLOCK)

            #  Get the reply.
            try:
                message = socket.recv_string()
                print("Received reply %s [ %s ]" % (req, message))

                req = json.loads(message)
                err = req['err']
                print (req)
                print (req.keys())
                if not err:
                    formula = req['formula']
                    print(repr(formula))
                    print('-------')
                else:
                    reconst = 'An error occurred. Make sure to use the same context and all cover text (including spaces)!'
                def generate():
                    i = 0
                    while i<5:
                        yield req['image'] + '\n'
                        time.sleep(10)
                        i += 1
            except Exception as e:
                pass
            return Response(stream_with_context(generate()), content_type="text/plain")

        #return generate(), {"Content-Type": "text/csv"}
if __name__ == '__main__':
    app.run(debug=False, port=5001)
