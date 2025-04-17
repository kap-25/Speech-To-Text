#!/usr/bin/env bash
# Install PortAudio dependencies
sudo apt-get update
sudo apt-get install -y portaudio19-dev
pip install -r requirements.txt