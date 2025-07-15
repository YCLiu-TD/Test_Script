#!/bin/bash
source install/setup.bash
ros2 topic pub -1 /planning/mission_planning/goal geometry_msgs/PoseStamped \
'{
  header: {
    stamp: {sec: 0, nanosec: 0},
    frame_id: "map"
  },
  pose: {
    position: {
      x: 3812.44384765625,
      y: 73770.7421875,
      z: 0.0
    },
    orientation: {
      x: 0.0,
      y: 0.0,
      z: 0.25960476343152117,
      w: 0.9657149511132485
    }
  }
}'
