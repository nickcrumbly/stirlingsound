#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
      echo "Usage: $0 <input_file> <output_file>"
          exit 0
fi


ffmpeg -i $1 -c:a libvorbis -ar 22500 $2
