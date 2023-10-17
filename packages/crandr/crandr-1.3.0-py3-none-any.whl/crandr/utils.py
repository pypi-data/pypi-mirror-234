#!/usr/bin/env python3

import string
import re
import typing

class MyFormatter(string.Formatter):

	"""
	This should be fully compatible with the default Formatter but adds one feature:
	A prefix and suffix can be specified inside of the field name, wrapped in single or double quotes.
	If the resulting value is not empty the prefix is inserted after leading white space and
	the suffix is inserted before trailing white space.
	Prefix and suffix do not count in to the padding length.
	
	>>> MyFormatter().format('{name:8}  {"["on"]":3}  {resolution}', name='DP-1', on='on', resolution='1920x1080')
	'DP-1      [on]   1920x1080'
	>>> MyFormatter().format('{name:8}  {"["on"]":3}  {resolution}', name='HDMI-2', on='off', resolution='1920x1080')
	'HDMI-2    [off]  1920x1080'
	"""

	QUOTES = ('"', "'")

	def get_field(self, field_name: str, args: typing.Sequence[typing.Any], kwargs: typing.Mapping[str, typing.Any]) -> typing.Tuple[typing.Tuple[str, typing.Any, str], str]:
		prefix = ""
		suffix = ""
		if field_name:
			if field_name[0] in self.QUOTES:
				quote = field_name[0]
				i = field_name.index(quote, 1)
				prefix = field_name[1:i]
				field_name = field_name[i+1:]
			if field_name[-1] in self.QUOTES:
				quote = field_name[-1]
				i = field_name.rindex(quote, 0, -1)
				suffix = field_name[i+1:-1]
				field_name = field_name[:i]
		
		value, used_key = super().get_field(field_name, args, kwargs)
		return (prefix, value, suffix), used_key

	def convert_field(self, value_tuple: typing.Tuple[str, typing.Any, str], conversion: str) -> typing.Tuple[str, str, str]:
		prefix, value, suffix = value_tuple
		formatted_value = super().convert_field(value, conversion)
		return prefix, formatted_value, suffix

	def format_field(self, value_tuple: typing.Tuple[str, typing.Any, str], format_spec: str) -> typing.Any:
		prefix, value, suffix = value_tuple
		formatted_value = super().format_field(value, format_spec)
		if value:
			m = re.match(r'(\s*)(.*?)(\s*)$', formatted_value)
			assert m
			formatted_value = m.group(1) + prefix + m.group(2) + suffix + m.group(3)
		return formatted_value


if __name__ == '__main__':
	class Monitor:
		on_str = 'on'
		name = 'HDMI-1'
		connection = 'vga'
		default_resolution = "1920x1080"

	pattern = '{m.name:8} {"("m.connection")":12}  {"["m.on_str"]"!s:3}  {m.default_resolution}'
	out = MyFormatter().format(pattern, m=Monitor())
	print(out)
