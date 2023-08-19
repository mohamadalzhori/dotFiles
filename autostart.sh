#!/bin/sh


# Check if redshift is already running
if ! pgrep -x "redshift" > /dev/null; then
    # Launch redshift if not running
    redshift &
fi


feh --bg-scale ~/Pictures/Wallpapers/pop.jpg &
nm-applet &
#dunst &
#sxhkd &
blueman-applet &
mailspring &
copyq &
picom &
todoist &
