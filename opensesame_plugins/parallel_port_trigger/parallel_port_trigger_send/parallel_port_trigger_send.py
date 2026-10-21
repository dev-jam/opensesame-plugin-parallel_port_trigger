"""
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

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

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
        # Read in the run phase: an earlier item may set these variables
        value = self.var.value
        if not isinstance(value, int) or not 0 <= value <= 255:
            raise OSException(f'Value should be an integer between 0 and 255, not: {value}')
        if self.duration_check:
            duration = self.var.duration
            if not isinstance(duration, int) or duration < 0:
                raise OSException(f'Duration should be a non-negative integer, not: {duration}')

        # No messages between setting and resetting the port: printing takes
        # time and would make the pulse longer
        self._write(value)
        self.set_item_onset()
        if self.duration_check:
            self.experiment.var.pptrigger_duration = duration
            if duration != 0:
                self.clock.sleep(duration)
            self._write(0)

        if self.dummy_mode:
            self._show_message(f'Dummy mode enabled, NOT sending value {value} to the parallel port on address: {self.port}')
        else:
            self._show_message(f'Sending value {value} to the parallel port on address: {self.port}')
        if self.duration_check:
            self._show_message(f'Waited {duration} ms to reset the parallel port to zero')

    def _write(self, value):
        if self.dummy_mode:
            return
        try:
            self.pptrigger.setData(value)
        except Exception as e:
            raise OSException(f'Could not access the parallel port\n\nMessage: {e}')

    def _init_var(self):
        self.dummy_mode = self.experiment.pptrigger_dummy_mode
        self.verbose = self.experiment.pptrigger_verbose
        self.port = self.experiment.pptrigger_port
        self.pptrigger = None if self.dummy_mode else self.experiment.pptrigger
        # Otherwise a value such as 'Yes' from a variable would leave the
        # trigger on the port instead of sending a pulse
        if self.var.duration_check not in ('yes', 'no'):
            raise OSException(f"Enable duration should be 'yes' or 'no', not: {self.var.duration_check}")
        self.duration_check = self.var.duration_check == 'yes'

    def _check_init(self):
        if not hasattr(self.experiment, 'pptrigger_dummy_mode'):
            raise OSException('You should have one instance of `parallel_port_trigger_init` at the start of your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose:
            print(message)


class QtParallelPortTriggerSend(ParallelPortTriggerSend, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        ParallelPortTriggerSend.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        self.checkbox_duration_check.toggled.connect(
            self.line_edit_duration.setEnabled)

    def edit_widget(self):
        widget = super().edit_widget()
        self.line_edit_duration.setEnabled(
            self.checkbox_duration_check.isChecked())
        return widget
