#-*- coding:utf-8 -*-

"""
31-01-2017
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
from openexp.keyboard import keyboard

VERSION = u'4.0'

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
        self.var.pptrigger_value = 0
        self.var.pptrigger_duration_check = u'no'
        self.var.pptrigger_duration = 0


    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

		# create keyboard object
        self.kb = keyboard(self.experiment,timeout=1)

        if hasattr(self.experiment, "pptrigger_dummy"):
            self.pptrigger_dummy = self.experiment.pptrigger_dummy
        else:
            raise osexception(
                    u'Parallel Port init is missing')

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().

        # Set the pptrigger value dynamically in run phase
        self.pptrigger_value = self.var.pptrigger_value
        self.pptrigger_duration_check = self.var.pptrigger_duration_check
        self.pptrigger_duration = self.var.pptrigger_duration        
        
        
        if self.pptrigger_dummy == u'no':
            ## turn trigger on
            try:
                if os.name == 'nt':
                    self.set_item_onset(self.experiment.pptrigger.DlPortWritePortUchar(int(self.pptrigger_port,0), self.pptrigger_value))
                else:
                    self.set_item_onset(self.experiment.pptrigger.setData(self.pptrigger_value))
                debug.msg(u'Sending value %s to the parallel port on address: %s' % (self.pptrigger_value,self.experiment.pptrigger_port))

            except Exception as e:
                raise osexception(
                    u'Wrong port address, could not access the Parallel Port', exception=e)
            
            ## Executing duration and reset
            if self.pptrigger_duration_check == u'yes':
                # use keyboard as timeout, allowing for Escape presses to abort experiment

                if self.pptrigger_duration !=0:

                    self.kb.get_key(timeout=self.pptrigger_duration)
                    debug.msg(u'Waiting %s ms to reset' % (self.pptrigger_duration))
                
                try: 
                    if os.name == 'nt':
                        self.set_item_onset(self.experiment.pptrigger.DlPortWritePortUchar(int(self.pptrigger_port,0), 0))
                    else:
                        self.set_item_onset(self.experiment.pptrigger.setData(0))
                    debug.msg(u'Resetting the parallel port to zero')

                except Exception as e:
                    raise osexception(
                        u'Wrong port address, could not access the Parallel Port', exception=e)
                    
                    
        elif self.pptrigger_dummy == u'yes':
            debug.msg(u'Dummy mode enabled, NOT sending value %s to the parallel port on address: %s' % (self.pptrigger_value,self.experiment.pptrigger_port))
        else:
            debug.msg(u'Error with dummy mode!')


class qtparallel_port_trigger(parallel_port_trigger, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Experiment Manager plug-in GUI"""

        parallel_port_trigger.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
        self.text_pptrigger_version.setText(
        u'<small>Parallel Port Trigger version %s</small>' % VERSION)

    def apply_edit_changes(self):

        """
        desc:
            Applies the controls.
        """

        if not qtautoplugin.apply_edit_changes(self) or self.lock:
            return False
        self.custom_interactions()

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
        if self.pptrigger_duration_check == u'yes':
            self.spinbox_pptrigger_duration.setEnabled(True)
        elif self.pptrigger_duration_check == u'no':
            self.spinbox_pptrigger_duration.setDisabled(True)

