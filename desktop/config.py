# ██████   █████  ██    ██ ██ ██████  ██████  ███████ ██    ██ ███████ 
# ██   ██ ██   ██ ██    ██ ██ ██   ██ ██   ██ ██      ██    ██ ██      
# ██   ██ ███████ ██    ██ ██ ██   ██ ██   ██ █████   ██    ██ ███████ 
# ██   ██ ██   ██  ██  ██  ██ ██   ██ ██   ██ ██       ██  ██       ██ 
# ██████  ██   ██   ████   ██ ██████  ██████  ███████   ████   ███████ 

# VERY USEFUL EXAMPLE FOR AUTOSTART UP
# from libqtile.ipc import find_sockfile, Client
# from libqtile.command.client import InteractiveCommandClient
# from libqtile.command.interface import IPCCommandInterface
# 
# c = InteractiveCommandClient(IPCCommandInterface(Client(find_sockfile())))
# 
# c.to_screen(0)
# c.spawn("firefox")


import os
import subprocess

import libqtile.lazy
from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.lazy import lazy
from libqtile import layout, bar, widget
from libqtile import hook
from typing import List  # noqa: F401

mod = "mod4"
left_screen = 1
middle_screen = 0
right_screen = 2

###############################################################################
################################Keyboard Shortcuts#############################
###############################################################################
keys = [
    # Move windows up and down in the current stack
    Key([mod, "shift"], "l", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),

    # Custom key bindings for software
    Key([mod], "s", lazy.spawn("spotify")),
    Key([mod], "w", lazy.spawn("firefox")),
    Key([mod], "e", lazy.spawn("pcmanfm")),
    Key([mod], "f", lazy.spawn("freecad")),
    Key([mod], "Return", lazy.spawn("terminator")),
    
    # Lock the computer screen
    Key([mod], "l", lazy.spawn("dm-tool lock")),

    # Media key bindings
    Key([], "XF86AudioNext", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")),
    Key([], "XF86AudioPrev", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous")),
    Key([], "XF86AudioPlay", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),

    # Toggle Floating and Fullscreen
    Key([mod, "shift"], 't', lazy.window.toggle_floating()),
    Key([mod, "shift"], 'f', lazy.window.toggle_fullscreen()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Swap screens quickly
    Key([mod], "i", lazy.to_screen(left_screen)),
    Key([mod], "o", lazy.to_screen(middle_screen)),
    Key([mod], "p", lazy.to_screen(right_screen)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "q", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod], "r", lazy.spawn("dmenu_run -c -l 20")),
]


group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
group_labels = ["WWW", "DEV", "SYS", "DOC", "VIRT", "CHAT", "MUS", "VID", "GFX", "OBS",]
group_layouts = ["monadtall", "monadtall", "verticaltile", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
# group_spawns = [["firefox"], [""], [["terminator -e bpytop", "terminator -e bluetoothctl", "terminator -e nvtop"]], [""], [""], [""], [""], [""], [""], [""]]
groups = []

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
 #           spawn=group_spawns[i][0],
        ))

for i in groups:
    keys.extend([
    Key([mod], i.name, lazy.group[i.name].toscreen()), 
    Key([mod, "control"], i.name, lazy.window.togroup(i.name)), 
    Key([mod, "shift"], i.name, lazy.window.togroup(i.name)), 
    ])

# Colors for the system
# Sexy Sexy Gruvbox
def init_colors():
    return [["#1d2021"], # 0 
            ["#282828"], # 1
            ["#d65d0e"], # 2
            ["#fe8019"], # 3
            ["#cc241d"], # 4
            ["#fb4934"], # 5
            ["#98971a"], # 6
            ["#b8bb26"], # 7
            ["#d79921"], # 8
            ["#fabd2f"], # 9
            ["#458588"], # 10
            ["#83a598"], # 11
            ["#b16286"], # 12
            ["#d3869b"], # 13
            ["#689d6a"], # 14
            ["#8ec07c"], # 15
            ["#928374"], # 16
            ["#a89984"], # 17
            ["#ebdbb2"], # 18
            ["#32302f"], # 19
            ["#665c54"]] # 20


colors = init_colors()

# Defaults for each layout
def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#ebdbb2",
            "border_normal": "#928374",
            }

layout_theme = init_layout_theme()

# Layouts and basic customizations
layouts = [
    layout.Max(),
    layout.MonadTall(**layout_theme),
    layout.VerticalTile(**layout_theme),
]

def init_widgets_defaults():
    return dict(font="Ubuntu",
                fontsize = 12,
                padding = 4,
                background=colors[1])

widget_defaults = init_widgets_defaults()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(background=colors[17],
                                     foreground=colors[0]),

                widget.GroupBox(highlight_method = "line",
                                active=colors[18],
                                background=colors[19],
                                disable_drag=True,
                                highlight_color=colors[16],
                                inactive=colors[3],
                                other_current_screen_border=colors[16],
                                other_screen_border=colors[16],
                                this_current_screen_border=colors[16],
                                this_screen_border=colors[18],
                                use_mouse_wheel=False,
                                urgent_border=colors[4]),

                widget.Spacer(background=colors[19]),

                widget.TextBox(background=colors[20],
                               foreground=colors[17],
                               text="Volume: "),

                widget.Volume(background=colors[20],
                              foreground=colors[17],),

                widget.Net(background=colors[17],
                           foreground=colors[0],
                           format="{down} ↓↑ {up}",),

                widget.Clock(format='%a, %b %-d',
                             foreground=colors[0],
                             background=colors[3]),

                widget.Clock(format=' %-I:%M:%S %p',
                             foreground=colors[0],
                             background=colors[5]),
            ],
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(background=colors[17],
                                     foreground=colors[0]),

                widget.GroupBox(highlight_method = "line",
                                active=colors[18],
                                background=colors[19],
                                disable_drag=True,
                                highlight_color=colors[16],
                                inactive=colors[3],
                                other_current_screen_border=colors[16],
                                other_screen_border=colors[16],
                                this_current_screen_border=colors[16],
                                this_screen_border=colors[18],
                                use_mouse_wheel=False,
                                urgent_border=colors[4]),

                widget.Spacer(background=colors[19]),

                widget.TextBox(background=colors[20],
                               foreground=colors[17],
                               text="Mem: "),

                widget.MemoryGraph(background=colors[17],
                                   border_color=colors[0],
                                   graph_color=colors[0]),

                widget.TextBox(text="CPU: ",
                               foreground=colors[0],
                               background=colors[3]),

                widget.CPUGraph(background=colors[5],
                                border_color=colors[0],
                                graph_color=colors[0]),
            ],
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(background=colors[17],
                                     foreground=colors[0]),

                widget.GroupBox(highlight_method = "line",
                                active=colors[18],
                                background=colors[19],
                                disable_drag=True,
                                highlight_color=colors[16],
                                inactive=colors[3],
                                other_current_screen_border=colors[16],
                                other_screen_border=colors[16],
                                this_current_screen_border=colors[16],
                                this_screen_border=colors[18],
                                use_mouse_wheel=False,
                                urgent_border=colors[4]),

                widget.Spacer(background=colors[19]),
                
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

# Give the autostart file 770 permissions
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
