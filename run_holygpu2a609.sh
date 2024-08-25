CUDA_VISIBLE_DEVICES=0 stdbuf -oL python diffusion_server_flask.py 6696 > final_logs_gpu_servers/log.holygpu2a609.0.6696.dec23.22 2>&1 &
CUDA_VISIBLE_DEVICES=1 stdbuf -oL python diffusion_server_flask.py 6697 > final_logs_gpu_servers/log.holygpu2a609.1.6697.dec23.22 2>&1 &
CUDA_VISIBLE_DEVICES=2 stdbuf -oL python diffusion_server_flask.py 6698 > final_logs_gpu_servers/log.holygpu2a609.2.6698.dec23.22 2>&1 &
CUDA_VISIBLE_DEVICES=3 stdbuf -oL python diffusion_server_flask.py 6699 > final_logs_gpu_servers/log.holygpu2a609.3.6699.dec23.22 2>&1 &
