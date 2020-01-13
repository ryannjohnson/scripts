#!/bin/bash

FILES_DIRECTORY="$1"
DESTINATION_DIRECTORY="$2"

rm -f "$FILES_DIRECTORY/ffmpeg_files.txt"

for FILE in $FILES_DIRECTORY/*.MTS
do
    echo "file '$FILE'" >> "$FILES_DIRECTORY/ffmpeg_files.txt"
done

ffmpeg \
    -f concat \
    -safe 0 \
    -i "$FILES_DIRECTORY/ffmpeg_files.txt" \
    -c copy \
    "$DESTINATION_DIRECTORY/$(date +%Y-%m-%d_%H-%M-%S)_copy.MTS"
