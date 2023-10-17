#!/usr/bin/env python3

import pytest

from crandr import main
from test_without_config import *


@pytest.fixture
def use_xrandr():
	main.DEFAULT_BACKEND = 'xrandr'


class TestDefault:

	def test_default_is_cycle(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_ON__DP-1-2_OFF.txt'
		
		args = ['--dry-run', '--test-input', fn]
		main.main(args)
		cmd_default = capsys.readouterr().out.rstrip()
		
		args.append('cycle')
		main.main(args)
		cmd_cycle = capsys.readouterr().out.rstrip()
		
		assert cmd_default == cmd_cycle


class TestToggle:

	def test_toggle_to_internal_from_dp11(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_ON__DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'toggle']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-1 --off --output eDP-1 --auto --scale 1x1 --rotate normal'

	def test_toggle_to_internal_from_dp12(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_OFF_DP-1-2_ON_.txt'
		args = ['--dry-run', '--test-input', fn, 'toggle']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-2 --off --output eDP-1 --auto --scale 1x1 --rotate normal'

	def test_toggle_to_external(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__DP-1-1_OFF_DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'toggle']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output eDP-1 --off --output DP-1-1 --auto --scale 1x1 --rotate normal'


class TestCycle:

	def test_cycle_to_dp11(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__DP-1-1_OFF_DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'cycle']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output eDP-1 --off --output DP-1-1 --auto --scale 1x1 --rotate normal'

	def test_cycle_to_dp12(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_ON__DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'cycle']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-1 --off --output DP-1-2 --auto --scale 1x1 --rotate normal'

	def test_cycle_to_edp1(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_OFF_DP-1-2_ON_.txt'
		args = ['--dry-run', '--test-input', fn, 'cycle']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-2 --off --output eDP-1 --auto --scale 1x1 --rotate normal'


class TestReset:

	def test_reset_dont_switch_monitor(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_OFF_DP-1-2_ON_.txt'
		args = ['--dry-run', '--test-input', fn, 'reset']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-2 --auto --scale 1x1 --rotate normal'

	def test_reset_turn_off(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_mirror_HDMI-1_original.txt'
		args = ['--dry-run', '--test-input', fn, 'reset']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output HDMI-1 --off --output eDP-1 --auto --scale 1x1 --rotate normal'

	def test_reset_turn_other_off(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_mirror_HDMI-1_original.txt'
		args = ['--dry-run', '--test-input', fn, 'reset', 'external']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output eDP-1 --off --output HDMI-1 --auto --scale 1x1 --rotate normal'


class TestExtend:

	def test_extend_left(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_ON__DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'extend', 'left']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-2 --left-of DP-1-1 --auto --scale 1x1 --output DP-1-1 --primary'

	def test_extend_left_internal(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_ON__DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'extend', 'left', 'internal']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output eDP-1 --left-of DP-1-1 --auto --scale 1x1 --output DP-1-1 --primary'

	def test_extend_right(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_ON__DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'extend', 'right', 'external']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-2 --right-of DP-1-1 --auto --scale 1x1 --output DP-1-1 --primary'

	def test_extend_above(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__DP-1-1_OFF_DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'extend', 'above']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-1 --above eDP-1 --auto --scale 1x1 --output eDP-1 --primary'

	def test_extend_below(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__DP-1-1_OFF_DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'extend', 'below', 'external']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output DP-1-1 --below eDP-1 --auto --scale 1x1 --output eDP-1 --primary'


class TestMirror:

	def test_mirror_one(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__HDMI-1_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'mirror']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output eDP-1 --same-as HDMI-1 --mode 1600x900 --scale 1.2x1.2 --output HDMI-1 --mode 1920x1080 --scale 1x1'

	def test_mirror_change_original(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_mirror_HDMI-1_original.txt'
		args = ['--dry-run', '--test-input', fn, 'mirror', '--original', 'internal']
		main.main(args)

		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'xrandr --output eDP-1 --mode 1600x900 --scale 1x1 --output HDMI-1 --same-as eDP-1 --mode 1920x1080 --scale 0.8333333333333334x0.8333333333333334'


class TestScale:

	def test_scale_wide(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__HDMI-1_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'scale', '.8x1.2']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'xrandr --output eDP-1 --auto --scale 0.8x1.2'

	def test_scale_reset(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__HDMI-1_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'scale', '1']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'xrandr --output eDP-1 --auto --scale 1.0x1.0'


class TestRotate:

	def test_rotate_left(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_ON__HDMI-1_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'rotate', 'left']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'xrandr --output eDP-1 --auto --rotate left'

	def test_rotate_invert_two_monitors(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_left-of_DP-1-2.txt'
		args = ['--dry-run', '--test-input', fn, 'rotate', 'inverted']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'xrandr --output eDP-1 --auto --rotate inverted --output DP-1-2 --auto --rotate inverted'

	def test_rotate_right_external_monitor(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_left-of_DP-1-2.txt'
		args = ['--dry-run', '--test-input', fn, 'rotate', 'right', 'external']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'xrandr --output DP-1-2 --auto --rotate right'

	def test_rotate_normal_internal_monitor(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_left-of_DP-1-2.txt'
		args = ['--dry-run', '--test-input', fn, 'rotate', 'normal', 'internal']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'xrandr --output eDP-1 --auto --rotate normal'


class TestList:

	def test_list(self, use_xrandr, capsys):
		fn = '_test-output/xrandr/eDP-1_OFF_DP-1-1_ON__DP-1-2_OFF.txt'
		args = ['--dry-run', '--test-input', fn, 'list']
		main.main(args)
		output = capsys.readouterr().out.rstrip()

		expected_output = '''\
eDP-1    (internal)      [off]  1600x900
DP-1-1   (display-port)  [on]   1920x1080
DP-1-2   (display-port)  [off]  1920x1080'''

		assert output == expected_output
