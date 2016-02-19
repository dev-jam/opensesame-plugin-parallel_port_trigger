#-*- coding:utf-8 -*-

"""
21-01-2016
Author: Bob Rosbag
Version: 1.0

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

if os.name == 'posix':
    # import the local modified version of pyparallel
    # that allows for non-exclusive connections to the parport
    path_to_file = os.path.join(os.path.dirname(__file__), 'parallelppdev.py')
    parallel = imp.load_source('parallel', path_to_file)
    try:
        import parallelppdev as parallel
    except ImportError:
        print(u'The local modified version of pyparallel could not be loaded. Check if the file is present and if the file permissions are correct.')
elif os.name == 'nt':
    try:
        from ctypes import windll
    except ImportError:
        print(u'The ctypes module can not be loaded. Check if ctypes is installed correctly.')
else:
    try:
        import parallel
    except ImportError:
        print('The pyparallel module could not be loaded, please make sure pyparallel is installed correctly.')


class parallel_port_trigger(item):

    """
    Parallel Port Trigger class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Parallel Port Trigger Plug-in'

    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.pp_value = 0
        self.var.pp_dummy = u'no'

        if os.name == 'nt':
            self.var.pp_port = u'0x378'
        else:
            self.var.pp_port = u'/dev/parport0'

        # Debugging output is only visible when OpenSesame is started with the
        # --debug argument.
        debug.msg(u'Parallel Port Trigger plug-in has been initialized!')

    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        if self.pp_dummy == u'no':
            if not hasattr(self.experiment, "pp"):
                try:
                    if os.name == 'nt':
                        self.experiment.pp = windll.dlportio
                    else:
                        self.experiment.pp = parallel.Parallel()

                    self.experiment.cleanup_functions.append(self.close)
                    self.python_workspace[u'pp'] = self.experiment.pp
                except:
                    raise osexception(
                        _(u'Could not access the Parallel Port'))
        elif self.var.pp_dummy == u'yes':
            debug.msg(u'Dummy mode enabled, prepare phase')
        else:
            debug.msg(u'Error with dummy mode, mode is: %s' % self.var.pp_dummy)

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().

        # Set the pp value

        if self.var.pp_dummy == u'no':
            ## turn trigger on
            if os.name == 'nt':
                self.set_item_onset(self.experiment.pp.DlPortWritePortUchar(int(self.var.pp_port,0), self.var.pp_value))
            else:
                self.set_item_onset(self.experiment.pp.setData(self.pp_value))
            debug.msg(u'Sending value %s to the parallel port on address: %s' % (self.var.pp_value,self.var.pp_port))
        elif self.var.pp_dummy == u'yes':
            debug.msg(u'Dummy mode enabled, NOT sending value %s to the parallel port on address: %s' % (self.var.pp_value,self.var.pp_port))
        else:
            debug.msg(u'Error with dummy mode!')

    def close(self):

        """
        desc:
            Neatly close the connection to the buttonbox.
        """

        if not hasattr(self.experiment, "bb") or \
            self.experiment.bb is None:
                debug.msg("no active Buttonbox")
                return
        try:
            self.experiment.bb.close()
            self.experiment.bb = None
            debug.msg("buttonbox closed")
        except:
            debug.msg("failed to close buttonbox")


class qtparallel_port_trigger(parallel_port_trigger, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Experiment Manager plug-in GUI"""

        parallel_port_trigger.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
