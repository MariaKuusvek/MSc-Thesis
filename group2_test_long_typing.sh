#!/bin/bash

echo "Starting Long Typing Group 2 Test"
python3 something.py &
PYTHON_PID=&!

sleep 5

sudo perf stat -a -e power/energy-pkg/ ,power/energy-cores/ sleep 120 >>
something.txt 2>&1 &
PERF_PID=&!

xclip -selection clipboard < LoremIpsum.txt

WINDOW_ID=&(xdotool search --name "Simple PyQt Text Input")
xdotool windowactivate WINDOW_ID

for i in {1..12}; do
    xdotool key ctrl+v
    sleep 10
done

wait &PERF_PID

kill &PYTHON_PID