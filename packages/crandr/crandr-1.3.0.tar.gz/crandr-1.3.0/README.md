This is a unifying wrapper around [xrandr](https://wiki.archlinux.org/title/Xrandr) and [swaymsg](https://man.archlinux.org/man/sway-output.5.en) to control your monitors/outputs,
mainly intended for setups where only one or two monitors are enabled at the same time.

[xrandr's syntax](https://man.archlinux.org/man/xrandr.1) is too verbose for direct usage and too explicit to use it in an [i3](https://i3wm.org/)/[sway](https://swaywm.org/) config file.
This script tries to make things easier.

## Examples
- `crandr` cycles through all connected monitors.
- `crandr toggle` toggles between the internal monitor and an external monitor.
- `crandr extend left` turns on another monitor and positions it left of the currently enabled monitor.
- `crandr mirror` turns on another monitor and mirrors the displayed content.
  If the monitors have different resolutions the internal monitor is scaled to match the resolution of the external monitor.
  If you want another monitor to be scaled you can specify the monitor which should not be scaled with `--original`.
  (Sway does not support mirroring yet, see [this issue](https://github.com/swaywm/sway/issues/1666).)
- `crandr scale .8` if everything is displayed too small and you want to make things bigger.
- `crandr rotate left` rotates the content of the currently enabled monitor so that the top of the content is at the left edge of the monitor.
- `crandr reset external` enables the external monitor with default rotation and scaling and turns off all other monitors (the internal monitor).
- `crandr list` to list all connected monitors.

## Help
For more information see
- `crandr --help`
- `crandr cycle --help`
- `crandr toggle --help`
- `crandr extend --help`
- `crandr mirror --help`
- `crandr scale --help`
- `crandr rotate --help`
- `crandr reset --help`
- `crandr list --help`

## Installation

```bash
$ pipx install crandr
```

## Dependencies
- Python >= 3.8
- xrandr and RandR >= version 1.3 or swaymsg

### Dependencies for running the tests:
- [mypy](http://mypy-lang.org/)
- [pytest](https://henryiii.github.io/level-up-your-python/notebooks/3.1%20pytest.html)

## Alternatives
- [arandr](https://christian.amsuess.com/tools/arandr/) (for [X](https://en.wikipedia.org/wiki/X_Window_System)) and [wdisplays](https://github.com/artizirk/wdisplays) (for [wayland](https://wiki.archlinux.org/title/Wayland)) are graphical user interfaces to control monitors.
- [autorandr](https://github.com/phillipberndt/autorandr) (for X) and [kanshi](https://github.com/emersion/kanshi) (for wayland) are programs which automatically enable output profiles when connecting and disconnecting monitors.
