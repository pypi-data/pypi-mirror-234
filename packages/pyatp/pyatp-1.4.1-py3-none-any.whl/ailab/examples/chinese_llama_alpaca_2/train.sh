current_dir=$(dirname "$0")
train_imp_path="$current_dir/train_imp.py"
gpu_cnt=$(nvidia-smi --list-gpus | wc -l)
torchrun --nnodes 1 --nproc_per_node $gpu_cnt $train_imp_path
status=$?
exit $status
