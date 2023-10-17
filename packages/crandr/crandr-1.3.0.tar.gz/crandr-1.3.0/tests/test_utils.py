#!/usr/bin/env python3

import pytest

from crandr import utils

@pytest.fixture(scope='module')
def formatter():
	return utils.MyFormatter()

class TestFormatterStandardFeatures:

	def test_format_int(self, formatter):
		result = formatter.format('that is {0}', 1)
		assert result == 'that is 1'

	def test_format_floats(self, formatter):
		result = formatter.format('{0:.2} != {1:.2}', 1/2, 1/3)
		assert result == '0.5 != 0.33'

	def test_format_str(self, formatter):
		result = formatter.format('hello {addressee}', addressee='world')
		assert result == 'hello world'

	def test_format_str_repr(self, formatter):
		result = formatter.format('a = {a!r}', a='')
		assert result == "a = ''"

	def test_format_empty(self, formatter):
		result = formatter.format('', foo=42)
		assert result == ''

	def test_format_list(self, formatter):
		l = ['hi', 'there']
		result = formatter.format('here and {l[1]}', l=l)
		assert result == 'here and there'

	def test_format_padding(self, formatter):
		result = formatter.format('|{0:>10}|{1:<10}|', 'hello', 'world')
		assert result == '|     hello|world     |'


class TestFormatterExtendedFeatures:

	def test_format_floats_in_parentheses(self, formatter):
		result = formatter.format('{"("0")":5.2f} != {"("1")":5.2f}', 1/2, 1/3)
		assert result == ' (0.50) !=  (0.33)'

	def test_format_prefix_and_suffix_are_omitted_if_value_is_empty(self, formatter):
		result = formatter.format('--{"[ "0" ]"}--', '')
		assert result == '----'

	def test_format_str_repr_with_prefix(self, formatter):
		result = formatter.format('a{" = "a!r}', a='')
		assert result == "a = ''"

	def test_format_example_1(self, formatter):
		result = formatter.format('{name:8}  {"["on"]":3}  {resolution}', name='DP-1', on='on', resolution='1920x1080')
		assert result == 'DP-1      [on]   1920x1080'

	def test_format_example_2(self, formatter):
		result = formatter.format('{name:8}  {"["on"]":3}  {resolution}', name='HDMI-2', on='off', resolution='1920x1080')
		assert result == 'HDMI-2    [off]  1920x1080'

	def test_format_default(self, formatter):
		class Monitor:
			name = 'eDP-1'
			connection = 'internal'
			on_str = 'on'
			default_resolution = '1600x900'
		m = Monitor
		pattern = '{m.name:8} {"("m.connection")":12}  {"["m.on_str"]":3}  {m.default_resolution}'
		result = formatter.format(pattern, m=m)
		assert result == 'eDP-1    (internal)      [on]   1600x900'

