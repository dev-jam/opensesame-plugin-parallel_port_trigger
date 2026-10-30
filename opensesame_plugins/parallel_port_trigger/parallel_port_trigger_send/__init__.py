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
        "var": "pulse_mode",
        "label": "Enable pulse mode",
        "name": "checkbox_pulse_mode",
        "info": "Set the port back to 0 after the pulse time"
    }, {
        "type": "line_edit",
        "var": "pulse_time",
        "label": "Pulse time (ms)",
        "name": "line_edit_pulse_time"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> a Parallel Port Trigger Init item at the start of the experiment is needed to initialize the parallel port</small>"
    }, {
        "type": "text",
        "label": f"<small>Parallel Port Trigger version {__version__}</small>"
    }
]
