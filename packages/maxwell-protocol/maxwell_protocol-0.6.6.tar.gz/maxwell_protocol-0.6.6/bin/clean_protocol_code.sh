#!/bin/bash

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )";
cd ${current_dir}

rm -rf proto
rm -rf maxwell
