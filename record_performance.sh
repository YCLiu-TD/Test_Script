#!/bin/bash
source ~/autoware/install/setup.bash

ros2 bag record \
    /sensing/lidar/concatenate_data_synchronizer/debug/processing_time_ms \
    /sensing/lidar/top/distortion_corrector/debug/processing_time_ms \
    /sensing/lidar/top/ring_outlier_filter/debug/processing_time_ms \
    /perception/object_recognition/detection/centerpoint/lidar_centerpoint/debug/processing_time_ms \
    /perception/object_recognition/tracking/multi_object_tracker/debug/processing_time_ms \
    /perception/object_recognition/prediction/map_based_prediction/debug/processing_time_ms \
    -o autoware_perf_test
