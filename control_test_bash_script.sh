#!/bin/bash

sleep 5

sudo perf stat -a \
    -e power/energy-pkg/,power/energy-cores/,cycles,instructions,cache-references,cache-misses,cs,migrations,page-faults \
    sleep 120 >> bash_script_control_test.txt 2>&1 &
PERF_PID=$!

wait $PERF_PID