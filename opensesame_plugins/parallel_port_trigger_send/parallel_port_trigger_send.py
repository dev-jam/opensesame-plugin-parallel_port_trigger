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

from libopensesame.py3compat import *
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception
from openexp.keyboard import keyboard

VERSION = u'2020.1-1'

class parallel_port_trigger_send(item):

    """
    Parallel Port Trigger class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Parallel Port Trigger: send trigger.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'


    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.value = 0
        self.var.duration_check = u'no'
        self.var.duration = 0


    def init_var(self):

        """Set en check variables."""

        if hasattr(self.experiment, "pptrigger_dummy_mode"):
            self.dummy_mode = self.experiment.pptrigger_dummy_mode
            self.verbose = self.experiment.pptrigger_verbose
        else:
            raise osexception(
                    u'Parallel Port init is missing')

        self.port = self.experiment.pptrigger_port

        if self.dummy_mode == u'no':
            self.pptrigger = self.experiment.pptrigger


    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        # create keyboard object
        self.kb = keyboard(self.experiment,timeout=1)

        self.init_var()


    def run(self):

        """Run phase"""

        # Set the pptrigger value dynamically in run phase
        self.value = self.var.value
        self.duration_check  = self.var.duration_check

        if self.duration_check == u'yes' :
            if isinstance(self.var.duration,int):
                self.duration = int(self.var.duration)
            else:
                raise osexception(u'Duration should be a integer')

        self.experiment.var.pptrigger_value = self.var.value

        if self.dummy_mode == u'no':
            ## turn trigger on
            try:
                if os.name == 'nt':
                    self.set_item_onset(self.pptrigger.DlPortWritePortUchar(int(self.port,0), self.value))
                else:
                    self.set_item_onset(self.pptrigger.setData(self.value))
                self.show_message(u'Sending value %s to the parallel port on address: %s' % (self.value,self.port))

            except Exception as e:
                raise osexception(
                    u'Wrong port address, could not access the Parallel Port', exception=e)

            ## Executing duration and reset
            if self.duration_check == u'yes':
                # use keyboard as timeout, allowing for Escape presses to abort experiment
                self.experiment.var.pptrigger_duration = self.duration

                if self.duration !=0:

                    self.kb.get_key(timeout=self.duration)
                    self.show_message(u'Waiting %s ms to reset' % (self.duration))

                try:
                    if os.name == 'nt':
                        self.pptrigger.DlPortWritePortUchar(int(self.port,0), 0)
                    else:
                        self.pptrigger.setData(0)
                    self.show_message(u'Resetting the parallel port to zero')

                except Exception as e:
                    raise osexception(
                        u'Wrong port address, could not access the Parallel Port', exception=e)


        elif self.dummy_mode == u'yes':
            self.show_message(u'Dummy mode enabled, NOT sending value %s to the parallel port on address: %s' % (self.value,self.port))
        else:
            self.show_message(u'Error with dummy mode!')


    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


class qtparallel_port_trigger_send(parallel_port_trigger_send, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Experiment Manager plug-in GUI"""

        parallel_port_trigger_send.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

    def apply_edit_changes(self):

        """
        desc:
            Applies the controls.
        """

        if not qtautoplugin.apply_edit_changes(self) or self.lock:
            return False
        self.custom_interactions()
        return True

    def edit_widget(self):

        """
        Refreshes the controls.

        Returns:
        The QWidget containing the controls
        """

        if self.lock:
            return
        self.lock = True
        w = qtautoplugin.edit_widget(self)
        self.custom_interactions()
        self.lock = False
        return w

    def custom_interactions(self):

        """
        desc:
            Activates the relevant controls for each tracker.
        """
        if self.var.duration_check == u'yes':
            self.line_edit_duration.setEnabled(True)
        elif self.var.duration_check == u'no':
            self.line_edit_duration.setDisabled(True)

