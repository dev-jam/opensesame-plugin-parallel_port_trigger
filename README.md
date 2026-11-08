OpenSesame Plugin: Parallel Port Trigger
==========

*An OpenSesame plugin for sending stimulus synchronization triggers through the parallel port to data acquisition systems.*  

Copyright (C) 2013-2026 Bob Rosbag, Per Sederberg, Edwin Dalmaijer and contributors  

Contributions: Code is based on the work of Per Sederberg. Debugged and polished by Edwin Dalmaijer.


## About

In EEG/ERP studies it is common to send triggers to mark the timestamp for significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to data acquisition systems.

The plugin has two items: an *Init* item, which should be placed at the beginning of an experiment, and a *Send* item, which sends a trigger.

Init item:

- *Dummy mode* for testing experiments without a parallel port.
- *Verbose mode* prints messages about what the items do.
- *Port Address* for Windows: hexadecimal, starting with 0x (0x378; Device Manager shows it as 0378), for Linux: port number (0 in /dev/parport0).

Send item:

- *Value* is an integer between 0 and 255 and specifies the trigger byte. It may be a variable, such as `{trigger}`.
- *Enable pulse mode*: the port is set back to 0 after the pulse time (a pulse).
- *Pulse time (ms)* is the time in ms before the port is set back to 0. It may be a variable.

In the script these settings are `pulse_mode` and `pulse_time`. Up to version 5.0.2 they were called `duration_check` and `duration`: an experiment or inline script with the old names still works, the send item converts them and gives a warning. Save the experiment to store the new names, and use the new names in inline scripts (`items['name'].var.pulse_time`). Note that versions up to 5.0.2 don't know the new names: they ignore them and send no pulse, the value stays on the port. Use the same version of the plugin on every computer that runs the experiment.

With pulse mode, the send item logs the pulse time as `pptrigger_pulse_time`, and also as `pptrigger_duration`, its name up to 5.0.2.

There are two ways to send a trigger:

- *Pulse mode*: one item sends a pulse, e.g. value 23 for 10 ms, and then sets the port back to 0.
- *Without pulse mode*: the value stays on the port until another item changes it. For example, one item sends 23 and a later item sends 0; the trigger then lasts as long as the time between the two items.

At the end of the experiment, also after an abort, the port is set back to 0.

In dummy mode no port is opened, but the items still check their values and wait for the pulse time, so an experiment behaves the same as with a parallel port.

Linux and Windows are supported. macOS is not: pyparallel is only installed on Linux and needs the Linux parallel port driver (`/dev/parportX`); only dummy mode works there. On Linux the [pyparallel](https://github.com/pyserial/pyparallel) package is used. On Windows the bundled InpOut32 driver (`inpout32.dll` / `inpoutx64.dll`) is used. This driver is installed the first time it is used, which needs administrator privileges: run OpenSesame once as administrator (see `InpOut32Drv_ReadMe.txt`).

InpOut32 is no longer maintained, and newer versions of Windows may not load its driver:

- *Memory integrity* (Windows Security, Device security, Core isolation details), on by default since Windows 11 22H2: Windows doesn't load the InpOut32 driver while it is on, also not as administrator.
- Windows 11 24H2 and later: since the April 2026 update, Windows stops trusting cross-signed drivers, such as the InpOut32 driver, once its new driver policy is enforced; only certified drivers and drivers on Microsoft's own list then load.

The init item then stops with the error "The InpOut32 driver could not be opened". On such a computer, a USB trigger interface (e.g. one that shows up as a serial port) is an alternative to the parallel port: it doesn't need InpOut32.


Documentation: <https://osdoc.cogsci.nl/4.1/manual/devices/parallel/>


## Installation

Install the plugin with pip, in the Python environment of OpenSesame:

    pip install opensesame-plugin-parallel_port_trigger


## License

This plugin is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version (GPL-3.0-or-later).

The full license text is in the file `COPYING`, and is also available at <https://www.gnu.org/licenses/gpl-3.0.html>.

This plugin contains works of others. The bundled InpOut32 driver DLLs (`inpout32.dll`, `inpoutx64.dll`) are Copyright (c) 2003-2015 Phil Gibbons, portions Copyright (c) 2000 logix4u.net, and are distributed under the MIT license; its text is in `opensesame_plugins/parallel_port_trigger/parallel_port_trigger_init/InpOut32Drv_license.txt`, next to the DLLs.


## Documentation

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <https://osdoc.cogsci.nl/>
