#!/usr/bin/env python3

import os
import shutil
import tempfile

import pytest

from crandr import main
from test_without_config import *


class configfile:

	def __init__(self, fn_in):
		self.fn_in = os.path.abspath(fn_in)

	def __enter__(self) -> str:
		self.path = tempfile.mkdtemp()
		self.old_config_home = os.environ.get('XDG_CONFIG_HOME', None)
		os.environ['XDG_CONFIG_HOME'] = self.path
		
		self.fn_out = os.path.join(self.path, main.APP_NAME, 'config')
		os.mkdir(os.path.join(self.path, main.APP_NAME))
		os.symlink(self.fn_in, self.fn_out)
		return self.fn_out

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.old_config_home is None:
			del os.environ['XDG_CONFIG_HOME']
		else:
			os.environ['XDG_CONFIG_HOME'] = self.old_config_home
		
		shutil.rmtree(self.path)
		return False


class TestConfig:

	# ------- --list-searched-paths -------

	def test_config_list_searched_paths(self, capsys):
		args = ['--dry-run', 'config', '--list-searched-paths']
		main.main(args)
		out = capsys.readouterr().out.rstrip()
		searched_path = out.splitlines()
		assert len(searched_path) >= 1
		
		for fn in searched_path:
			assert os.path.isabs(fn)
			assert os.path.split(fn)[1] == 'config'

	# ------- --print-file-name -------

	def test_config_print_nothing(self, capsys):
		args = ['--dry-run', 'config', '--print-file-name']
		main.main(args)
		out = capsys.readouterr().out.rstrip()
		fn = out
		assert fn == ''

	def test_config_print_config_file(self, capsys):
		args = ['--dry-run', 'config', '--print-file-name']
		with configfile('_test-output/config/test') as fn:
			main.main(args)
			out = capsys.readouterr().out.rstrip()
			assert out == fn

	# ------- --edit -------

	def test_config_edit__no_editor__without_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', '')
		args = ['--dry-run', 'config', '--edit']
		main.main(args)
		out = capsys.readouterr().out.rstrip().splitlines()
		path = os.path.join(os.environ['XDG_CONFIG_HOME'], main.APP_NAME)
		fn = os.path.join(path, 'config')
		assert out == [
			f'os.makedirs({path!r}, exist_ok=True)',
			f'cp \'doc/example_config\' {fn!r}',
			'vi %s' % fn,
		]

	def test_config_edit__no_editor__with_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', '')
		args = ['--dry-run', 'config', '--edit']
		with configfile('_test-output/config/test') as fn:
			main.main(args)
			out = capsys.readouterr().out.rstrip()
			assert out == 'vi %s' % fn

	def test_config_edit__with_editor__without_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', 'vim')
		args = ['--dry-run', 'config', '--edit']
		main.main(args)
		out = capsys.readouterr().out.rstrip().splitlines()
		path = os.path.join(os.environ['XDG_CONFIG_HOME'], main.APP_NAME)
		fn = os.path.join(path, 'config')
		assert out == [
			f'os.makedirs({path!r}, exist_ok=True)',
			f'cp \'doc/example_config\' {fn!r}',
			'vim %s' % fn,
		]

	def test_config_edit__with_editor__with_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', 'nano')
		args = ['--dry-run', 'config', '--edit']
		with configfile('_test-output/config/test') as fn:
			main.main(args)
			out = capsys.readouterr().out.rstrip()
			assert out == 'nano %s' % fn

	# ------- no arguments -------

	def test_config_default__no_editor__without_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', '')
		args = ['--dry-run', 'config']
		main.main(args)
		out = capsys.readouterr().out.rstrip().splitlines()
		assert out[:3] == [
			'[not opening config file because EDITOR is not defined]',
			'no config file existing',
			'the following paths are searched:'
		]
		assert len(out) >= 4
		assert out[3].startswith('- ')
		assert out[3].endswith('config')

	def test_config_default__no_editor__with_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', '')
		args = ['--dry-run', 'config']
		with configfile('_test-output/config/test') as fn:
			main.main(args)
			out = capsys.readouterr().out.rstrip().splitlines()
			assert out == [
				'[not opening config file because EDITOR is not defined]',
				fn,
			]

	def test_config_default__with_editor__without_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', 'nano')
		args = ['--dry-run', 'config']
		main.main(args)
		out = capsys.readouterr().out.rstrip().splitlines()
		path = os.path.join(os.environ['XDG_CONFIG_HOME'], main.APP_NAME)
		fn = os.path.join(path, 'config')
		assert out == [
			f'os.makedirs({path!r}, exist_ok=True)',
			f'cp \'doc/example_config\' {fn!r}',
			'nano %s' % fn,
		]

	def test_config_default__with_editor__with_config(self, capsys, monkeypatch):
		monkeypatch.setitem(os.environ, 'EDITOR', 'vim')
		args = ['--dry-run', 'config']
		with configfile('_test-output/config/test') as fn:
			main.main(args)
			out = capsys.readouterr().out.rstrip()
			assert out == 'vim %s' % fn


class TestConfigParsing:

	def test_map_name_to_connection(self, capsys):
		args = ['--dry-run', '--backend', 'xrandr', '--test-input', '_test-output/xrandr/eDP-1_mirror_HDMI-1_original.txt', 'list', '--format', '{m.name}:{m.connection}']
		with configfile('_test-output/config/test') as fn:
			main.main(args)
			out = capsys.readouterr().out.rstrip().splitlines()
			assert out == [
				'eDP-1:internal',
				'HDMI-1:display-port',
			]
