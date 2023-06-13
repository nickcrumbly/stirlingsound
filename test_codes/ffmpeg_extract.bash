#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
      echo "Usage $0 <input_file>"
      exit 0
fi

ffmpeg -i $1 -filter_complex "channelsplit=channel_layout=5.1[FL][FR][FC][LFE][BL][BR]" -map "[FL]" front_left.wav -map "[FR]" front_right.wav -map "[FC]" front_center.wav -map "[LFE]" lfe.wav -map "[BL]" back_left.wav -map "[BR]" back_right.wav -y
