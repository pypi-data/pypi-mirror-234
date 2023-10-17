#!/usr/bin/env python3

from __future__ import annotations

import fnmatch
import enum
import typing

CONNECTION_INTERNAL = 'internal'
CONNECTION_DP = 'display-port'
CONNECTION_HDMI = 'hdmi'
CONNECTION_VGA = 'vga'
name_to_connection: typing.MutableMapping[str, str] = {}
EXTERNAL_CONNECTIONS = (CONNECTION_DP, CONNECTION_HDMI, CONNECTION_VGA)
ALL_CONNECTIONS = (CONNECTION_INTERNAL,) + EXTERNAL_CONNECTIONS


class Monitor:

	__slots__ = ('name', 'long_name', 'on', 'position', 'default_resolution', 'same_as', 'resolution', 'scale', 'rotation')

	@property
	def connection(self) -> str:
		for name in sorted(name_to_connection, key=len, reverse=True):
			if fnmatch.fnmatchcase(self.name, name):
				return name_to_connection[name]
		if self.name.startswith("DP"):
			return CONNECTION_DP
		if self.name.startswith("HDMI"):
			return CONNECTION_HDMI
		if self.name.startswith("VGA"):
			return CONNECTION_VGA
		else:
			return CONNECTION_INTERNAL

	def __init__(self, *, name: str, long_name:str, on: bool,
			default_resolution: typing.Optional['Resolution'] = None,
			position: typing.Optional['Position'] = None) -> None:
		# read
		self.name = name
		self.long_name = long_name
		self.on = on
		self.default_resolution = default_resolution

		# write
		self.position = position
		self.same_as: typing.Optional[Monitor] = None
		self.resolution: typing.Optional[Resolution] = None
		self.scale: typing.Optional[Scale] = None
		self.rotation: typing.Optional[Rotation] = None

	def __repr__(self) -> str:
		attrs = ', '.join('%s=%r' % (attr, getattr(self, attr)) for attr in self.__slots__)
		return "%s(%s)" % (type(self).__name__, attrs)

	@property
	def on_str(self) -> str:
		if self.on:
			return "on"
		else:
			return "off"


@enum.unique
class Direction(enum.Enum):

	LEFT = 'left'
	RIGHT = 'right'
	ABOVE = 'above'
	BELOW = 'below'

class Position:

	__slots__ = ('direction', 'reference_monitor')

	def __init__(self, direction: Direction, reference_monitor: Monitor):
		self.direction = direction
		self.reference_monitor = reference_monitor


class Resolution:

	__slots__ = ('width', 'height')

	def __init__(self, width: int, height: int):
		self.width = width
		self.height = height

	def __truediv__(self, other: Resolution) -> Scale:
		if not isinstance(other, Resolution):
			return NotImplemented
		return Scale(
			self.width / other.width,
			self.height / other.height,
		)

	def __str__(self) -> str:
		return f'{self.width}x{self.height}'

class Scale:

	__slots__ = ('x', 'y')

	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y

	@classmethod
	def parse(cls, s: str) -> Scale:
		if 'x' in s:
			sx, sy = s.split('x', 1)
			x = float(sx)
			y = float(sy)
		else:
			x = float(s)
			y = x

		return cls(x, y)


@enum.unique
class Rotation(enum.Enum):

	NORMAL = 'normal'
	INVERTED = 'inverted'
	LEFT = 'left'
	RIGHT = 'right'


class NotSupportedException(Exception):
	 pass


class Api:

	def __init__(self, **kw: typing.Mapping[str, typing.Any]) -> None:
		pass

	def print_version(self) -> None:
		raise NotImplementedError()

	def iter_connected_monitors(self, test_input: typing.Optional[str] = None) -> typing.Iterator[Monitor]:
		raise NotImplementedError()

	def turn_off_and_on(self,
			monitors_to_be_turned_off: typing.Iterable[Monitor],
			monitors_to_be_turned_on: typing.Iterable[Monitor],
			*, primary: typing.Optional[Monitor] = None, verbose: bool, dry_run: bool) -> None:
		raise NotImplementedError()


if __name__ == '__main__':
	pass
