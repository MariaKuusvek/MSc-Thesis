#!/bin/bash

python3 base_skeleton_application.py &
PYTHON_PID=$!

sleep 5

sudo perf stat -a \
    -e power/energy-pkg/,power/energy-cores/,cycles,instructions,cache-references,cache-misses,cs,migrations,page-faults \
    sleep 120 >> control_test_medium.txt 2>&1 &
PERF_PID=$!

xclip -selection clipboard < LoremIpsum_5KB.txt

WINDOW_ID=&(xdotool search --name "Simple PyQt Text Input")
xdotool windowactivate WINDOW_ID
xdotool key ctrl+v

wait $PERF_PID

kill $PYTHON_PID