#!/bin/bash

echo "Removing *.pyc and *~ files"

count=0

while IFS= read -r -d $'\0' file; do
    if [[ $file == *.pyc || $file == *~ ]]; then
        echo "removing $file"
        rm $file
        let "count++"
    fi
done < <(find . -print0)

echo "removed $count files."

unset count
