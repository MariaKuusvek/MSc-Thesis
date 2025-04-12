#!/bin/bash

python3 folder/file &
PYTHON_PID=&!

sleep 5

sudo perf stat -a -e power/energy-pkg/ ,power/energy-cores/ sleep 120 >>
output_file_name.txt 2>&1 &
PERF_PID=&!

WINDOW_ID=&(xdotool search --name "Simple PyQt Text Input")
xdotool windowactivate WINDOW_ID
xdotool type "Hello"

wait &PERF_PID

kill &PYTHON_PID