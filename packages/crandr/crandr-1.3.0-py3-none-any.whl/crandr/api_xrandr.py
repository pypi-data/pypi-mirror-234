#!/usr/bin/env python3

import subprocess
import re
import typing
import shlex

from . import model


def is_available() -> bool:
	cmd = ['which', 'xrandr']
	try:
		subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return True
	except:
		return False


class Api(model.Api):

	encoding = 'utf-8'


	# ---------- meta ----------

	def print_version(self) -> None:
		subprocess.call(['xrandr', '--version'])


	# ---------- read ----------

	re_geometry = r'(?P<width>[0-9]+)x(?P<height>[0-9]+)\+(?P<offsetx>[0-9]+)\+(?P<offsety>[0-9]+)'
	re_connected = r'^(?P<name>[^\s]+) connected (primary )?(%s)?' % re_geometry
	reo_connected = re.compile(re_connected)
	re_available_resolution = r'\s+(?P<width>[0-9]+)x(?P<height>[0-9]+)\s+([0-9]+\.[0-9]+)((?P<on>\*)| )((?P<default>\+)| )'
	reo_available_resolution = re.compile(re_available_resolution)

	def _get_xrandr_output(self) -> typing.Sequence[str]:
		cmd = ['xrandr']
		p = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
		return p.stdout.decode(self.encoding).splitlines()

	def _read_test_file(self, fn: str) -> typing.Sequence[str]:
		with open(fn, 'rt') as f:
			return f.read().splitlines()

	def iter_connected_monitors(self, test_input: typing.Optional[str] = None) -> typing.Iterator[model.Monitor]:
		monitor = None
		if test_input:
			xrandr_output = self._read_test_file(test_input)
		else:
			xrandr_output = self._get_xrandr_output()

		for ln in xrandr_output:
			if m := self.reo_connected.match(ln):
				if monitor:
					yield monitor

				monitor = model.Monitor(
					name = m.group('name'),
					long_name = '',
					on = m.group('width') is not None,
				)
			elif m := self.reo_available_resolution.match(ln):
				assert monitor
				if monitor.default_resolution is None or m.group('default'):
					monitor.default_resolution = model.Resolution(int(m.group('width')), int(m.group('height')))

		assert monitor
		yield monitor


	# ---------- write ----------

	direction_map = {
		model.Direction.LEFT : '--left-of',
		model.Direction.RIGHT : '--right-of',
		model.Direction.ABOVE : '--above',
		model.Direction.BELOW : '--below',
	}

	rotation_map = {
		model.Rotation.NORMAL : 'normal',
		model.Rotation.INVERTED : 'inverted',
		model.Rotation.LEFT : 'left',
		model.Rotation.RIGHT : 'right',
	}

	def turn_off_and_on(self,
			monitors_to_be_turned_off: typing.Iterable[model.Monitor],
			monitors_to_be_turned_on: typing.Iterable[model.Monitor],
			*, primary: typing.Optional[model.Monitor] = None, verbose: bool, dry_run: bool) -> None:
		cmd = ['xrandr']
		for monitor in monitors_to_be_turned_off:
			cmd.extend(['--output', monitor.name, '--off'])
		for monitor in monitors_to_be_turned_on:
			cmd.extend(['--output', monitor.name])
			if monitor.position:
				cmd.append(self.direction_map[monitor.position.direction])
				cmd.append(monitor.position.reference_monitor.name)
			if monitor.same_as:
				cmd.append('--same-as')
				cmd.append(monitor.same_as.name)
			if monitor.resolution:
				cmd.append('--mode')
				cmd.append('{r.width}x{r.height}'.format(r=monitor.resolution))
			else:
				cmd.append('--auto')
			if monitor.scale:
				cmd.append('--scale')
				cmd.append(f'{monitor.scale.x}x{monitor.scale.y}')
			if monitor.rotation:
				cmd.append('--rotate')
				cmd.append(self.rotation_map[monitor.rotation])

		if primary:
			cmd.extend(['--output', primary.name, '--primary'])

		if verbose:
			print(shlex.join(cmd))
		if not dry_run:
			try:
				subprocess.run(cmd, check=True, text=True, stderr=subprocess.PIPE)
			except subprocess.CalledProcessError as e:
				m = re.match('xrandr: Configure crtc ([0-9]) failed', e.stderr)
				if m:
					crtc = m.group(1)
					if crtc == '0':
						crtc = '1'
					else:
						crtc = '0'
					#https://askubuntu.com/questions/136139/xrandr-configure-crtc-0-failed-when-trying-to-change-resolution-on-external-m
					cmd.extend(['--crtc',  '1'])
					if verbose:
						print(shlex.join(cmd))
					subprocess.run(cmd, check=True)
				else:
					print(e.stderr)



if __name__ == '__main__':
	api = Api()
	for m in api.iter_connected_monitors():
		print(m)
