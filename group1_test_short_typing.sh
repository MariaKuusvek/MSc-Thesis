#!/bin/bash

python3 something.py &
PYTHON_PID=$!

sleep 5

sudo perf stat -a \
    -e power/energy-pkg/,power/energy-cores/,cycles,instructions,cache-references,cache-misses,cs,migrations,page-faults \
    sleep 120 >> filename.txt 2>&1 &
PERF_PID=$!

WINDOW_ID=&(xdotool search --name "Simple PyQt Text Input")
xdotool windowactivate WINDOW_ID
xdotool type "Hello"

wait $PERF_PID

kill $PYTHON_PID