"""Parallel Port Trigger - initializes the parallel port device"""

# The category determines the group for the plugin in the item toolbar
category = "Parallel Port Trigger"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "dummy_mode",
        "label": "Dummy mode",
        "name": "checkbox_dummy",
        "tooltip": "Run in dummy mode"
    },  {
        "type": "checkbox",
        "var": "verbose",
        "label": "Verbose mode",
        "name": "checkbox_verbose",
        "tooltip": "Run in verbose mode"
    }, {
        "type": "line_edit",
        "var": "port",
        "label": "Port Address",
        "name": "line_edit_port",
        "tooltip": "Address of the parallel port, value is a hexadecimal number (Windows) or path (Linux)"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Parallel Port Trigger Init item at the begin of the experiment is needed for initialization of the parallel port</small>"
    }, {
        "type": "text",
        "label": "<small>Parallel Port Trigger version 4.1.1</small>"
    }
]
