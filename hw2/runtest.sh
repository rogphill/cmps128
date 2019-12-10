#!/bin/bash
sudo docker kill $(docker ps -q)
sudo docker build -t assignment2 .
python2 HW2.py
