"""Parallel Port Trigger - send trigger"""

# The category determines the group for the plugin in the item toolbar
category = "Parallel Port Trigger"
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "value",
        "label": "Value",
        "name": "line_edit_port",
        "tooltip": "Value to set port"
    }, {
        "type": "checkbox",
        "var": "duration_check",
        "label": "Enable duration",
        "name": "checkbox_duration_check",
        "tooltip": "When enabled, a pulse is created instead of a state change"
    }, {
        "type": "line_edit",
        "var": "duration",
        "label": "Duration (ms)",
        "name": "line_edit_duration",
        "tooltip": "Value in ms"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Parallel Port Trigger Init item at the begin of the experiment is needed for initialization of the parallel port</small>"
    }, {
        "type": "text",
        "label": "<small>Parallel Port Trigger version 4.0.0</small>"
    }
]
