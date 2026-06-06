#!/usr/bin/env bash

# Compile the standard C++ core console loop application 
# Using -O3 optimization flag for efficient execution
g++ -O3 library_system.cpp -o library_system

# Grant execution permissions to the generated C++ binary file
chmod +x library_system