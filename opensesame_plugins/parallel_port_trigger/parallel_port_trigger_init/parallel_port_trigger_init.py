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

import os
import platform
from libopensesame.item import Item
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger

DLL_FILES = {'32bit': 'inpout32.dll', '64bit': 'inpoutx64.dll'}


class InpOutPort:
    """Wraps the InpOut32 DLL (Windows) in the interface of pyparallel's
    Parallel class (Linux), so both have setData(). Other attributes are
    passed on to the DLL, e.g. DlPortWritePortUchar() in inline scripts."""

    def __init__(self, dll, address):
        self.dll = dll
        self.address = address

    def setData(self, value):
        self.dll.DlPortWritePortUchar(self.address, value)

    def __getattr__(self, name):
        return getattr(self.dll, name)


class ParallelPortTriggerInit(Item):

    def reset(self):
        self.var.dummy_mode = 'no'
        self.var.verbose = 'no'
        self.var.port = '0x378' if os.name == 'nt' else 0

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

        if self.dummy_mode:
            self._show_message('Dummy mode enabled for the Parallel Port Trigger Plug-in')
            return

        if os.name == 'nt':
            self.experiment.pptrigger = self._open_windows()
        else:
            self.experiment.pptrigger = self._open_linux()
        self.experiment.cleanup_functions.append(self.close)

        try:
            self.experiment.pptrigger.setData(0)
        except Exception as e:
            raise OSException(f'Could not access the parallel port\n\nMessage: {e}')
        self.set_item_onset()
        self._show_message('Resetting the parallel port to all zero')

    def close(self):
        if getattr(self.experiment, 'pptrigger', None) is None:
            return
        # Don't leave trigger lines high, e.g. a value sent without duration
        # when the experiment ends or is aborted.
        # Only a warning: cleanup also runs after an error, and an exception
        # here would hide that error.
        try:
            self.experiment.pptrigger.setData(0)
            self._show_message('Resetting the parallel port to all zero')
        except Exception as e:
            oslogger.warning(f'Could not reset the parallel port to zero: {e}')
        self.experiment.pptrigger = None
        self._show_message('Parallel Port closed')

    def _init_var(self):
        if self.var.dummy_mode not in ('yes', 'no'):
            raise OSException(f"Dummy mode should be 'yes' or 'no', not: {self.var.dummy_mode}")
        self.dummy_mode = self.var.dummy_mode == 'yes'
        self.verbose = self.var.verbose == 'yes'
        self.port = self.var.port
        self.experiment.pptrigger_dummy_mode = self.dummy_mode
        self.experiment.pptrigger_verbose = self.verbose
        self.experiment.pptrigger_port = self.port

    def _open_windows(self):
        from ctypes import windll

        # Only a string, such as 0x378: OpenSesame stores an address without
        # 0x, such as 0378 (how Device Manager shows 0x378), as the number
        # 378, which can't be told apart from a decimal address
        try:
            address = int(self.port, 0) if isinstance(self.port, str) else None
        except ValueError:
            address = None
        if address is None:
            raise OSException(f'Port address should be a hexadecimal number starting with 0x, like 0x378, on Windows, not: {self.port}\n\nDevice Manager shows addresses without 0x: write 0378 as 0x378.')
        # Lower I/O addresses are not parallel ports, e.g. 0x0. I/O addresses
        # are 16-bit: a higher address doesn't fit the DLL's port argument
        if not 0x100 <= address <= 0xFFFF:
            raise OSException(f'Port address should be a parallel port address between 0x100 and 0xFFFF on Windows, like 0x378, not: {self.port}')

        architecture = platform.architecture()[0]
        if architecture not in DLL_FILES:
            raise OSException(f'Platform not supported: {architecture}')
        path_to_dll_file = os.path.join(os.path.dirname(__file__), DLL_FILES[architecture])
        self._show_message(f'Loading {path_to_dll_file}')
        try:
            dll = windll.LoadLibrary(path_to_dll_file)
        except Exception as e:
            raise OSException(f'Could not load parallel port library {path_to_dll_file}\n\nMessage: {e}')
        # Without the driver, writing to the port silently does nothing
        if not dll.IsInpOutDriverOpen():
            raise OSException('The InpOut32 driver could not be opened. It is installed the first time it is used, which needs administrator privileges: run OpenSesame once as administrator.')

        self._show_message(f'Using parallel port on address: {address:#x}')
        return InpOutPort(dll, address)

    def _open_linux(self):
        if not isinstance(self.port, int) or self.port < 0:
            raise OSException(f'Port should be a number X pointing to /dev/parportX on Linux, not: {self.port}')
        try:
            import parallel
        except ImportError as e:
            raise OSException(f'The pyparallel module could not be loaded, please make sure pyparallel is installed correctly.\n\nMessage: {e}')

        device = f'/dev/parport{self.port}'
        self._show_message(f'Using parallel port on address: {device}')
        try:
            port = parallel.Parallel(port=self.port)
        except Exception as e:
            raise OSException(f'Could not access the parallel port {device}\n\nMessage: {e}')
        self._show_message('Parallel Port Trigger plug-in has been initialized!')
        return port

    def _check_init(self):
        if hasattr(self.experiment, 'pptrigger_dummy_mode'):
            raise OSException('You should have only one instance of `parallel_port_trigger_init` in your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose:
            print(message)
