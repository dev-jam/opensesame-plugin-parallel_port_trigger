"""Parallel Port Trigger - send trigger"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "Parallel Port Trigger"
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "value",
        "label": "Value",
        "name": "line_edit_value",
        "info": "0-255"
    }, {
        "type": "checkbox",
        "var": "duration_check",
        "label": "Enable duration",
        "name": "checkbox_duration_check",
        "info": "Set the port back to 0 after the duration"
    }, {
        "type": "line_edit",
        "var": "duration",
        "label": "Duration (ms)",
        "name": "line_edit_duration"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> a Parallel Port Trigger Init item at the start of the experiment is needed to initialize the parallel port</small>"
    }, {
        "type": "text",
        "label": f"<small>Parallel Port Trigger version {__version__}</small>"
    }
]
