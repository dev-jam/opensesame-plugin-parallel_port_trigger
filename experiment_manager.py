#-*- coding:utf-8 -*-

"""

01-03-2015
Author: Bob Rosbag


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

from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas

class experiment_manager(item):

    """
    This class (the class with the same name as the module) handles the basic
    functionality of the item. It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'An example new-style plug-in'

    def reset(self):

        """
        desc:
            Resets plug-in to initial values.
        """

        # Here we provide default values for the variables that are specified
        # in info.json. If you do not provide default values, the plug-in will
        # work, but the variables will be undefined when they are not explicitly
        # set in the GUI.
        self._experiment_file_name = u'example.opensesame.tar.gz'


    def prepare(self):

        """The preparation phase of the plug-in goes here."""

        # Call the parent constructor.
        item.prepare(self)


    def run(self):

        """The run phase of the plug-in goes here."""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().
        import os
        fs = os.sep

        subject_nr          = self.get("subject_nr")
        home_path           = self.experiment.experiment_path
        
        command       = u'opensesamerun'
        file_name     = self.get("_experiment_file_name")
        subject_arg   = u'--subject=' + str(subject_nr)
        log_arg       = u'--logfile=' + home_path + fs + file_name + u'_-_' + u'subject-' + str(subject_nr) + u'.csv'
        screen_arg    = u'--fullscreen'
        
        
        args = [command, file_name, subject_arg, log_arg, screen_arg]
        print(args)
        
        import subprocess
        subprocess.call(args)
    

class qtexperiment_manager(experiment_manager, qtautoplugin):
    
    """
    This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):

        """
        Constructor.
        
        Arguments:
        name        --    The name of the plug-in.
        experiment    --    The experiment object.
        
        Keyword arguments:
        script        --    A definition script. (default=None)
        """

        # We don't need to do anything here, except call the parent
        # constructors.
        experiment_manager.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

    def init_edit_widget(self):

        """
        Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        # First, call the parent constructor, which constructs the GUI controls
        # based on info.json.
        qtautoplugin.init_edit_widget(self)
        # If you specify a 'name' for a control in info.json, this control will
        # be available self.[name]. The type of the object depends on the
        # control. A checkbox will be a QCheckBox, a line_edit will be a
        # QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
        # to the setEnabled() slot of the QLineEdit. This has the effect of
        # disabling the QLineEdit when the QCheckBox is uncheckhed.


