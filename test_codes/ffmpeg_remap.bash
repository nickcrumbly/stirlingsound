#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "Usage: $0 <input_file> <output_file>"
    exit 0
fi

ffmpeg -i $1 -filter_complex "channelmap=map=FL-FL|FC-FR|FR-FC|BL-LFE|BR-BL|LFE-BR:channel_layout=5.1" $2
