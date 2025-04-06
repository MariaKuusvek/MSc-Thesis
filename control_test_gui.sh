#!/bin/bash

echo "Starting GUI Control Test"
python3 base_skeleton_application.py &
PYTHON_PID=&!

sleep 5

sudo perf stat -a -e power/energy-pkg/ ,power/energy-cores/ sleep 120 >>
gui_control_test.txt 2>&1 &
PERF_PID=&!

wait &PERF_PID

kill &PYTHON_PID