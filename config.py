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

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

mod = "mod4"

black  = "#282828"
red    = "#cc241d"
green  = "#98971a"
yellow = "#d79921"
blue   = "#458588"
purple = "#b16286"
aqua   = "#689d6a"
white  = "#ebdbb2"
gray   = "#928374"

keys = [
    # Switch between screens
    Key([mod], "1", lazy.to_screen(0)),
    Key([mod], "2", lazy.to_screen(1)),

    # Switch between windows in current stack pane
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),

    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    Key([mod], "Return", lazy.spawn("urxvt -fg lightgray -bg black -tr -tint lightgray -sh 40")),
    Key([mod], "b", lazy.spawn("chromium")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "space", lazy.next_layout()),

    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),

    Key([mod], "r", lazy.spawncmd()),

    # add volume control
    Key([mod, "shift"], "k", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod, "shift"], "j", lazy.spawn("amixer -c 0 -q set Master 2dB-")),

    # lock secreen
    Key([mod, "control"], "l", lazy.spawn("i3lock -i /home/arch/.i3/i3lock.png -c 000000")),

    Key([mod], "z", lazy.window.toggle_floating()),
    #Key([mod], "n", lazy.window.toggle_minimize()),
    #Key([mod], "m", lazy.window.toggle_maximize()),

    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "o", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "m", lazy.layout.maximize()),
]

myMonadTall = layout.MonadTall()

myStack = layout.Stack(
    border_focus=blue,
    border_normal=gray,
    border_width=2,
    margin=2,
    num_stacks=2,
)

myLayouts = {
    "a": [
        myMonadTall,
        layout.Max(),
    ],
    "s": [
        myMonadTall,
        layout.Max(),
    ],
    "d": [
        myMonadTall,
        layout.Max(),
    ],
    "f": [
        myMonadTall,
        layout.Max(),
    ],
    "g": [
        layout.Max(),
    ],
}

myMatches = {
    "a": None,
    "s": None,
    "d": None,
    "f": None,
    "g": [Match(wm_class=["chromium"])]
}

groups = [Group(i, layouts=myLayouts[i], matches=myMatches[i]) for i in "asdfg"]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

widget_defaults = dict(
    font='Arial',
    fontsize=16,
    padding=3,
)

screens = [
    Screen(
        bottom=bar.Bar([
            widget.TextBox(
                text=u"Arch >",
                background=blue,
                foreground=black,
                markup=True
            ),
            widget.CurrentLayout(
                fontsize=16,
                background=gray,
                foreground=black
            ),
            widget.TextBox(
                text=u">",
                background=gray,
                foreground=black
            ),
            widget.Prompt(
                fontsize=16,
                background=yellow,
                foreground=gray,
                padding=0
            ),
            widget.TextBox(
                text=u"[",
                fontsize=16,
                background=black,
                foreground=gray,
                padding=0
            ),
            widget.WindowName(
                background=black,
                foreground=white
            ),
            widget.TextBox(
                text=u"]",
                fontsize=16,
                background=black,
                foreground=white,
                padding=0
            ),
            widget.TextBox(text=u"< Cpu", fontsize=16, background=black, foreground=gray,),
            widget.CPUGraph(graph_color='0066FF', fill_color='001188', border_width=1, line_width=1),

            widget.TextBox(text="< Mem", fontsize=16),
            widget.MemoryGraph(graph_color='22FF44', fill_color='11AA11', border_width=1, line_width=1),

            widget.TextBox(text="< Net", fontsize=16),
            widget.NetGraph(border_width=1, line_width=1),

            widget.TextBox(text="< Bat:", fontsize=16),
            widget.Battery(background=aqua, foreground=black),

            widget.TextBox('Vol:', fontsize=16, background=aqua, foreground=black),
            widget.Volume(background=aqua, foreground=black),

            widget.Clock(
                format=u'< %Y-%m-%d %H:%M',
                background=purple,
                foreground=black
            ),
            widget.Systray(
                background=black
            ),
        ], 20),
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
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus = blue,
    border_normal = gray,
    border_width = 2
)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

def main(qtile):
    qtile.cmd_warning()
