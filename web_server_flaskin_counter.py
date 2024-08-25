import sys
import random
import requests
import collections

from flask import Flask, request, render_template, stream_with_context, Response
from redis import Redis

app = Flask(__name__)

cli = Redis('localhost')

if not cli.exists("global_counter"):
    print ('setting Redis global counter to 0')
    cli.set('global_counter', 0)

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
        names = sorted(list(names))
        names_per_server = collections.defaultdict(list)
        for name in names:
            server_name = name.split(':')[1]
            names_per_server[server_name].append(name)
        server_names = sorted(list(names_per_server.keys()))
        names_out = []
        i_min = min([len(names_per_server[server_name]) for server_name in server_names])
        for i in range(0, i_min):
            for server_name in server_names:
                names_out.append(names_per_server[server_name][i])
        names = names_out
        print (names)
        global_counter = cli.incr('global_counter')
        idx = global_counter % len(names)
        #hostname = random.choice(list(names))
        hostname = names[idx]
        print (f'{hostname}, {idx}, {global_counter}')
        print('-------')
        sys.stdout.flush()
        def generate():
            with requests.post(url=hostname, data=data, timeout=1200, stream=True) as r:
                for line in r.iter_lines():
                    yield line.decode('ascii').strip() + '\n'
        return Response(stream_with_context(generate()), content_type="text/plain")

if __name__ == '__main__':
    app.run(debug=False, port=3001)
