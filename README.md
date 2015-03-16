OpenSesame Plugin: Parallel Port Trigger
==========

*An OpenSesame Plug-in for sending stimulus synchronization triggers through the parallel port to data acquisition systems.*  

Copyright, 2013, Bob Rosbag  

Contributions: Code is based on the work of Per Sederberg. Debugged and polished by Edwin Dalmaijer.

1. About
--------

In EEG/ERP studies it is common to send triggers to mark the timestamp for significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to data acquisition systems.

The plug-in has three options:
- *Value* is a positive integer between 0-255 and specifies the trigger byte
- *Duration* (ms) is a positive integer, 'keypress', or 'mouseclick', to wait respectively for a specified interval in milliseconds, until a key has been pressed, or until a mouse button has been clicked. It specifies the time the trigger is active.
- *Port adress (Windows only)* is the hexadecimal value of the parallel port in Windows. This setting is ignored in Linux.


Linux and Windows are supported (possible also OSX, not tested). For Windows the `DLPortIO.dll` driver is used to access the parallel port. Install options are listed below.


Installation instructions: <http://osdoc.cogsci.nl/devices/triggers/>


2. LICENSE
----------

Parallel Port Trigger is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

- <http://www.gnu.org/licenses/gpl.txt>

Parallel Port Trigger contains works of others. For the full license information, please
refer to `debian/copyright`.

3. Documentation
----------------

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
