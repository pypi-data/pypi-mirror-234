#!/usr/bin/env python3

import os
import typing

class ConfigPathFinder:

	def __init__(self, app_name: str, *, file_name: str = 'config'):
		self.app_name = app_name
		self.file_name = file_name
		self._appdirs: typing.Any = None

	def get_app_dirs(self) -> typing.Any:
		if self._appdirs:
			return self._appdirs
		
		try:
			from platformdirs import PlatformDirs as AppDirs
		except:
			try:
				from xdgappdirs import AppDirs
			except:
				try:
					from appdirs import AppDirs
				except:
					return None
		self._appdirs = AppDirs(self.app_name, multipath=True)
		return self._appdirs

	def iter_config_directories(self) -> typing.Iterator[str]:
		app_dirs = self.get_app_dirs()
		if app_dirs:
			yield from app_dirs.user_config_dir.split(os.pathsep)
			yield from app_dirs.site_config_dir.split(os.pathsep)
		else:
			path = os.environ.get('XDG_CONFIG_HOME', None)
			if not path:
				path = os.path.expanduser('~')
				path = os.path.join(path, '.config')
			path = os.path.join(path, self.app_name)
			yield path

	def iter_possible_config_files(self) -> typing.Iterator[str]:
		for path in self.iter_config_directories():
			yield os.path.join(path, self.file_name)

	def get_existing_config_file(self) -> typing.Optional[str]:
		for ffn in self.iter_possible_config_files():
			if os.path.isfile(ffn):
				return ffn
		
		return None
