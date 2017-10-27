#!/bin/bash

echo "Removing *.pyc and *~ files"

count=0

for file in $(find .); do
    if [[ $file == *.pyc || $file == *~ ]]; then
        rm $file
        let "count++"
    fi
done

echo "removed $count files."

unset count
