# latex2im


## Usage

### Launch GPU Servers

```
CUDA_VISIBLE_DEVICES=0 stdbuf -oL python diffusion_server_flask.py 6666 > final_logs_gpu_servers/log.rushgpu01.0.6666.jan9 2>&1 &
CUDA_VISIBLE_DEVICES=1 stdbuf -oL python diffusion_server_flask.py 6667 > final_logs_gpu_servers/log.rushgpu01.1.6667.jan9 2>&1 &
CUDA_VISIBLE_DEVICES=2 stdbuf -oL python diffusion_server_flask.py 6668 > final_logs_gpu_servers/log.rushgpu01.2.6668.jan9 2>&1 &
CUDA_VISIBLE_DEVICES=3 stdbuf -oL python diffusion_server_flask.py 6669 > final_logs_gpu_servers/log.rushgpu01.3.6669.jan9 2>&1 &
```

### Launch Redis Server

```
stdbuf -oL ./redis-server > ../log.redis_server.jan9 2>&1 &  #(wd: /n/rush_lab/Lab/Users/yuntian/redis/redis-7.0.5/src)
```

### Launch Main Server

```
stdbuf -oL gunicorn --bind localhost:4001 --workers 21 --worker-class=gevent --worker-connections=1000 --timeout 1200 web_server_flaskin_counter:app > final_logs_backendserver/log.gunicorn.4001.counter2 2>&1 &
```
