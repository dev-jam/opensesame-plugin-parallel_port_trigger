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


class ParallelPortTriggerSend(Item):

    def reset(self):
        self.var.value = 0
        self.var.duration_check = 'no'
        self.var.duration = 0

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        self.value = self.var.value

        if self.dummy_mode == 'no':
            try:
                if os.name == 'nt':
                    self.set_item_onset(self.pptrigger.DlPortWritePortUchar(int(self.port, 0), self.value))
                else:
                    self.set_item_onset(self.pptrigger.setData(self.value))
                self._show_message('Sending value %s to the parallel port on address: %s' % (self.value, self.port))
            except Exception as e:
                raise OSException('Wrong port address, could not access the Parallel Port\n\nMessage: %s' % e)

            if self.duration_check == 'yes':
                self.experiment.var.pptrigger_duration = self.duration
                if self.duration != 0:
                    self.clock.sleep(self.duration)
                    self._show_message('Waiting %s ms to reset' % (self.duration))
                try:
                    if os.name == 'nt':
                        self.pptrigger.DlPortWritePortUchar(int(self.port, 0), 0)
                    else:
                        self.pptrigger.setData(0)
                    self._show_message('Resetting the parallel port to zero')
                except Exception as e:
                    raise OSException('Wrong port address, could not access the Parallel Port\n\nMessage: %s' % e)
        elif self.dummy_mode == 'yes':
            self._show_message('Dummy mode enabled, NOT sending value %s to the parallel port on address: %s' % (self.value,self.port))
        else:
            self._show_message('Error with dummy mode!')

    def _init_var(self):
        self.dummy_mode = self.experiment.pptrigger_dummy_mode
        self.verbose = self.experiment.pptrigger_verbose
        self.port = self.experiment.pptrigger_port
        self.duration_check = self.var.duration_check

        if self.dummy_mode == 'no':
            self.pptrigger = self.experiment.pptrigger
        if self.duration_check == 'yes':
            if isinstance(self.var.duration, int):
                self.duration = int(self.var.duration)
            else:
                raise OSException('Duration should be a integer')

    def _check_init(self):
        if not hasattr(self.experiment, 'pptrigger_dummy_mode'):
            raise OSException('You should have one instance of `parallel_port_trigger_init` at the start of your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            oslogger.warning(message)


class QtParallelPortTriggerSend(ParallelPortTriggerSend, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        ParallelPortTriggerSend.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        self.line_edit_duration.setEnabled(self.checkbox_duration_check.isChecked())
        self.checkbox_duration_check.stateChanged.connect(
            self.line_edit_duration.setEnabled)
