import sys
import random
import requests

from flask import Flask, request, render_template, stream_with_context, Response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST' or request.method == 'GET':
        formula = request.form['formula']
        api_key = request.form['api_key']
        if api_key != 'MIIEpAIBAAKCAQEAxNJYsX2DT+EPHCDyrobRX6/mAh+i5qD/uP425SaphpXZEBGE':
            print ('API KEY mismatch!')
            return

        print('-------')
        print(repr(formula))
        hostnames = open('hosts').readlines()
        names = set([])
        for hostname_status in hostnames:
            hostname, status = hostname_status.strip().split()
            if status == 'avail':
                names.add(hostname)
        data = dict(formula=formula)
        hostname = random.choice(list(names))
        print (hostname)
        print('-------')
        sys.stdout.flush()
        def generate():
            with requests.post(url=hostname, data=data, timeout=1200, stream=True) as r:
                for line in r.iter_lines():
                    yield line.decode('ascii').strip() + '\n'
        return Response(stream_with_context(generate()), content_type="text/plain")

if __name__ == '__main__':
    app.run(debug=False, port=5001)
