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

#import warnings
import os

from libopensesame.py3compat import *
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception

VERSION = u'3.1.0'


class parallel_port_trigger_init(item):

    description = u'Parallel Port Trigger: initializes the parallel port device.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'

    def reset(self):

        self.var.dummy_mode = u'no'
        self.var.verbose = u'no'

        if os.name == 'nt':
            self.var.port = u'0x378'
        else:
            self.var.port = 0

        self.show_message(u'Parallel Port Trigger plug-in has been initialized!')

    def init_var(self):

        self.dummy_mode = self.var.dummy_mode
        self.verbose = self.var.verbose
        self.experiment.pptrigger_verbose = self.var.verbose

        self.experiment.pptrigger_dummy_mode = self.var.dummy_mode
        self.experiment.pptrigger_port = self.var.port

    def prepare(self):

        item.prepare(self)

        self.close()
        self.init_var()

        if self.dummy_mode == u'no':
            if os.name == 'nt':
                try:
                    from ctypes import windll
                except ImportError as e:
                    raise osexception(u'The ctypes module can not be loaded. Check if ctypes is installed correctly.', exception=e)

                import platform

                if platform.architecture()[0] == "32bit":
                    self.dll_file = 'inpout32.dll'
                elif platform.architecture()[0] == "64bit":
                    self.dll_file = 'inpoutx64.dll'
                else:
                    raise osexception('Platform not supported')

                path_to_dll_file = os.path.join(os.path.dirname(__file__), self.dll_file)
                self.show_message(path_to_dll_file)

                try:
                    self.experiment.pptrigger = windll.LoadLibrary(path_to_dll_file)

                except Exception as e:
                    raise osexception(
                        u'Could not load parallel port library ', exception=e)

                if isinstance(self.var.port,str):
                    self.port = self.var.port
                else:
                    raise osexception('Port value should be a string on Windows')

            else:
                try:
                    import parallel
                except ImportError as e:
                    raise osexception('The pyparallel module could not be loaded, please make sure pyparallel is installed correctly.', exception=e)

                if isinstance(self.var.port,int):
                    self.show_message(u'Using parallel port on address: /dev/parport%d' % self.var.port)
                    self.port = self.var.port
                else:
                    raise osexception('Port value should be a integer on Linux')

                try:
                    self.experiment.pptrigger = parallel.Parallel(port=self.port)
                except Exception as e:
                    raise osexception(
                        u'Could not access the parallel port', exception=e)

            self.experiment.cleanup_functions.append(self.close)

            ## reset trigger
            try:
                if os.name == 'nt':
                    self.set_item_onset(self.experiment.pptrigger.DlPortWritePortUchar(int(self.port,0), 0))
                else:
                    self.set_item_onset(self.experiment.pptrigger.setData(0))
                self.show_message(u'Resetting the parallel port to all zero')
            except Exception as e:
                raise osexception(
                    u'Could not access the Parallel Port', exception=e)
        elif self.dummy_mode == u'yes':
            self.show_message(u'Dummy mode enabled for the Parallel Port Trigger Plug-in')
        else:
            self.show_message(u'Error with dummy mode, mode is: %s' % self.dummy_mode)

    def run(self):

        pass

    def show_message(self, message):

        debug.msg(message)
        if self.verbose:
            print(message)

    def close(self):

        if not hasattr(self.experiment, "pptrigger") or \
            self.experiment.pptrigger is None:
                return
        try:
            self.experiment.pptrigger = None
            self.show_message("Parallel Port closed")
        except:
            self.show_message("failed to close Parallel port")


class qtparallel_port_trigger_init(parallel_port_trigger_init, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        parallel_port_trigger_init.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

