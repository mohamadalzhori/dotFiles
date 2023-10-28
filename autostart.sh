#!/bin/sh


# Check if redshift is already running
if ! pgrep -x "redshift" > /dev/null; then
    # Launch redshift if not running
    redshift &
fi


#feh --bg-scale ~/Pictures/Wallpapers/AlQantara.png &
feh --bg-center Pictures/Wallpapers/TheWallpaper.png&
nm-applet &
#dunst &
#sxhkd &
#/bin/bash /home/zhori/.local/bin/scripts/onedrive.sh &
#megasync &
blueman-applet &
mailspring &
copyq &
picom &
todoist &
mocp -m Music &
fusuma &
#notion-app-enhanced &

