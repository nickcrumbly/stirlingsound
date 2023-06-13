#!/usr/bin/env bash

# Install base packages from distro, this lets APT resolve packages
sudo apt install -y libsdl2-*-2.0-0 libsdl2-doc libsdl2-dev python3-gpiozero ffmpeg ogg123 oggenc

# Use pip in local mode to make sure pygame is fresh
python3 -m pip install -r requirements.txt --user
