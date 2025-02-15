#!/bin/bash

# get input directory
input_dir=$1

# check if input directory is provided
if [ -z "$input_dir" ]; then
    echo "Usage: $0 <input_directory>"
    exit 1
fi

# check if input directory exists
if [ ! -d "$input_dir" ]; then
    echo "Directory $input_dir does not exist."
    exit 1
fi

# iterate over all image files in the directory
for img in "$input_dir"/*.{jpg,jpeg,png,gif}; do
    # check if file exists
    if [ -f "$img" ]; then
        # get image dimensions
        width=$(identify -format "%w" "$img")
        height=$(identify -format "%h" "$img")

        # rotate image if width is greater than height
        if [ "$width" -gt "$height" ]; then
            echo "Rotating $img"
            convert "$img" -rotate 90 "$img"
        fi
    fi
done

echo "All images have been oriented correctly."