from redis import Redis
from time import sleep

cli = Redis('localhost')
shared_var = 0

while True:
   cli.set('global_counter', shared_var)
   sleep(1)
