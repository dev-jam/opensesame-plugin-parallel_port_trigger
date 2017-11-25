#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2017

This plug-in is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this plug-in.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup

setup(
    # Some general metadata. By convention, a plugin is named:
    # opensesame-plugin-[plugin name]
    name='opensesame_plugin_-_parallel_port_trigger',
    version='1.0.0',
    description='An OpenSesame Plug-in for sending stimulus synchronization triggers through the parallel port to data acquisition systems.',
    author='Bob Rosbag',
    author_email='b.rosbag@let.ru.nl',
    url='https://github.com/dev-jam/opensesame_plugin_-_parallel_port_trigger',
    # Classifiers used by PyPi if you upload the plugin there
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    # The important bit that specifies how the plugin files should be installed,
    # so that they are found by OpenSesame. This is a bit different from normal
    # Python modules, because an OpenSesame plugin is not a (normal) Python
    # module.
    data_files=[
        # First the target folder.
        ('share/opensesame_plugins/parallel_port_trigger_init',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/parallel_port_trigger_init/parallel_port_trigger_init.md',
            'opensesame_plugins/parallel_port_trigger_init/parallel_port_trigger_init.png',
            'opensesame_plugins/parallel_port_trigger_init/parallel_port_trigger_init_large.png',
            'opensesame_plugins/parallel_port_trigger_init/parallel_port_trigger_init.py',
            'opensesame_plugins/parallel_port_trigger_init/info.yaml',
            'opensesame_plugins/parallel_port_trigger_init/parallelppdev.py',
            'opensesame_plugins/parallel_port_trigger_init/inpout32.dll',
            ]
        ),
        ('share/opensesame_plugins/parallel_port_trigger_send',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/parallel_port_trigger_send/parallel_port_trigger_send.md',
            'opensesame_plugins/parallel_port_trigger_send/parallel_port_trigger_send.png',
            'opensesame_plugins/parallel_port_trigger_send/parallel_port_trigger_send_large.png',
            'opensesame_plugins/parallel_port_trigger_send/parallel_port_trigger_send.py',
            'opensesame_plugins/parallel_port_trigger_send/info.yaml',
            ]
        )]
    )
