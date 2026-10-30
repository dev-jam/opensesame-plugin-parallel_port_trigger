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

# Names of the pulse mode settings up to 5.0.2
OLD_NAMES = {'duration_check': 'pulse_mode', 'duration': 'pulse_time'}


class ParallelPortTriggerSend(Item):

    def reset(self):
        self.var.value = 0
        self.var.pulse_mode = 'no'
        self.var.pulse_time = 0

    def from_string(self, string):
        super().from_string(string)
        self._convert_old_names(
            'the experiment', 'Save the experiment to store the new names.')

    def prepare(self):
        super().prepare()
        self._convert_old_names(
            'an inline script', 'Use the new names in the inline script.')
        self._check_init()
        self._init_var()

    def run(self):
        self._convert_old_names(
            'an inline script', 'Use the new names in the inline script.')
        # Read in the run phase: an earlier item may set these variables
        value = self.var.value
        if not isinstance(value, int) or not 0 <= value <= 255:
            raise OSException(f'Value should be an integer between 0 and 255, not: {value}')
        if self.pulse_mode:
            pulse_time = self.var.pulse_time
            if not isinstance(pulse_time, int) or pulse_time < 0:
                raise OSException(f'Pulse time should be a non-negative integer, not: {pulse_time}')

        # No messages between setting and resetting the port: printing takes
        # time and would make the pulse longer
        self._write(value)
        self.set_item_onset()
        if self.pulse_mode:
            self.experiment.var.pptrigger_pulse_time = pulse_time
            # The name up to 5.0.2, for existing analysis scripts
            self.experiment.var.pptrigger_duration = pulse_time
            if pulse_time != 0:
                self.clock.sleep(pulse_time)
            self._write(0)

        if self.dummy_mode:
            self._show_message(f'Dummy mode enabled, NOT sending value {value} to the parallel port on address: {self.port}')
        else:
            self._show_message(f'Sending value {value} to the parallel port on address: {self.port}')
        if self.pulse_mode:
            self._show_message(f'Waited {pulse_time} ms to reset the parallel port to zero')

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
        pulse_mode = self.var.pulse_mode
        if pulse_mode not in ('yes', 'no'):
            raise OSException(f"Enable pulse mode should be 'yes' or 'no', not: {pulse_mode}")
        self.pulse_mode = pulse_mode == 'yes'

    def _convert_old_names(self, source, fix):
        # Experiments and inline scripts made up to 5.0.2 use the old names;
        # without this an old pulse mode setting would be ignored silently
        # and the value would stay on the port. The old name wins: the new
        # one may only have its default from reset().
        found = [old for old in OLD_NAMES if old in self.var.vars()]
        if not found:
            return
        for old in found:
            self.var.set(OLD_NAMES[old], self.var.get(old, _eval=False))
            self.var.unset(old)
        # Once per item and source: prepare() and run() repeat in a loop
        warned = self.__dict__.setdefault('_old_names_warned', set())
        if source in warned:
            return
        warned.add(source)
        names = ', '.join(f'{old} is now {OLD_NAMES[old]}' for old in found)
        oslogger.warning(
            f'Item {self.name}: {source} uses the old names of the pulse '
            f'settings ({names}); they were converted. {fix} Versions of '
            f'the Parallel Port Trigger plug-in up to 5.0.2 ignore the new '
            f'names and send no pulse: the value stays on the port.')

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
        self.checkbox_pulse_mode.toggled.connect(
            self.line_edit_pulse_time.setEnabled)

    def edit_widget(self):
        widget = super().edit_widget()
        self.line_edit_pulse_time.setEnabled(
            self.checkbox_pulse_mode.isChecked())
        return widget
