#!/usr/bin/env python3

# Copyright © 2022 erzo <erzo@posteo.de>
# This work is free. You can use, copy, modify, and/or distribute it
# under the terms of the BSD Zero Clause License, see LICENSE.

"""
This is a unifying wrapper around xrandr and swaymsg to control your monitors/outputs,
mainly intended for setups where only one or two monitors are enabled at the same time.

All sub commands take an optional connections argument to specify which monitor you want to use.
Unfortunately it's value is not always as expected. For example xrandr reports my VGA port as DP-2
and one of the display ports as HDMI-1.
You can check the connection name to use with list, it is given in parentheses after the name.
You can manually set a connection name with `crandr config`.
"""

import os
import sys
import time
import argparse
import subprocess
import shlex
import typing
import importlib
import pkgutil
import configparser

from . import model
from . import utils
from . import config_paths
from .version import __version__

APP_NAME = 'crandr'

BACKENDS = {
	'swaymsg' : '.api_swaymsg',
	'xrandr' : '.api_xrandr',
	'auto' : None,
}
DEFAULT_BACKEND = 'auto'

CONNECTION_ANY = 'any'
CONNECTION_EXTERNAL = 'external'
ALL_CONNECTION_VALUES = (CONNECTION_ANY, CONNECTION_EXTERNAL) + model.ALL_CONNECTIONS


# ---------- parse config file ----------

def parse_config() -> None:
	SECTION_MAP_NAME_TO_CONNECTION = 'map-name-to-connection'
	ALLOWED_SECTIONS = [SECTION_MAP_NAME_TO_CONNECTION]
	
	fn = config_paths.ConfigPathFinder(APP_NAME).get_existing_config_file()
	if not fn:
		return None
	
	class MyConfigParser(configparser.ConfigParser):
		# avoid conversion to lower case
		def optionxform(self, x: str) -> str:
			return x
	
	parser = MyConfigParser(
		allow_no_value = False,
		strict = True,
		empty_lines_in_values = False,
		interpolation = None,
	)
	
	try:
		parser.read(fn)
	except Exception as e:
		config_error(fn, e)
	
	for section in parser.sections():
		if section not in ALLOWED_SECTIONS:
			config_error(fn, 'unknown section %r, should be one of %s' % (section, ', '.join('%r' % s for s in ALLOWED_SECTIONS)))
	
	if SECTION_MAP_NAME_TO_CONNECTION in parser:
		mappings = parser[SECTION_MAP_NAME_TO_CONNECTION]
		for name, connection in mappings.items():
			if connection in model.ALL_CONNECTIONS:
				model.name_to_connection[name] = connection
			else:
				config_error(fn, 'invalid connection %r, should be one of %s' % (connection, ', '.join('%r' % c for c in model.ALL_CONNECTIONS)))

def config_error(fn: str, error: typing.Union[str, Exception]) -> None:
	print('error in config file %s:' % fn, file=sys.stderr)
	print(error, file=sys.stderr)
	sys.exit(2)


# ---------- enable one monitor ----------

def default(api: model.Api, args: argparse.Namespace) -> None:
	args.connections = model.ALL_CONNECTIONS
	cycle(api, args)

def cycle(api: model.Api, args: argparse.Namespace) -> None:
	'''cycle through all connected monitors, turning on one at a time'''
	monitors = list(api.iter_connected_monitors(test_input=args.test_input))
	if not monitors:
		print("no monitors connected", file=sys.stderr)
		sys.exit(1)

	monitors_to_be_turned_off = []
	monitor_to_be_turned_on = None

	was_last_on = False
	for m in monitors:
		if m.on:
			monitors_to_be_turned_off.append(m)
			was_last_on = True
		elif was_last_on and m.connection in args.connections:
			monitor_to_be_turned_on = m
			was_last_on = False

	if monitor_to_be_turned_on is None:
		for m in monitors:
			if m.connection in args.connections:
				monitor_to_be_turned_on = m
				break
		else:
			monitor_to_be_turned_on = get_fallback_monitor(monitors, args.connections)
		if monitor_to_be_turned_on in monitors_to_be_turned_off:
			monitors_to_be_turned_off.remove(monitor_to_be_turned_on)

	monitor_to_be_turned_on.scale = model.Scale(1, 1)
	monitor_to_be_turned_on.rotation = model.Rotation.NORMAL
	monitors_to_be_turned_on = [monitor_to_be_turned_on]
	api.turn_off_and_on(monitors_to_be_turned_off, monitors_to_be_turned_on, verbose=args.verbose, dry_run=args.dry_run)

def toggle(api: model.Api, args: argparse.Namespace) -> None:
	'''toggle between two connections'''
	monitors = list(api.iter_connected_monitors(test_input=args.test_input))
	if not monitors:
		print("no monitors connected", file=sys.stderr)
		sys.exit(1)
	
	monitors_to_be_turned_off = [m for m in monitors if m.on]
	
	if monitors_to_be_turned_off and monitors_to_be_turned_off[0].connection in args.connections1:
		connections = args.connections2
	else:
		connections = args.connections1

	for m in monitors:
		if not m.on and m.connection in connections:
			monitor_to_be_turned_on = m
			break
	else:
		alternative_connections = args.connections1 if connections is args.connections2 else args.connections2
		monitor_to_be_turned_on = get_fallback_monitor(monitors, connections, alternative_connections)
		if monitor_to_be_turned_on in monitors_to_be_turned_off:
			monitors_to_be_turned_off.remove(monitor_to_be_turned_on)
	
	monitor_to_be_turned_on.scale = model.Scale(1, 1)
	monitors_to_be_turned_on = [monitor_to_be_turned_on]
	monitor_to_be_turned_on.rotation = model.Rotation.NORMAL
	api.turn_off_and_on(monitors_to_be_turned_off, monitors_to_be_turned_on, verbose=args.verbose, dry_run=args.dry_run)

def reset(api: model.Api, args: argparse.Namespace) -> None:
	'''turn off other monitors after extend or mirror and reset scaling and rotation after rotate, scale and mirror'''
	monitors = list(api.iter_connected_monitors(test_input=args.test_input))
	if not monitors:
		print("no monitors connected", file=sys.stderr)
		sys.exit(1)
	
	monitor_to_be_on = get_fallback_monitor(monitors, args.connections)
	monitor_to_be_on.scale = model.Scale(1, 1)
	monitor_to_be_on.rotation = model.Rotation.NORMAL
	
	monitors_to_be_turned_off = [m for m in monitors if m.on and m is not monitor_to_be_on]
	monitors_to_be_turned_on = [monitor_to_be_on]
	api.turn_off_and_on(monitors_to_be_turned_off, monitors_to_be_turned_on, verbose=args.verbose, dry_run=args.dry_run)

def get_fallback_monitor(monitors: typing.List[model.Monitor], connections: typing.Container[str], alternative_connections: typing.Container[str] = []) -> model.Monitor:
	monitors.sort(key=lambda m: 4*(m.connection in connections) + 2*(m.connection in alternative_connections) + m.on, reverse=True)
	return monitors[0]


# ---------- enable a second monitor ----------

def extend(api: model.Api, args: argparse.Namespace) -> None:
	'''turn on a second monitor'''
	monitors = list(api.iter_connected_monitors(test_input=args.test_input))
	if not monitors:
		print("no monitors connected", file=sys.stderr)
		sys.exit(1)
	
	direction: model.Direction = args.direction
	try:
		reference_monitor = next(m for m in monitors if m.on)
	except StopIteration:
		print("no monitor turned on, I don't know which monitor to use as reference", file=sys.stderr)
		sys.exit(1)
	
	monitors_to_be_turned_off: typing.Final[typing.List[model.Monitor]] = []
	monitors_to_be_turned_on = [m for m in monitors if not m.on and m.connection in args.connections]
	monitors_to_be_turned_on.sort(key = lambda m: 0 if m.connection != model.CONNECTION_INTERNAL else 1)
	if not monitors_to_be_turned_on:
		print("no further monitor to be turned on in %s" % ",".join(args.connections))
		sys.exit(1)
	
	monitors_to_be_turned_on = monitors_to_be_turned_on[:1]
	monitors_to_be_turned_on[0].position = model.Position(direction, reference_monitor)
	monitors_to_be_turned_on[0].scale = model.Scale(1, 1)
	
	api.turn_off_and_on(monitors_to_be_turned_off, monitors_to_be_turned_on, primary=reference_monitor, verbose=args.verbose, dry_run=args.dry_run)

def mirror(api: model.Api, args: argparse.Namespace) -> None:
	'''turn on all monitors and mirror the content'''
	monitors = list(api.iter_connected_monitors(test_input=args.test_input))
	if not monitors:
		print("no monitors connected", file=sys.stderr)
		sys.exit(1)
	
	monitors_to_be_turned_off: typing.Final[typing.List[model.Monitor]] = []
	monitors_to_be_turned_on = [m for m in monitors if m.on]
	for m in monitors:
		if not m.on and m.connection in args.connections:
			monitors_to_be_turned_on.append(m)
	
	if len(monitors_to_be_turned_on) < 2:
		print("no second monitor to turn on", file=sys.stderr)
		sys.exit(1)
	
	try:
		original = next(m for m in monitors_to_be_turned_on if m.connection in args.original)
	except StopIteration:
		print("monitor chosen as original does not exist or is not active", file=sys.stderr)
		sys.exit(1)
	
	original.resolution = original.default_resolution
	assert original.resolution
	for m in monitors_to_be_turned_on:
		if m is not original:
			m.resolution = m.default_resolution
			assert m.resolution
			m.same_as = original
			m.scale = original.resolution / m.resolution
		else:
			m.scale = model.Scale(1, 1)
	
	api.turn_off_and_on(monitors_to_be_turned_off, monitors_to_be_turned_on, verbose=args.verbose, dry_run=args.dry_run)
	
	if api.__module__.endswith('api_swaymsg'):
		print('mirroring is not yet implemented in sway [February 2022]', file=sys.stderr)
		print('but I have set things up so that floating windows appear on both monitors', file=sys.stderr)
		print('using wayvnc + vinagre might be a better option, though', file=sys.stderr)
		print('https://github.com/swaywm/sway/issues/1666', file=sys.stderr)


# ---------- tweak monitors which are already turned on ----------

def rotate(api: model.Api, args: argparse.Namespace) -> None:
	'''rotate the monitor which is currently turned on'''
	monitors_to_be_rotated = [m for m in api.iter_connected_monitors(test_input=args.test_input) if m.on and m.connection in args.connections]
	if not monitors_to_be_rotated:
		print("no monitors to be rotated", file=sys.stderr)
		sys.exit(1)
	
	for m in monitors_to_be_rotated:
		m.rotation = args.rotation
	
	api.turn_off_and_on([], monitors_to_be_rotated, verbose=args.verbose, dry_run=args.dry_run)

def scale(api: model.Api, args: argparse.Namespace) -> None:
	'''scale the monitor which is currently turned on'''
	monitors_to_be_scaled = [m for m in api.iter_connected_monitors(test_input=args.test_input) if m.on and m.connection in args.connections]
	if not monitors_to_be_scaled:
		print("no monitors to be scaled", file=sys.stderr)
		sys.exit(1)
	
	for m in monitors_to_be_scaled:
		m.scale = args.scale
	
	api.turn_off_and_on([], monitors_to_be_scaled, verbose=args.verbose, dry_run=args.dry_run)


# ---------- list monitors ----------

def ls(api: model.Api, args: argparse.Namespace) -> None:
	'''list all connected monitors'''
	formatter = utils.MyFormatter()
	for m in api.iter_connected_monitors(test_input=args.test_input):
		if m.connection in args.connections:
			print(formatter.format(args.format, m=m))


# ---------- config ----------

def config(api: model.Api, args: argparse.Namespace) -> None:
	config_finder = config_paths.ConfigPathFinder(APP_NAME)
	if args.list_searched_paths:
		for searched_path in config_finder.iter_possible_config_files():
			print(searched_path)
	elif args.print_file_name:
		fn = config_finder.get_existing_config_file()
		if fn:
			print(fn)
	else:
		editor = os.environ.get('EDITOR', None)
		if not editor:
			if args.edit:
				editor = 'vi'
			else:
				config_fallback(config_finder)
				return
		fn = config_finder.get_existing_config_file()
		if not fn:
			fn = next(config_finder.iter_possible_config_files())
			path = os.path.split(fn)[0]
			resource_example_config = 'doc/example_config'
			if args.verbose:
				print(f'os.makedirs({path!r}, exist_ok=True)')
				print(f'cp {resource_example_config!r} {fn!r}')
			if not args.dry_run:
				os.makedirs(path, exist_ok=True)
				with open(fn, 'wt') as f:
					f.write(get_resource_content(resource_example_config))
		cmd = editor + ' ' + shlex.quote(fn)
		if args.verbose:
			print(cmd)
		if not args.dry_run:
			subprocess.run(cmd, shell=True)
			parse_config()

def config_fallback(config_finder: config_paths.ConfigPathFinder) -> None:
	print('[not opening config file because EDITOR is not defined]')
	fn = config_finder.get_existing_config_file()
	if fn:
		print(fn)
	else:
		print('no config file existing')
		print('the following paths are searched:')
		for searched_path in config_finder.iter_possible_config_files():
			print('- %s' % searched_path)

def get_resource_content(resource_name: str) -> str:
	#https://stackoverflow.com/a/58941536
	raw = pkgutil.get_data(__name__, resource_name)
	assert raw is not None
	return raw.decode('utf-8')


# ---------- version ----------

def print_version(args: argparse.Namespace) -> None:
	'''show the version of this program and the used backend and exit'''
	print(f'{APP_NAME} {__version__}')
	# I am deliberately calling get_api only after printing the version number of this program in case get_api fails
	get_api(args).print_version()
	sys.exit(0)


# ---------- main ----------

def create_parser() -> argparse.ArgumentParser:
	root_parser = argparse.ArgumentParser(APP_NAME, description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	subparsers = root_parser.add_subparsers(title='command')
	possible_connections = ','.join(f'{ac}' for ac in ALL_CONNECTION_VALUES)

	def add_subparser(func: typing.Callable[[model.Api, argparse.Namespace], None], *, name: str='') -> argparse.ArgumentParser:
		if not name:
			name = func.__name__
		parser = subparsers.add_parser(name, help=func.__doc__, description=func.__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
		parser.set_defaults(func=func)
		return parser

	def connection(connections: str) -> typing.List[str]:
		if connections == CONNECTION_ANY:
			return list(model.ALL_CONNECTIONS)
		if connections == CONNECTION_EXTERNAL:
			return list(model.EXTERNAL_CONNECTIONS)

		connections_list = connections.split(',')
		for c in connections_list:
			if c not in model.ALL_CONNECTIONS:
				raise argparse.ArgumentTypeError(f'invalid connection {c!r}, should be one of {possible_connections}')
		return connections_list

	root_parser.set_defaults(func=default)
	root_parser.add_argument('--version', action='store_true', help=print_version.__doc__)
	root_parser.add_argument('-n', '--dry-run', action='store_true', help='do not run the command to change the monitors (implies --verbose)')
	root_parser.add_argument('-v', '--verbose', action='store_true', help='print the command to change the monitors')
	root_parser.add_argument('--test-input', help='a file which contains the output of the backend')
	root_parser.add_argument('--backend', default=DEFAULT_BACKEND, choices=BACKENDS.keys(), help='the command used to configure the monitors')
	root_parser.add_argument('--use-short-names-on-sway', action='store_true', help='[swaymsg only] use names like eDP-1 and DP-4. These names can change when disconnecting and reconnecting a monitor which can lead to a situation where all monitors are disabled even after reconnecting a previously enabled monitor. Therefore the default behavior is to use longer names based on make, model and serial, see man sway-output.')
	root_parser.add_argument('--wait', type=float, help='time to wait before starting, this may help if you are experiencing trouble when binding this command to a key on sway')

	parser = add_subparser(cycle)
	parser.add_argument('connections', type=connection, nargs='?', default=CONNECTION_ANY, help=f'a comma separated list of connections which should be considered for activation: {possible_connections}')

	parser = add_subparser(toggle)
	parser.add_argument('connections1', type=connection, nargs='?', default=CONNECTION_EXTERNAL, help=f'one of {possible_connections}')
	parser.add_argument('connections2', type=connection, nargs='?', default=model.CONNECTION_INTERNAL, help=f'one of {possible_connections}')

	parser = add_subparser(extend)
	parser.add_argument('direction', type=model.Direction, help='one of %s' % ', '.join(d.value for d in model.Direction))
	parser.add_argument('connections', type=connection, nargs='?', default=CONNECTION_ANY, help=f'a comma separated list of connections which should be considered for activation: {possible_connections}')

	parser = add_subparser(mirror)
	parser.add_argument('-o', '--original', type=connection, default=CONNECTION_EXTERNAL, help='the content on this screen is always displayed at 100%%, if the other screen has a different resolution it will be scaled there')
	parser.add_argument('connections', type=connection, nargs='?', default=CONNECTION_ANY, help=f'a comma separated list of connections which should be considered for activation: {possible_connections}')

	parser = add_subparser(scale)
	parser.add_argument('scale', type=model.Scale.parse, help=f'<scale_x>[x<scale_y>], if scale_y is omitted it is set to scale_x. If you pass a 2 everything on the monitor will be half as big so that twice as much will fit on it. Pass 1 to return to normal. Sway does not support different scale values for x and y direction.')
	parser.add_argument('connections', type=connection, nargs='?', default=CONNECTION_ANY, help=f'a comma separated list of connections which should be scaled: {possible_connections}')

	parser = add_subparser(rotate)
	parser.add_argument('rotation', type=model.Rotation, help='one of %s' % ', '.join(r.value for r in model.Rotation))
	parser.add_argument('connections', type=connection, nargs='?', default=CONNECTION_ANY, help=f'a comma separated list of connections which should be rotated: {possible_connections}')

	parser = add_subparser(reset)
	parser.add_argument('connections', type=connection, nargs='?', default=CONNECTION_ANY, help=f'a comma separated list of connections out of which the first is kept on: {possible_connections}')

	parser = add_subparser(ls, name='list')
	parser.add_argument('connections', type=connection, nargs='?', default=CONNECTION_ANY, help=f'a comma separated list of connections which should be printed: {possible_connections}')
	parser.add_argument('-f', '--format', default='{m.name:8} {"("m.connection")":12}  {"["m.on_str"]":3}  {m.default_resolution}', help=f'the pattern of the lines to be printed')

	parser = add_subparser(config)
	parser.add_argument('-l', '--list-searched-paths', action='store_true', help='list all config file names which are checked for existence')
	parser.add_argument('-p', '--print-file-name', action='store_true', help='print the path of the config file or nothing if no config file is found')
	parser.add_argument('-e', '--edit', action='store_true', help='open the config file in EDITOR')

	#parser = subparsers.add_parser('load', help='load a configuration')
	#parser.set_defaults(func=load)

	return root_parser

def get_api(args: argparse.Namespace) -> model.Api:
	name: str = args.backend
	module = BACKENDS[name]
	if module:
		api_module = importlib.import_module(module, APP_NAME)
	else:
		for module in BACKENDS.values():
			if not module:
				continue
			api_module = importlib.import_module(module, APP_NAME)
			if api_module.is_available():
				break
		else:
			print('Failed to find an available backend. The following are supported but none of them seems to be installed:', file=sys.stderr)
			for backend in BACKENDS:
				print(f'- {backend}', file=sys.stderr)
			sys.exit(1)
	
	api: model.Api = api_module.Api(**vars(args))
	return api

def main(command_line_args: typing.Optional[typing.Sequence[str]]=None) -> None:
	parser = create_parser()
	args = parser.parse_args(command_line_args)
	if args.wait:
		time.sleep(args.wait)
	if args.dry_run:
		args.verbose = True
	func: typing.Callable[[model.Api, argparse.Namespace], None] = args.func
	if func is not config:
		parse_config()
	if args.version:
		print_version(args)
	api = get_api(args)
	try:
		func(api, args)
	except model.NotSupportedException as e:
		print(e, file=sys.stderr)
		sys.exit(1)


if __name__ == '__main__':
	main()
