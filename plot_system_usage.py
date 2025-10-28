import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("system_log.csv")

df['cpu_util(%)'] = 100 - df['cpu_idle(%)']

GPU_TOTAL_MEM_MIB = 16384
df['gpu_mem_used(%)'] = df['gpu_mem_used(MiB)'] / GPU_TOTAL_MEM_MIB * 100

plt.figure(figsize=(12, 6))
plt.plot(df['gpu_util(%)'], label='GPU Utilization (%)', linewidth=1.8)
plt.plot(df['cpu_util(%)'], label='CPU Utilization (%)', linewidth=1.8)
plt.plot(df['gpu_mem_used(%)'], label='GPU Memory Usage (%)', linestyle='--', linewidth=1.8)

plt.xlabel('Time (samples)')
plt.ylabel('Utilization (%)')
plt.title('System Resource Utilization During Autoware Sensing & Perception Test')

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()
