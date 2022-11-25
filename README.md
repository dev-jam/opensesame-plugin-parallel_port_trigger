OpenSesame Plug-in: Parallel Port Trigger
==========

*An OpenSesame plug-in for sending stimulus synchronization triggers through the parallel port to data acquisition systems.*  

Copyright, 2022, Bob Rosbag  

Contributions: Code is based on the work of Per Sederberg. Debugged and polished by Edwin Dalmaijer.


## 1. About
--------

In EEG/ERP studies it is common to send triggers to mark the timestamp for significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to data acquisition systems.

The plug-in has an *init* item which should be placed at the beginning of an experiment and a *trigger* item for initiating triggers:

- *Dummy mode* for testing experiments.
- *Port adress* for Windows: hexadecimal or decimal value, for Linux: full path or port number.
- *Value* is a positive integer between 1-255 and specifies the trigger byte.
- *Enable duration* option to enable the duration parameter.
- *Duration* is the duration in ms.


Linux and Windows are supported (possible also OSX, not tested). For Windows the `DLPortIO.dll` driver is used to access the parallel port. No need for driver installation.


Documentation: <http://osdoc.cogsci.nl/devices/triggers/>


## 2. LICENSE
----------

The Parallel Port Trigger plug-in is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

- <http://www.gnu.org/licenses/gpl.txt>

This plug-in contains works of others.


## 3. Documentation
----------------

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
