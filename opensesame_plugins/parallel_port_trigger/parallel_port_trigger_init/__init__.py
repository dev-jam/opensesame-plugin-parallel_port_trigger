"""Parallel Port Trigger - initializes the parallel port device"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "Parallel Port Trigger"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "dummy_mode",
        "label": "Dummy mode",
        "name": "checkbox_dummy",
        "info": "No parallel port is used"
    },  {
        "type": "checkbox",
        "var": "verbose",
        "label": "Verbose mode",
        "name": "checkbox_verbose"
    }, {
        "type": "line_edit",
        "var": "port",
        "label": "Port Address",
        "name": "line_edit_port",
        "info": "Windows: e.g. 0x378, Linux: 0 for /dev/parport0"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> a Parallel Port Trigger Init item at the start of the experiment is needed to initialize the parallel port</small>"
    }, {
        "type": "text",
        "label": f"<small>Parallel Port Trigger version {__version__}</small>"
    }
]
