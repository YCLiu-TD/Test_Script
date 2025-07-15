#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('latency_report.csv')

plt.figure()
plt.plot(df['cycle_idx'], df['total_components_ms'])
plt.title('Planning Total Components Time per Cycle')
plt.xlabel('Cycle Index')
plt.ylabel('Total Components Time (ms)')
plt.tight_layout()
plt.savefig('planning_total_time.png')

plt.figure()
plt.plot(df['cycle_idx'], df['cpu_usage_percent'])
plt.title('CPU Usage per Cycle')
plt.xlabel('Cycle Index')
plt.ylabel('CPU Usage (%)')
plt.tight_layout()
plt.savefig('cpu_usage.png')

print("Saved plots as planning_total_time.png and cpu_usage.png")
