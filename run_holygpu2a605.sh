CUDA_VISIBLE_DEVICES=0 stdbuf -oL python diffusion_server_flask.py 6686 > final_logs_gpu_servers/log.holygpu2a605.0.6686.dec23.22 2>&1 &
CUDA_VISIBLE_DEVICES=1 stdbuf -oL python diffusion_server_flask.py 6687 > final_logs_gpu_servers/log.holygpu2a605.1.6687.dec23.22 2>&1 &
CUDA_VISIBLE_DEVICES=2 stdbuf -oL python diffusion_server_flask.py 6688 > final_logs_gpu_servers/log.holygpu2a605.2.6688.dec23.22 2>&1 &
CUDA_VISIBLE_DEVICES=3 stdbuf -oL python diffusion_server_flask.py 6689 > final_logs_gpu_servers/log.holygpu2a605.3.6689.dec23.22 2>&1 &
