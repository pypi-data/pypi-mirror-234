current_dir=$(dirname "$0")
train_imp_path="$current_dir/train_imp.py"
gpu_cnt=$(nvidia-smi --list-gpus | wc -l)
distributed=false
for arg in "$@"; do
  case "$arg" in
      --distributed)
      distributed=true
      ;;
    *)
      # 其他参数处理
      ;;
  esac
done

if [ "$distributed" = true ];then
    echo "start distributed"
    torchrun --nnodes $NNODES --nproc_per_node $gpu_cnt --node_rank $RANK \
            --master_addr $MASTER_ADDR --master_port $MASTER_PORT $train_imp_path
else
    torchrun --nnodes 1 --nproc_per_node $gpu_cnt $train_imp_path
fi

status=$?
exit $status

