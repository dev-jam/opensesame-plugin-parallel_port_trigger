OpenSesame Plug-in: Parallel Port Trigger
==========

*An OpenSesame plug-in for sending stimulus synchronization triggers through the parallel port to data acquisition systems.*  

Copyright, 2022, Bob Rosbag  

Contributions: Code is based on the work of Per Sederberg. Debugged and polished by Edwin Dalmaijer.


## About

In EEG/ERP studies it is common to send triggers to mark the timestamp for significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to data acquisition systems.

The plug-in has an *init* item which should be placed at the beginning of an experiment and a *trigger* item for initiating triggers:

- *Dummy mode* for testing experiments without a parallel port.
- *Verbose mode* prints messages about what the items do.
- *Port address* for Windows: hexadecimal, starting with 0x (0x378; Device Manager shows it as 0378), for Linux: port number (0 in /dev/parport0).
- *Value* is an integer between 0 and 255 and specifies the trigger byte. It may be a variable, such as `{trigger}`.
- *Enable duration* option to enable the duration parameter: the port is set back to 0 after the duration (a pulse).
- *Duration* is the duration in ms. It may be a variable.

There are two ways to send a trigger:

- *With duration*: one item sends a pulse, e.g. value 23 for 10 ms, and then sets the port back to 0.
- *Without duration*: the value stays on the port until another item changes it. For example, one item sends 23 and a later item sends 0; the trigger then lasts as long as the time between the two items.

At the end of the experiment, also after an abort, the port is set back to 0.

In dummy mode no port is opened, but the items still check their values and wait for the duration, so an experiment behaves the same as with a parallel port.

Linux and Windows are supported. macOS is not: pyparallel is only installed on Linux and needs the Linux parallel port driver (`/dev/parportX`); only dummy mode works there. On Linux the [pyparallel](https://github.com/pyserial/pyparallel) package is used. On Windows the bundled InpOut32 driver (`inpout32.dll` / `inpoutx64.dll`) is used. This driver is installed the first time it is used, which needs administrator privileges: run OpenSesame once as administrator (see `InpOut32Drv_ReadMe.txt`).


Documentation: <http://osdoc.cogsci.nl/devices/triggers/>


## License

This software is distributed under the terms of the GNU General Public License 3. The full license should be included in the file `COPYING`, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>

This plug-in contains works of others.


## Documentation

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
