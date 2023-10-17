#!/usr/bin/env python3

import pytest

from crandr import main
from test_without_config import *


@pytest.fixture
def use_swaymsg():
	main.DEFAULT_BACKEND = 'swaymsg'


class TestToggle:

	def test_toggle_from_default(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/default_eDP-1_DP-4.json'
		args = ['--dry-run', '--test-input', fn, 'toggle']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output \'"Ancor Communications Inc MX279 G8LMRS023461"\' enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output \'"Unknown 0x484E 0x00000000"\' disable',
		]

	def test_toggle_to_external(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'toggle']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output DP-4 enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output eDP-1 disable',
		]

	def test_toggle_to_internal(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/DP-4_ON_eDP-1_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'toggle']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output eDP-1 enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output DP-4 disable',
		]


class TestCycle:

	def test_cycle_from_default(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/default_eDP-1_DP-4.json'
		args = ['--dry-run', '--test-input', fn, 'cycle']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output \'"Unknown 0x484E 0x00000000"\' enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output \'"Ancor Communications Inc MX279 G8LMRS023461"\' disable',
		]

	def test_cycle_to_external(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'cycle']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output DP-4 enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output eDP-1 disable',
		]

	def test_cycle_to_internal(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/DP-4_ON_eDP-1_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'cycle']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output eDP-1 enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output DP-4 disable',
		]


class TestReset:

	def test_reset_turn_off(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/default_eDP-1_DP-4.json'
		args = ['--dry-run', '--test-input', fn, 'reset']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output \'"Unknown 0x484E 0x00000000"\' enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output \'"Ancor Communications Inc MX279 G8LMRS023461"\' disable',
		]

	def test_reset_stay_on_same_monitor_1(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/DP-4_ON_eDP-1_OFF.json'
		args = ['--dry-run', '--test-input', fn, 'reset']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output \'"Ancor Communications Inc MX279 G8LMRS023461"\' enable position 0 0 scale 1.0 transform normal',
		]

	def test_reset_stay_on_same_monitor_2(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'reset']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output eDP-1 enable position 0 0 scale 1.0 transform normal',
		]

	def test_reset_switch_monitor(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'reset', 'external']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output DP-4 enable position 0 0 scale 1.0 transform normal',
			'swaymsg -- output eDP-1 disable',
		]


class TestExtend:

	def test_extend_left(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, 'extend', 'left']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'swaymsg -- output \'"Ancor Communications Inc MX279 G8LMRS023461"\' enable position -1920 0 scale 1.0'

	def test_extend_right(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, 'extend', 'right']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'swaymsg -- output \'"Ancor Communications Inc MX279 G8LMRS023461"\' enable position 1600 0 scale 1.0'

	def test_extend_above(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'extend', 'above']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'swaymsg -- output DP-4 enable position 0 -1080 scale 1.0'

	def test_extend_below(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'extend', 'below']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip()
		assert cmd == 'swaymsg -- output DP-4 enable position 0 900 scale 1.0'


class TestMirror:

	def test_mirror_one(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'mirror']
		main.main(args)
		
		cmd = capsys.readouterr().out.rstrip().splitlines()
		assert cmd == [
			'swaymsg -- output eDP-1 enable position 0 0 mode 1600x900 scale 0.8333333333333334',
			'swaymsg -- output DP-4 enable position 0 0 mode 1920x1080 scale 1.0'
		]


class TestScale:

	def test_scale_big(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, 'scale', '.8']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'swaymsg -- output \'"Unknown 0x484E 0x00000000"\' enable position 0 0 scale 1.25'

	def test_scale_reset(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'scale', '1']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'swaymsg -- output eDP-1 enable position 0 0 scale 1.0'

	def test_scale_different_x_and_y_not_possible(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, 'scale', '.8x1.2']
		
		with pytest.raises(SystemExit) as e:
			main.main(args)
		
		assert e.type == SystemExit
		assert e.value.code == 1
		
		out, err = capsys.readouterr()
		cmd = out.rstrip()
		err = err.rstrip()
		
		assert cmd == ''
		assert err == 'swaymsg does not support different scales for x and y direction'


class TestRotate:

	def test_rotate_left_internal_monitor(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, 'rotate', 'left']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'swaymsg -- output \'"Unknown 0x484E 0x00000000"\' enable position 0 0 transform 270'

	def test_rotate_inverted_internal_monitor(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'rotate', 'inverted']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'swaymsg -- output eDP-1 enable position 0 0 transform 180'

	def test_rotate_right_external_monitor(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/DP-4_ON_eDP-1_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'rotate', 'right']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'swaymsg -- output DP-4 enable position 0 0 transform 90'

	def test_rotate_normal_external_monitor(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/DP-4_ON_eDP-1_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'rotate', 'normal']
		
		main.main(args)
		cmd = capsys.readouterr().out.rstrip()
		
		assert cmd == 'swaymsg -- output DP-4 enable position 0 0 transform normal'


class TestList:

	def test_list(self, use_swaymsg, capsys):
		fn = '_test-output/swaymsg/eDP-1_ON_DP-4_OFF.json'
		args = ['--dry-run', '--test-input', fn, '--use-short-names-on-sway', 'list']
		main.main(args)
		output = capsys.readouterr().out.rstrip()

		expected_output = '''\
eDP-1    (internal)      [on]   1600x900
DP-4     (display-port)  [off]  1920x1080'''

		assert output == expected_output
