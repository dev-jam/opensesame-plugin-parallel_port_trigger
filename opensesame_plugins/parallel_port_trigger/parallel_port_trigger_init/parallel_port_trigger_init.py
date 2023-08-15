#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2022

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

import os
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger


class ParallelPortTriggerInit(Item):

    def reset(self):
        self.var.dummy_mode = 'no'
        self.var.verbose = 'no'
        if os.name == 'nt':
            self.var.port = '0x378'
        else:
            self.var.port = 0

    def prepare(self):
        super().prepare()
        self.verbose = 'yes'
        self.close()
        self._init_var()
        self._check_init()

        if self.dummy_mode == 'no':
            if os.name == 'nt':
                try:
                    from ctypes import windll
                except ImportError as e:
                    raise OSException('The ctypes module can not be loaded. Check if ctypes is installed correctly.\n\nMessage: %s' % e)
                import platform
                if platform.architecture()[0] == "32bit":
                    self.dll_file = 'inpout32.dll'
                elif platform.architecture()[0] == "64bit":
                    self.dll_file = 'inpoutx64.dll'
                else:
                    raise OSException('Platform not supported')

                path_to_dll_file = os.path.join(os.path.dirname(__file__), self.dll_file)
                self._show_message(path_to_dll_file)

                try:
                    self.experiment.pptrigger = windll.LoadLibrary(path_to_dll_file)
                except Exception as e:
                    raise OSException('Could not load parallel port library\n\nMessage: %s' % e)

                if isinstance(self.var.port,str):
                    self.port = self.var.port
                else:
                    raise OSException('Port value should be a string on Windows')
            else:
                try:
                    import parallel
                except ImportError as e:
                    raise OSException('The pyparallel module could not be loaded, please make sure pyparallel is installed correctly.\n\nMessage: %s' % e)

                if isinstance(self.var.port,int):
                    self._show_message('Using parallel port on address: /dev/parport%d' % self.var.port)
                    self.port = self.var.port
                else:
                    raise OSException('Port value should be a integer on Linux')

                try:
                    self.experiment.pptrigger = parallel.Parallel(port=self.port)
                    self._show_message('Parallel Port Trigger plug-in has been initialized!')
                except Exception as e:
                    raise OSException('Could not access the parallel port\n\nMessage: %s' % e)

            self.experiment.cleanup_functions.append(self.close)

            # reset trigger
            try:
                if os.name == 'nt':
                    self.set_item_onset(self.experiment.pptrigger.DlPortWritePortUchar(int(self.port, 0), 0))
                else:
                    self.set_item_onset(self.experiment.pptrigger.setData(0))
                self._show_message('Resetting the parallel port to all zero')
            except Exception as e:
                raise OSException('Could not access the Parallel Port\n\nMessage: %s' % e)
        elif self.dummy_mode == 'yes':
            self._show_message('Dummy mode enabled for the Parallel Port Trigger Plug-in')
        else:
            self._show_message('Error with dummy mode, mode is: %s' % self.dummy_mode)

    def close(self):
        if not hasattr(self.experiment, "pptrigger") or \
                self.experiment.pptrigger is None:
            return
        try:
            self.experiment.pptrigger = None
            self._show_message("Parallel Port closed")
        except Exception:
            raise OSException("Failed to close Parallel port")

    def _init_var(self):
        self.dummy_mode = self.var.dummy_mode
        self.verbose = self.var.verbose
        self.experiment.pptrigger_verbose = self.var.verbose
        self.experiment.pptrigger_dummy_mode = self.var.dummy_mode
        self.experiment.pptrigger_port = self.var.port

    def _check_init(self):
        if hasattr(self.experiment, 'pptrigger'):
            raise OSException('You should have only one instance of `parallel_port_trigger_init` in your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            oslogger.warning(message)


class qtParallelPortTriggerInit(ParallelPortTriggerInit, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        ParallelPortTriggerInit.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
