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

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([script])

alt_key = "mod1"
super_key = "mod4"
terminal = "kitty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([alt_key], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([alt_key], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([alt_key], "j", lazy.layout.down(), desc="Move focus down"),
    Key([alt_key], "k", lazy.layout.up(), desc="Move focus up"),
    Key([alt_key], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([alt_key, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([alt_key, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([alt_key, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([alt_key, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([alt_key, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([alt_key, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([alt_key, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([alt_key, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([alt_key], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    #Key( [alt_key, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
    Key([super_key], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([alt_key], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([alt_key], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [alt_key],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([alt_key], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([alt_key, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([alt_key, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([alt_key], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([alt_key, "shift"], "Return", lazy.spawn("rofi -show drun")),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [alt_key],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

colors = {
    "bg1": "1d2021",
    "bg2": "0b0e14",
    "red": '#e5555f',
    "yellow": '#ffde7a',
    "green": '#7ee787',
}

layouts = [
    layout.MonadTall(
        border_width=3,
        border_focus=colors['yellow'],
        border_normal=colors['bg1'],
        margin=8
    ),
]

widget_defaults = dict(
    font="Mononoki Nerd Font",
    fontsize=17,
    padding=7,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active='#7ee787',
                    inactive='#62afef',
                    highlight_method='block',
                    this_current_screen_border=colors["bg1"],
                    background=colors["bg2"],
                    padding=9
                ),
                widget.TextBox(
                    "",
                    foreground=colors["red"],
                    #background=colors["bg1"],
                ),
                widget.WindowName(
                    foreground=colors["red"],
                    #background=colors["bg1"],
                ),
                widget.Systray(),
                widget.TextBox(
                    "",
                    foreground=colors["yellow"]
                ),
                widget.CurrentLayout(
                    foreground=colors["yellow"]
                ),
                widget.TextBox(
                    "󰥔",
                    foreground=colors["green"]
                ),
                widget.Clock(
                    format="%Y/%m/%d %a %I:%M %p",
                    foreground=colors["green"]
                ),
            ],
            24,
            background=colors["bg2"]
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
floats_kept_above = True
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

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
