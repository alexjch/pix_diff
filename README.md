# Identifying video frames with content changes

Basic detection of changes in between video frames using Pillow library. The motivation is to use an intel edison to record and save images to a cloud service storage and avoid serving these images from a device in my network (And opening my network to potential attacks) 

## Hardware setup
* Intel edison
* Camera
* ffmpeg
* AWS

## Usage


## Frame generation
ffmpeg -i ~/videostream/night.mp4 -r 1/1 ~/imagestream/$filename%03d.bmp

## Change detection


## Save frames that contain actions


## Video to frames


## TODO:
* Video capture and frame generation (script?)
* Include edison setup
** Camera
** Video capture bits as systemd service

##Some Sources
https://pillow.readthedocs.io/en/3.4.x/index.html
http://docs.opencv.org/3.0-beta/index.html
http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/


