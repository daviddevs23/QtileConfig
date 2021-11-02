#!/bin/sh

nitrogen --restore &
numlockx on & 
pulseaudio -k && pulseaudio --start &
bluetoothctl power on &
xrandr --output HDMI-0 --mode 1920x1080 --rate 60.00 --pos 0x0 --rotate left --dpi 90 --output DP-2 --primary --mode 1920x1080 --rate 60 --pos 1080x0 --rotate normal --dpi 161 --output DP-1 --mode 1920x1080 --rate 60.00 --pos 3000x0 --dpi 92 & 
picom &

