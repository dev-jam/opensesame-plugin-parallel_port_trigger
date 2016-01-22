OpenSesame Plug-in: Parallel Port Trigger (in Testing)
==========

*An OpenSesame Plug-in for sending stimulus synchronization triggers through the parallel port to data acquisition systems.*  

Copyright, 2016, Bob Rosbag  

Contributions: Code is based on the work of Per Sederberg. Debugged and polished by Edwin Dalmaijer.

1. About
--------

In EEG/ERP studies it is common to send triggers to mark the timestamp for significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to data acquisition systems.

The plug-in has four options:
- *Value* is a positive integer between 1-255 and specifies the trigger byte
- *Duration* (ms) is a positive integer, 'keypress', or 'mouseclick', to wait respectively for a specified interval in milliseconds, until a key has been pressed, or until a mouse button has been clicked. It specifies the time the trigger is active.
- *Port adress* is the hexadecimal value of the parallel port in Windows or the path to the device in Linux.
- *Dummy mode* for testing experiments

Linux and Windows are supported (possible also OSX, not tested). For Windows the `DLPortIO.dll` driver is used to access the parallel port. Install options are listed below.


Installation instructions: <http://osdoc.cogsci.nl/devices/triggers/>


2. LICENSE
----------

The Parallel Port Trigger Plug-in is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

- <http://www.gnu.org/licenses/gpl.txt>

Parallel Port Trigger contains works of others. For the full license information, please
refer to `debian/copyright`.


3. Documentation
----------------

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
