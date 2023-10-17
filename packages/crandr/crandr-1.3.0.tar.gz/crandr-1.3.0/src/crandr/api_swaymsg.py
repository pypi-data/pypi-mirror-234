#!/usr/bin/env python3

import subprocess
import json
import typing
import shlex

from . import model


def is_available() -> bool:
	cmd = ['which', 'swaymsg']
	try:
		subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return True
	except:
		return False


class Api(model.Api):

	encoding = 'utf-8'

	def __init__(self, **kw: typing.Mapping[str, typing.Any]) -> None:
		self.use_short_names = typing.cast(bool, kw.get('use_short_names_on_sway', False))


	# ---------- meta ----------

	def print_version(self) -> None:
		subprocess.call(['swaymsg', '--version'])


	# ---------- read ----------

	def _get_outputs(self) -> str:
		cmd = ['swaymsg', '-t', 'get_outputs']
		p = subprocess.run(cmd, stdout=subprocess.PIPE, check=True)
		return p.stdout.decode(self.encoding)

	def _read_test_file(self, fn: str) -> str:
		with open(fn, 'rt') as f:
			return f.read()

	def iter_connected_monitors(self, test_input: typing.Optional[str] = None) -> typing.Iterator[model.Monitor]:
		monitor = None
		if test_input:
			outputs_str = self._read_test_file(test_input)
		else:
			outputs_str = self._get_outputs()

		outputs = json.loads(outputs_str)
		for o in outputs:
			default_mode = o['modes'][-1]
			yield model.Monitor(
				name = o['name'],
				long_name = '"%s %s %s"' % (o['make'], o['model'], o['serial']),
				on = o['active'],
				default_resolution = model.Resolution(
					default_mode['width'],
					default_mode['height'],
				)
			)


	# ---------- write ----------

	rotation_map = {
		model.Rotation.NORMAL : 'normal',
		model.Rotation.RIGHT : '90',
		model.Rotation.INVERTED : '180',
		model.Rotation.LEFT : '270',
	}

	def turn_off_and_on(self,
			monitors_to_be_turned_off: typing.Iterable[model.Monitor],
			monitors_to_be_turned_on: typing.Iterable[model.Monitor],
			*, primary: typing.Optional[model.Monitor] = None, verbose: bool, dry_run: bool) -> None:
		get_name: typing.Callable[[model.Monitor], str]
		if self.use_short_names:
			get_name = lambda m: m.name
		else:
			get_name = lambda m: m.long_name
		for monitor in monitors_to_be_turned_on:
			x, y = self._calc_position(monitor)
			cmd = ['swaymsg', '--', 'output', get_name(monitor), 'enable', 'position', f'{x}', f'{y}']
			if monitor.resolution:
				cmd.append('mode')
				cmd.append('{r.width}x{r.height}'.format(r=monitor.resolution))
			if monitor.scale:
				if monitor.scale.x != monitor.scale.y:
					raise model.NotSupportedException('swaymsg does not support different scales for x and y direction')
				scale = 1 / monitor.scale.x
				cmd.append('scale')
				cmd.append(f'{scale}')
			if monitor.rotation:
				cmd.append('transform')
				cmd.append(self.rotation_map[monitor.rotation])
			self._run_swaymsg(cmd, verbose=verbose, dry_run=dry_run)
		for monitor in monitors_to_be_turned_off:
			cmd = ['swaymsg', '--', 'output', get_name(monitor), 'disable']
			self._run_swaymsg(cmd, verbose=verbose, dry_run=dry_run)

	def _calc_position(self, monitor: model.Monitor) -> typing.Tuple[int, int]:
		#TODO: consider scale
		def get_resolution(m: model.Monitor) -> model.Resolution:
			if m.resolution:
				return m.resolution
			else:
				assert m.default_resolution
				return m.default_resolution

		# the position specifies the top left corner
		# the y axis is pointing downward
		if monitor.position is None:
			x = 0
			y = 0
		elif monitor.position.direction == model.Direction.LEFT:
			x = - get_resolution(monitor).width
			y = 0
		elif monitor.position.direction == model.Direction.RIGHT:
			x = get_resolution(monitor.position.reference_monitor).width
			y = 0
		elif monitor.position.direction == model.Direction.ABOVE:
			x = 0
			y = - get_resolution(monitor).height
		elif monitor.position.direction == model.Direction.BELOW:
			x = 0
			y = get_resolution(monitor.position.reference_monitor).height
		else:
			assert False

		return x, y

	def _run_swaymsg(self, cmd: typing.Sequence[str], *, verbose: bool, dry_run: bool) -> None:
		if verbose:
			print(shlex.join(cmd))
		if not dry_run:
			subprocess.run(cmd, check=True)


if __name__ == '__main__':
	api = Api()
	for m in api.iter_connected_monitors():
		print(m)
