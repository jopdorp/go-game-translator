#!/bin/bash

# get input directory
input=$1

root_dir=$(pwd)


convert_sgf_to_png() {
    cd "$@"
    # create $@.csv
    
    rm -rf anki_collection
    mkdir anki_collection
    touch anki_collection/"$@".csv
    
    for file in *; do
        echo "checking $file"
        # skip pngs
        if [[  $file == "anki_collection" ]]; then
            continue
        fi

        if [ -d "$file" ]; then
            echo "recurse $file"
            convert_sgf_to_png "$file"
        elif [[ "$file" == *.sgf ]]; then

            name=$(basename "$file"  .sgf)
            ${root_dir}/sgftopng  "anki_collection/$name.png" 1-0 < "$name.sgf"
            ${root_dir}/sgftopng "anki_collection/$name.solution.png" < "$name.sgf"

            # write new line in "$@".csv first column "anki_collection/${name}.png", second column "anki_collection/${name}.solution.png"
            echo "<img src='${name}.png'>, <img src='${name}.solution.png'>" >> anki_collection/"$@".csv
        else
            echo "unknown file type $file"
        fi
    done
    cd ..
}

convert_sgf_to_png $input
