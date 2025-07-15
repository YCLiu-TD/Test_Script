#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from autoware_internal_debug_msgs.msg import Float64Stamped
import numpy as np
import csv
import os
import psutil

VS_TOPIC = '/planning/scenario_planning/velocity_smoother/debug/processing_time_ms'
LOCAL_TOPICS = {
    'mission_planner':    '/planning/mission_planning/mission_planner/debug/processing_time_ms',
    'scenario_selector':  '/planning/scenario_planning/scenario_selector/debug/processing_time_ms',
    'path_planner':       '/planning/scenario_planning/lane_driving/behavior_planning/behavior_path_planner/debug/total_time/processing_time_ms',
    'elastic_band':       '/planning/scenario_planning/lane_driving/motion_planning/elastic_band_smoother/debug/processing_time_ms',
    'velocity_planner':   '/planning/scenario_planning/lane_driving/motion_planning/motion_velocity_planner/debug/processing_time_ms',
    'obstacle_cruise':    '/planning/scenario_planning/lane_driving/motion_planning/obstacle_cruise_planner/debug/processing_time_ms',
    'path_optimizer':     '/planning/scenario_planning/lane_driving/motion_planning/path_optimizer/debug/processing_time_ms',
    'velocity_smoother':  VS_TOPIC,
}

class LatencyMonitor(Node):
    def __init__(self):
        super().__init__('latency_monitor')
        self.last_vs_time = None
        self.current_local = {name: None for name in LOCAL_TOPICS}
        self.cycle_idx = 0

        # Prepare CSV in append mode
        self.csv_path = os.path.join(os.getcwd(), 'latency_report.csv')
        first = not os.path.exists(self.csv_path)
        self.csv_file = open(self.csv_path, 'a', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        if first:
            header = ['cycle_idx', 'frame_interval_ms', 'total_components_ms'] \
                     + list(LOCAL_TOPICS.keys()) \
                     + ['cpu_usage_percent']
            self.csv_writer.writerow(header)

        # Subscribe to all modules
        for name, topic in LOCAL_TOPICS.items():
            cb = self.make_cb(name)
            self.create_subscription(Float64Stamped, topic, cb, 10)

        # Timer to flush CSV periodically
        self.create_timer(5.0, self.csv_file.flush)

    def make_cb(self, name):
        def cb(msg):
            ts = msg.stamp.sec + msg.stamp.nanosec * 1e-9
            # Update local value
            self.current_local[name] = msg.data
            if name == 'velocity_smoother':
                # On each velocity_smoother event, record a cycle
                if self.last_vs_time is not None:
                    interval = (ts - self.last_vs_time) * 1000.0
                else:
                    interval = 0.0
                self.last_vs_time = ts

                # Sum of components
                total_comp = sum(v or 0.0 for v in self.current_local.values())
                # CPU usage since last call
                cpu_pct = psutil.cpu_percent(interval=None)

                # Build CSV row
                row = [self.cycle_idx,
                       f'{interval:.3f}',
                       f'{total_comp:.3f}'] \
                    + [f'{self.current_local[n] or 0.0:.3f}' for n in LOCAL_TOPICS] \
                    + [f'{cpu_pct:.1f}']
                self.csv_writer.writerow(row)
                self.csv_file.flush()
                self.cycle_idx += 1
        return cb

    def destroy_node(self):
        # Close file
        try:
            self.csv_file.close()
        except:
            pass
        super().destroy_node()


def main():
    rclpy.init()
    node = LatencyMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        print(f'CSV saved to {node.csv_path}')

if __name__ == '__main__':
    main()
