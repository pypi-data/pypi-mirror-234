#!/bin/bash
# driver.sh - The simplest autograder we could think of. It checks
#   that students can write a C program that compiles, and then
#   executes with an exit status of zero.
#   Usage: ./driver.sh

# Compile the code
# echo "Compiling hello3.c"
# python3 -c "print('Hello world from python 2')"
# python3 --version
python3 driver_python.py

#(make clean; make)
#status=$?
#if [ ${status} -ne 0 ]; then
#    echo "Failure: Unable to compile hello3.c (return status = ${status})"
#    echo "{\"scores\": {\"Correctness\": 0}}"
#    exit
#fi
#
# Run the code
#echo "Running ./hello3"
#./hello3
#status=$?
#if [ ${status} -eq 0 ]; then
#    echo "Success: ./hello3 runs with an exit status of 0"
#    echo "{\"scores\": {\"Correctness\": 100}}"
#else
#    echo "Failure: ./hello fails or returns nonzero exit status of ${status}"
#    echo "{\"scores\": {\"Correctness\": 0}}"
#fi

exit

