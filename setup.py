#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
21-01-2016
Author: Bob Rosbag
Version: 3.0

This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup
import yaml

# Extract the plugin version from info.yaml
with open('parallel_port_trigger/info.yaml') as fd:
	d = yaml.load(fd)
version = d['version']

setup(
	name='opensesame-plugin-parallel_port_trigger',
	version=version,
	description='Paralle-port trigger plugin for OpenSesame',
	author='Bob Rosbag',
	url='https://github.com/dev-jam/opensesame_plugin_-_parallel_port_trigger',
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	data_files=[
		('share/opensesame_plugins/parallel_port_trigger',
		[
			'parallel_port_trigger/parallel_port_trigger.md',
			'parallel_port_trigger/parallel_port_trigger.png',
			'parallel_port_trigger/parallel_port_trigger_large.png',
			'parallel_port_trigger/parallel_port_trigger.py',
			'parallel_port_trigger/info.yaml',
			]
		),
		('share/opensesame_plugins/parallel_port_trigger_init',
		[
			'parallel_port_trigger_init/parallel_port_trigger_init.md',
			'parallel_port_trigger_init/parallel_port_trigger_init.png',
			'parallel_port_trigger_init/parallel_port_trigger_init_large.png',
			'parallel_port_trigger_init/parallel_port_trigger_init.py',
			'parallel_port_trigger_init/info.yaml',
			]
		)],
	)
