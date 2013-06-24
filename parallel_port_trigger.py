"""
11-03-2013
This based on io_port of Per Sederberg
Author: Bob Rosbag
Author: Edwin Dalmaijer


This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame. If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame import item
from libqtopensesame import qtplugin
from openexp.keyboard import keyboard
from PyQt4 import QtGui, QtCore


import warnings
import os

import imp


if os.name == 'posix':
	# import the local modified version of pyparallel
	# that allows for non-exclusive connections to the parport
	path_to_file = os.path.join(os.path.dirname(__file__), "parallelppdev.py")
	parallel = imp.load_source('parallel', path_to_file)
	try: 
		import parallelppdev as parallel
	except ImportError:
		print("The local modified version of pyparallel could not be loaded. Check if the file is present and if the file permissions are correct.")
if os.name == 'nt' :
	try:
		from ctypes import windll
	except ImportError:
		print("The ctypes module can not be loaded. Check if ctypes is installed correctly.")
else:
	try:
		import parallel
	except ImportError:
		print("The pyparallel module could not be loaded, please make sure pyparallel is installed correctly.")
		

# we only want one instance of pp, so here's a global var

if os.name == 'nt':
	_winpp = None
else:
	_pp = None

	
class parallel_port_trigger(item.item):

	"""
	This class (the class with the same name as the module)
	handles the basic functionality of the item. It does
	not deal with GUI stuff.
	"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor
		"""
		
		# The item_typeshould match the name of the module
		self.item_type = "parallel_port_trigger"
		
		# Provide a short accurate description of the item's functionality
		self.description = "Allows setting pins on the parallel port"
		
		# Set some item-specific variables
		self.value = 0
		self.duration = 500
		self.port = "0x378"
				
		# The parent handles the rest of the contruction
		item.item.__init__(self, name, experiment, string)

		# add cleanup code
		self.experiment.cleanup_functions.append(self.clean_up_the_mess)
						
	def clean_up_the_mess(self):
		
		if os.name == 'nt':
			if "_winpp" in globals():
				global _winpp
				if self.experiment.debug:
					print "parallel_port_trigger.clean_up_this_mess(): deleting _pp"
				if not _winpp is None:
					del _winpp
		else:
			if "_pp" in globals():
				global _pp
				if self.experiment.debug:
					print "parallel_port_trigger.clean_up_this_mess(): deleting _pp"
				if not _pp is None:
					del _pp

	def prepare(self):
	
		"""
		Prepare the item. In this case this means doing little.
		"""
		
		# Pass the word on to the parent
		item.item.prepare(self)		

		# get the global pp instance and initialize it if
		# necessary
		
		if os.name == 'nt':
			global _winpp
			if _winpp is None:
				try:
					_winpp = windll.dlportio
					print('Successfully accessed the parallel port on address: %s' % self.port)
				except OSError:
					print('Could not access the parallel port on address: %s' % self.port)
			self.winpp = _winpp
		else:
			global _pp
			if _pp is None:
				try:
					_pp = parallel.Parallel()
					print('Successfully accessed the parallel port (/dev/parport0).')
				except OSError:
					print('Could not access /dev/parport0.')
			self.pp = _pp

		
		# create keyboard object
		self.kb = keyboard(self.experiment,timeout=1)
		
		
		# Report success
		return True
				
	def run(self):
	
		"""
		Run the item. In this case this means putting the offline canvas
		to the display and waiting for the specified duration.
		"""
		
		# Set the pp value

		if os.name == 'nt':
			if not self.winpp is None:
				self.set_item_onset(self.winpp.DlPortWritePortUchar(int(self.port,0), self.value))
		else:
			if not self.pp is None:
				self.set_item_onset(self.pp.setData(self.value))


		t0 = self.time()
		t1 = t0


		while self.duration == None or t1 - t0 <= self.duration:
			t1 = self.time()
			key,presstime = self.kb.get_key()
			if key:
				break

		# unless duration was zero, turn it off
		if os.name == 'nt':
			if not self.winpp is None and self.duration !=0:
				self.winpp.DlPortWritePortUchar(int(self.port,0), 0)
		
		else:
			if not self.pp is None and self.duration !=0:
				self.pp.setData(0)
				
		# Report success
		return True
					
class qtparallel_port_trigger(parallel_port_trigger, qtplugin.qtplugin):

	"""
	This class (the class named qt[name of module] handles
	the GUI part of the plugin. For more information about
	GUI programming using PyQt4, see:
	<http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/classes.html>
	"""

	def __init__(self, name, experiment, string = None):
	
		"""
		Constructor
		"""
		
		# Pass the word on to the parents		
		parallel_port_trigger.__init__(self, name, experiment, string)		
		qtplugin.qtplugin.__init__(self, __file__)	
		
	def init_edit_widget(self):
	
		"""
		This function creates the controls for the edit
		widget.
		"""
		
		# Lock the widget until we're doing creating it
		self.lock = True
		
		# Pass the word on to the parent		
		qtplugin.qtplugin.init_edit_widget(self, False)
		
		# Create the controls
		# 
		# A number of convenience functions are available which 
		# automatically create controls, which are also automatically
		# updated and applied. If you set the varname to None, the
		# controls will be created, but not automatically updated
		# and applied.
		#
		# qtplugin.add_combobox_control(varname, label, list_of_options)
		# - creates a QComboBox
		# qtplugin.add_line_edit_control(varname, label)
		# - creates a QLineEdit		
		# qtplugin.add_spinbox_control(varname, label, min, max, suffix = suffix, prefix = prefix)
		
		self.add_spinbox_control("value", "Value", 0, 255, tooltip = "Value to set port")
		self.add_line_edit_control("duration", "Duration", tooltip = "Expecting a value in milliseconds, 'keypress' or 'mouseclick'")
		self.add_line_edit_control("port", "Port Adress (Windows only)", tooltip = "Adress of the parallel port in Windows")

		
		# Add a stretch to the edit_vbox, so that the controls do not
		# stretch to the bottom of the window.
		self.edit_vbox.addStretch()		
		
		# Unlock
		self.lock = True		
		
	def apply_edit_changes(self):
	
		"""
		Set the variables based on the controls
		"""
		
		# Abort if the parent reports failure of if the controls are locked
		if not qtplugin.qtplugin.apply_edit_changes(self, False) or self.lock:
			return False
				
		# Refresh the main window, so that changes become visible everywhere
		self.experiment.main_window.refresh(self.name)		
		
		# Report success
		return True

	def edit_widget(self):
	
		"""
		Set the controls based on the variables
		"""
		
		# Lock the controls, otherwise a recursive loop might aris
		# in which updating the controls causes the variables to be
		# updated, which causes the controls to be updated, etc...
		self.lock = True
		
		# Let the parent handle everything
		qtplugin.qtplugin.edit_widget(self)				
		
		# Unlock
		self.lock = False
		
		# Return the _edit_widget
		return self._edit_widget
