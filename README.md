OpenSesame Plugin: Parallel Port Trigger
==========

*An OpenSesame Plugin for sending stimulus synchronization triggers through the parallel port to data acquisition systems.*  

Copyright, 2013, Bob Rosbag  

Contributions: Code is based on the work of Per Sederberg. Debugged and polished by Edwin Dalmaijer.

1. About
--------

In EEG/ ERP studies it is common to send triggers to mark the time of significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to the EEG apparatus. This can be done with the parallel port trigger plugin which works in Linux and Windows. For Windows the `DLPortIO.dll` driver is used to access the parallel port.

The plugin has three input boxes:
- Value ranges between 0-255.
- Duration in ms
- Parallel port adress has to be specified manually (Windows only). 


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
