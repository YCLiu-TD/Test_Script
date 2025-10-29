#!/bin/bash

echo "timestamp,gpu_util(%),gpu_mem_used(MiB),cpu_idle(%)" | tee system_log.csv
while true; do
  timestamp=$(date +%Y-%m-%d_%H:%M:%S)
  gpu_info=$(nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader,nounits | head -n 1)
  cpu_idle=$(mpstat 1 1 | awk '/Average/ {print $12}')
  echo "$timestamp,$gpu_info,$cpu_idle" | tee -a system_log.csv
done
