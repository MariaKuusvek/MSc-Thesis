#!/bin/bash

echo "Starting Short Typing Control Test"
python3 base_skeleton_application.py &
PYTHON_PID=&!

sleep 5

sudo perf stat -a -e power/energy-pkg/ ,power/energy-cores/ sleep 120 >>
short_typing_control_test.txt 2>&1 &
PERF_PID=&!

WINDOW_ID=&(xdotool search --name "Simple PyQt Text Input")
xdotool windowactivate WINDOW_ID
xdotool type "Hello"

wait &PERF_PID

kill &PYTHON_PID