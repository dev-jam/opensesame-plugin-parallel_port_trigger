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

#import warnings
import os
import imp

from libopensesame.py3compat import *
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception

VERSION = u'2020.1-1'

class parallel_port_trigger_init(item):

    """
    Parallel Port Trigger class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Parallel Port Trigger: initializes the parallel port device.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'


    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.dummy_mode = u'no'
        self.var.verbose = u'no'

        if os.name == 'nt':
            self.var.port = u'0x378'
        else:
            self.var.port = u'/dev/parport0'


        # Debugging output is only visible when OpenSesame is started with the
        # --debug argument.
        self.show_message(u'Parallel Port Trigger plug-in has been initialized!')


    def init_var(self):

        """Set en check variables."""

        self.dummy_mode = self.var.dummy_mode
        self.verbose = self.var.verbose
        self.experiment.pptrigger_verbose = self.var.verbose

        self.experiment.pptrigger_dummy_mode = self.var.dummy_mode
        self.experiment.pptrigger_port = self.var.port

        self.experiment.var.pptrigger_port = self.var.port


    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        self.close()
        self.init_var()


        if self.dummy_mode == u'no':
            if os.name == 'posix':
                # import the local modified version of pyparallel
                # that allows for non-exclusive connections to the parport
                path_to_file = os.path.join(os.path.dirname(__file__), 'parallelppdev.py')
                parallel = imp.load_source('parallel', path_to_file)
                try:
                    import parallelppdev as parallel
                except ImportError as e:
                    raise osexception(u'The local modified version of pyparallel could not be loaded. Check if the file is present and if the file permissions are correct.', exception=e)
            elif os.name == 'nt':
                try:
                    from ctypes import windll
                except ImportError as e:
                    raise osexception(u'The ctypes module can not be loaded. Check if ctypes is installed correctly.', exception=e)
            else:
                try:
                    import parallel
                except ImportError as e:
                    raise osexception('The pyparallel module could not be loaded, please make sure pyparallel is installed correctly.', exception=e)

            if not hasattr(self.experiment, "pptrigger"):
                try:
                    if os.name == 'nt':
                        path_to_dll_file = os.path.join(os.path.dirname(__file__), 'inpout32.dll')
                        self.show_message(path_to_dll_file)
                        self.experiment.pptrigger = windll.LoadLibrary(path_to_dll_file)

                        if isinstance(self.var.port,str):
                            #port = self.port.encode('ascii')
                            self.port = self.var.port.encode('ascii')
                        else:
                            raise osexception('Port value should be a string on Windows')


                    else:
                        self.show_message(u'Using parallel port on address: %s' % self.var.port)
                        if isinstance(self.var.port,int):
                            self.port = self.var.port
                        elif isinstance(self.var.port,str):
                            #port = self.port.encode('ascii')
                            self.port = self.var.port.encode('ascii')

                        else:
                            raise osexception('Port value should be a integer or string on Linux')
                        self.experiment.pptrigger = parallel.Parallel(port=self.port)

                except Exception as e:
                    raise osexception(
                        u'Could not access the Parallel Port', exception=e)
                self.experiment.cleanup_functions.append(self.close)
                self.python_workspace[u'pp'] = self.experiment.pptrigger

            ## reset trigger
            try:
                if os.name == 'nt':
                    self.set_item_onset(self.experiment.pptrigger.DlPortWritePortUchar(int(self.port,0), 0))
                else:
                    self.set_item_onset(self.experiment.pptrigger.setData(0))
                self.show_message(u'Resetting the parallel port on address: %s' % (self.port))

            except Exception as e:
                raise osexception(
                    u'Wrong port address, could not access the Parallel Port', exception=e)
        elif self.dummy_mode == u'yes':
            self.show_message(u'Dummy mode enabled for the Parallel Port Trigger Plug-in')
        else:
            self.show_message(u'Error with dummy mode, mode is: %s' % self.dummy_mode)

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().

        pass


    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose:
            print(message)


    def close(self):

        """
        desc:
            Neatly close the connection to the parallel port.
        """

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

        """Experiment Manager plug-in GUI"""

        parallel_port_trigger_init.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

