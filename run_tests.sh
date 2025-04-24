#!/bin/bash

programs=(
  "novelWriter/novelWriter_skeleton_base.py"
  "novelWriter/novelWriter_skeleton_change.py"
  "novelWriter/novelWriter_skeleton_change+logging.py"
  "mu/mu_skeleton_base.py"
  "mu/mu_skeleton_change.py"
  "mu/mu_skeleton_change+logging.py"
  "leo/leo_skeleton_base.py"
  "leo/leo_skeleton_change.py"
  "leo/leo_skeleton_change+logging.py"
)

for program in "${programs[@]}"; do

    prog_basename=$(basename "$program" .py)

    scenarios=("empty" "medium" "long")

    for scenario in "${scenarios[@]}"; do
        result_file="test_${prog_basename}_${scenario}.txt"

        if [ "$scenario" == "medium" ]; then
            input_file="LoremIpsum_5KB.txt"
        elif [ "$scenario" == "long" ]; then
            input_file="LoremIpsum_50KB.txt"
        fi

        for ((i=1; i<=30; i++)); do
            python3 "$program" &
            PYTHON_PID=$!

            sleep 5

            sudo perf stat -a \
                -e power/energy-pkg/,power/energy-cores/,cycles,instructions,cache-references,cache-misses,cs,migrations,page-faults \
                sleep 120 >> "$result_file" 2>&1 &
            PERF_PID=$!

            if [ "$scenario" != "empty" ]; then
                xclip -selection clipboard < "$input_file"

                WINDOW_ID=&(xdotool search --name "Simple PyQt Text Input")
                xdotool windowactivate WINDOW_ID
                xdotool key ctrl+v
            fi

            wait $PERF_PID

            kill $PYTHON_PID

            sleep 300
        done
    done
done