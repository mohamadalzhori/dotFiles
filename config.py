# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from libqtile import bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import TextBox, Volume, Sep
from libqtile import qtile
from qtile_extras.widget.decorations import BorderDecoration
from libqtile.widget import GenPollText, base, TextBox
import os
import subprocess
from libqtile import hook
import time
import imaplib
import re
from widgets.my_custom_widget import create_next_event_widget


# Create the TextBox widget using the function from event_widget.py
next_event = create_next_event_widget()

mod = "mod4"
terminal = guess_terminal()

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.Popen([home])


colors  = [
    ["#282a36", "#282a36"], # bg
    ["#f8f8f2", "#f8f8f2"], # fg
    ["#000000", "#000000"], # colori01
    ["#ff5555", "#ff5555"], # color02
    ["#50fa7b", "#50fa7b"], # color03
    ["#f1fa8c", "#f1fa8c"], # color04
    ["#bd93f9", "#bd93f9"], # color05
    ["#ff79c6", "#ff79c6"], # color06
    ["#9aedfe", "#9aedfe"]  # color15
    ]

def log_message(message):
    with open('/tmp/qtile_debug.log', 'a') as log_file:
        log_file.write(message + '\n')

keys = [
    # A list of available commands that can be bound to keys can be found
        #TextBox(text="|", padding=5),
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key(['mod1'], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "space", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    # rofi integration

Key(['mod1'],'space', lazy.spawn("/home/zhori/.local/bin/scripts/executor.sh")),
    #Key(['mod1'],'m', lazy.spawn("rofi-wifi-menu.sh")),

    # Function Keys

    #Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q sset Master 5%-")),
    #Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q sset Master 5%+")),
    #Key([], "XF86AudioMute", lazy.spawn("amixer -q sset Master toggle")),

    # Use pavucontrol commands for audio control
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Switch to Arabic (Alt+RightShift)
    Key(["mod1"], "Shift_R", lazy.spawn("setxkbmap ar")),

    # Switch to English (Alt+LeftShift)
    Key(["mod1"], "Shift_L", lazy.spawn("setxkbmap us")),


    # Increase brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),

    # Decrease brightness
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

    # Launch Flameshot with the Print key
    Key([], "Print", lazy.spawn("flameshot gui")),

]

groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


@hook.subscribe.client_new
def client_new(client):
    if client.name == 'Mailspring':
        client.togroup('5')
    if client.name == 'Rhythmbox':
        client.togroup('5')
    if client.name == 'Todoist':
        client.togroup('5')

layouts = [
        layout.Columns(border_focus = "#ff3d33", border_normal = "#000000", border_width=3, margin=5),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans bold",
    fontsize=12,
    padding=3,
    foreground = "#ff3d33",
)
extension_defaults = widget_defaults.copy()



screens = [
    Screen(
        top=bar.Bar(
            [
            
        widget.Prompt(
                 font = "Ubuntu Mono",
                 fontsize=14,
        ),
        widget.GroupBox(
                 fontsize = 11,
                 margin_y = 3,
                 margin_x = 4,
                 padding_y = 2,
                 padding_x = 3,
                 borderwidth = 3,
                 active = "FFFFFF",
                 inactive = "000000",
                 rounded = False,
                 highlight_color = colors[2],
                 highlight_method = "line",
                 this_current_screen_border = "#ff3d33",
                 this_screen_border = colors [4],
                 #other_current_screen_border = colors[7],
                 #other_screen_border = colors[4],
                 ),
        widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),
        widget.WindowName(
                 max_chars = 40
                 ),
       
        #widget.CPU(
        #         format = 'Cpu: {load_percent}%',
        #         mouse_callbacks={'Button1': lambda : qtile.cmd_spawn('gnome-system-monitor')},
        #         decorations=[
        #             BorderDecoration(
        #                 colour = colors[4],
        #                border_width = [0, 0, 2, 0],
        #             )
        #         ],
        #         ),
        #widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),
        #widget.Memory(
        #         mouse_callbacks={'Button1': lambda : qtile.cmd_spawn('gnome-system-monitor')},
        #       format = '{MemUsed: .0f}{mm}',
        #         fmt = 'Mem: {}',
        #         decorations=[
        #             BorderDecoration(
        #                 colour = colors[8],
        #                 border_width = [0, 0, 2, 0],
        #             )
        #         ],
        #         ),
        #widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),
        #widget.DF(
        #         update_interval = 60,
        #         mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('nautilus')},
        #         partition = '/',
        #         #format = '[{p}] {uf}{m} ({r:.0f}%)',
        #         format = '{uf}{m} free',
        #         fmt = 'Disk: {}',
        #         visible_on_warn = False,
        #         decorations=[
        #             BorderDecoration(
        #                 colour = colors[5],
        #                 border_width = [0, 0, 2, 0],
        #             )
        #         ],
        #         ),
   
   next_event,

    widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),

    TextBox(text="⏮", fontsize=20, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('playerctl previous --player rhythmbox')}),
    TextBox(text="⏸", fontsize=20, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('playerctl play-pause --player rhythmbox')}),
    TextBox(text="⏭", fontsize=20, mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('playerctl next --player rhythmbox')}),


        widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),
        widget.Volume(
                 fmt = 'Vol: {}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[7],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),
        widget.Battery(
        format="{char} {percent:2.0%}",
        low_foreground="ffffff",
        low_percentage=0.20,   
        ),


        widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),
        widget.KeyboardLayout(
                 fmt = '{}',
                 decorations=[
                     BorderDecoration(
                         colour = colors[8],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        widget.Sep(linewidth=2,padding=10,foreground="#FFFFFF"),
        widget.Clock(
                 format = "%a, %b %d - %I:%M %p",
                 decorations=[
                     BorderDecoration(
                         colour = colors[3],
                         border_width = [0, 0, 2, 0],
                     )
                 ],
                 ),
        #widget.Spacer(length = 8),
        widget.Systray(padding = 3),
        #widget.Spacer(length = 8),


            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
