#-*- coding:utf-8 -*-

"""
21-01-2016
Author: Bob Rosbag
Version: 5.0

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

#import warnings
import os
import imp

from libopensesame.py3compat import *
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception

VERSION = u'5.0'

class parallel_port_trigger_init(item):

    """
    Parallel Port Trigger class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Parallel Port Trigger Plug-in'

    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.pptrigger_dummy = u'no'

        if os.name == 'nt':
            self.var.pptrigger_port = u'0x378'
        else:
            self.var.pptrigger_port = u'/dev/parport0'

        # Debugging output is only visible when OpenSesame is started with the
        # --debug argument.
        debug.msg(u'Parallel Port Trigger plug-in has been initialized!')

    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        self.pptrigger_port = self.var.pptrigger_port
        self.pptrigger_dummy = self.var.pptrigger_dummy
        
        self.experiment.pptrigger_dummy = self.var.pptrigger_dummy
        self.experiment.pptrigger_port = self.pptrigger_port
        
        if self.pptrigger_dummy == u'no':
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
                        print(path_to_dll_file)
                        self.experiment.pptrigger = windll.LoadLibrary(path_to_dll_file)
                    else:
                        #print(self.pptrigger_port.encode('ascii'))
                        if isinstance(self.pptrigger_port,str):
                            pptrigger_port = self.pptrigger_port.encode('ascii')
                        elif isinstance(self.pptrigger_port,int):
                            pptrigger_port = self.pptrigger_port
                        else:
                            raise osexception('Port value is not an integer or string')
                        self.experiment.pptrigger = parallel.Parallel(port=pptrigger_port)
                        #self.experiment.pptrigger = parallel.Parallel()
                    pass
                except Exception as e:
                    raise osexception(
                        u'Could not access the Parallel Port', exception=e)
                self.experiment.cleanup_functions.append(self.close)
                self.python_workspace[u'pptrigger'] = self.experiment.pptrigger
        elif self.pptrigger_dummy == u'yes':
            debug.msg(u'Dummy mode enabled, prepare phase')
        else:
            debug.msg(u'Error with dummy mode, mode is: %s' % self.pptrigger_dummy)

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().

    def close(self):

        """
        desc:
            Neatly close the connection to the parallel port.
        """

        if not hasattr(self.experiment, "pptrigger") or \
            self.experiment.pptrigger is None:
                debug.msg("no active Parallel port")
                return
        try:
            self.experiment.pptrigger.close()
            self.experiment.pptrigger = None
            debug.msg("Parallel Port closed")
        except:
            debug.msg("failed to close Parallel port")


class qtparallel_port_trigger_init(parallel_port_trigger_init, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Experiment Manager plug-in GUI"""

        parallel_port_trigger_init.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
        self.text_pptrigger_version.setText(
        u'<small>Parallel Port Trigger version %s</small>' % VERSION)
