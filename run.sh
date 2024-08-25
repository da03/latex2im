 stdbuf -oL gunicorn --bind localhost:4001 --workers 21 --timeout 1200 web_server_flaskin_counter:app > final_logs_backendserver/log.gunicorn.4001.counter 2>&1 &
 stdbuf -oL gunicorn --bind localhost:4001 --workers 21 --timeout 1200 web_server_flaskin:app > final_logs_backendserver/log.gunicorn.4001.nocounter 2>&1 &
 stdbuf -oL gunicorn --bind localhost:4001 --workers 100 --timeout 1200 web_server_flaskin_counter:app > final_logs_backendserver/log.gunicorn.4001.counter 2>&1 &
 stdbuf -oL gunicorn --bind localhost:4001 --workers 21 --worker-class=gevent --worker-connections=1000  --timeout 1200 web_server_flaskin_counter:app > final_logs_backendserver/log.gunicorn.4001.counter 2>&1 &


 CUDA_VISIBLE_DEVICES=0 stdbuf -oL python diffusion_server_flask.py 6616 > final_logs_gpu_servers/log.seasdgx101.0.6616 2>&1 &
 CUDA_VISIBLE_DEVICES=1 stdbuf -oL python diffusion_server_flask.py 6617 > final_logs_gpu_servers/log.seasdgx101.1.6617 2>&1 &
 CUDA_VISIBLE_DEVICES=2 stdbuf -oL python diffusion_server_flask.py 6618 > final_logs_gpu_servers/log.seasdgx101.2.6618 2>&1 &

 [3]   Running                 CUDA_VISIBLE_DEVICES=0 stdbuf -oL python diffusion_server_flask.py 6616 > final_logs_gpu_servers/log.seasdgx101.0.6616 2>&1 &
 [4]   Running                 CUDA_VISIBLE_DEVICES=1 stdbuf -oL python diffusion_server_flask.py 6617 > final_logs_gpu_servers/log.seasdgx101.1.6617 2>&1 &
 [5]-  Running                 CUDA_VISIBLE_DEVICES=2 stdbuf -oL python diffusion_server_flask.py 6618 > final_logs_gpu_servers/log.seasdgx101.2.6618 2>&1 &


 CUDA_VISIBLE_DEVICES=0 stdbuf -oL python diffusion_server_flask.py 6636 > final_logs_gpu_servers/log.seasdgx103.0.6636 2>&1 &
 CUDA_VISIBLE_DEVICES=1 stdbuf -oL python diffusion_server_flask.py 6637 > final_logs_gpu_servers/log.seasdgx103.1.6637 2>&1 &
 CUDA_VISIBLE_DEVICES=2 stdbuf -oL python diffusion_server_flask.py 6638 > final_logs_gpu_servers/log.seasdgx103.2.6638 2>&1 &


 CUDA_VISIBLE_DEVICES=0 stdbuf -oL python diffusion_server_flask.py 6626 > final_logs_gpu_servers/log.seasdgx102.0.6626 2>&1 &
 CUDA_VISIBLE_DEVICES=1 stdbuf -oL python diffusion_server_flask.py 6627 > final_logs_gpu_servers/log.seasdgx102.1.6627 2>&1 &
 CUDA_VISIBLE_DEVICES=2 stdbuf -oL python diffusion_server_flask.py 6628 > final_logs_gpu_servers/log.seasdgx102.2.6628 2>&1 &
