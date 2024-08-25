from redis import Redis
from time import sleep

cli = Redis('localhost')

while True:
    print(int(cli.get('global_counter')))
    sleep(1)
