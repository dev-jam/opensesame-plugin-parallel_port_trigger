# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [5.1.0] - 2026-10-30

- the send item's *Enable duration* and *Duration* are now called *Enable pulse mode* and *Pulse time*, as in the radboudbox plug-in, also in the script (`pulse_mode`, `pulse_time` instead of `duration_check`, `duration`) and in the error messages
- the old names in an experiment or set by an inline script are converted, with a warning; warning: versions up to 5.0.2 ignore the new names, so an experiment saved with this version sends no pulse there (the value stays on the port)
- the send item also logs the pulse time as `pptrigger_pulse_time`; `pptrigger_duration` stays

## [5.0.2] - 2026-10-21

- fixed: since 5.0.0, a Windows port address without 0x, such as 0378 (how Device Manager shows 0x378), was read as the decimal number 378 (0x17a) and written to; it now gives an error, as before 5.0.0; decimal addresses are no longer accepted, because OpenSesame stores both as the same number
- the items show a short hint next to the port address, value, dummy mode and duration settings; their tooltips were never shown by OpenSesame and are removed
- readme: macOS is not supported (only dummy mode works there); verbose mode is described
- fixed: a Windows port address above 0xFFFF, outside the 16-bit I/O address range, was accepted and written to; it now gives an error
- fixed: an enable duration value other than 'yes' or 'no' (e.g. 'Yes' from a variable) was treated as 'no', so the value stayed on the port instead of a pulse; it now gives an error in the prepare phase

## [5.0.1] - 2026-10-18

- fixed: since 5.0.0, a dummy mode value other than 'yes' or 'no' (e.g. from a variable) was treated as 'no' and opened the parallel port; before 5.0.0 the plug-in then sent nothing; it now gives an error
- fixed: since 5.0.0, a Windows port address below 0x100, such as 0 (the Linux port number), was accepted and written to; it now gives an error
- note: 5.0.0 also changed the verbose messages, which its changelog does not list: 'Waiting <n> ms to reset' and 'Resetting the parallel port to zero' became one message 'Waited <n> ms to reset the parallel port to zero' (also for a duration of 0); closing the port also prints 'Resetting the parallel port to all zero'; on Windows 'Loading <dll>' and 'Using parallel port on address: <address>' were added

## [5.0.0] - 2026-10-17

- fixed: license in package metadata (was shown as proprietary on PyPI)
- fixed: dependency changed to python >= 3.10
- fixed: on Windows the item onset (`time_<item>`) was set to the return value of the DLL call instead of a timestamp
- fixed: a trigger value outside 0-255 gave the error 'wrong port address' (Linux) or was silently truncated (Windows); it now gives a clear error, also in dummy mode
- fixed: a negative duration was silently ignored; it now gives an error
- the port is set back to 0 when the experiment ends or is aborted
- Windows: an error is given when the InpOut32 driver is not installed, instead of silently sending nothing
- the duration is now read in the run phase, like the value, so an earlier item can set it; an invalid duration now gives an error in the run phase instead of the prepare phase
- dummy mode: the send item now sets the item onset (`time_<item>`) and `pptrigger_duration`, and waits for the duration, like with a parallel port
- dummy mode: a second init item now gives an error, like with a parallel port
- verbose messages are printed after the pulse instead of during it, so they no longer make the pulse longer
- Windows: the port address may also be a decimal number; an invalid address now gives a clear error in the init item
- the init item no longer imports Qt; removed the unused `qtParallelPortTriggerInit` class
- removed `libopensesame.py3compat`
- the version label in the items is read from the installed package, so the version is only set in `pyproject.toml`
- `experiment.pptrigger_dummy_mode` and `experiment.pptrigger_verbose` are now booleans instead of 'yes'/'no'
- on Windows `experiment.pptrigger` is a wrapper with `setData()`, like pyparallel on Linux; it passes other calls on to the DLL

## [4.3.0] - 2025-09-05

- convert string handling to f-strings

## [4.2.0] - 2025-07-17

- license cleanup

## [4.1.0] - 2023-11-14

- removed old keyboard instance
    
## [4.0.1] - 2023-08-30

- fixed dependencies
    
## [4.0.0] - 2023-08-15

- new style api OpenSesame 4.0
- lots of small fixes and code cleanup
    
## [3.2.0] - 2023-08-13

Final release for OpenSesame 3 API

- small bugfixes
    
## [v2.3.0] - 2022-11-25

- new plugin code style
- debian packaging fixed
    
## [v2.0.0] - 2021-04-15


    
## [v6.0] - 2017-01-31

- added reset of parallel port at the init item

    
## [v5.0] - 2016-11-15

- Old style use of dlportio method migrated to new style
- Windows driver integrated

    
## [v4.0] - 2016-04-22

- split plugin in two items: 'init' and 'execution of trigger'
- restored duration with checkbox to enable duration
- bugfixes

    
## [v3.1.2] - 2016-03-24

Cleaned .pyc files

    
## [v3.1] - 2016-03-24

- fixed: dummy mode was always enabled
- dummy mode is now chosen in the first occurrence of the item
- dummy mode now works properly when there is no parallel port and/or driver

    
## [v3.0.1] - 2016-03-24

- Fixed exception handling and import error
- updated documentation, removal of duration

    
## [v3.0] - 2016-02-19

- Opensesame 3 Style
- Switch based

    
## [v2.0] - 2015-03-16


    
## [v1.0] - 2014-01-21


    
## [1.0.0] - 2014-01-21

Stable release


## 1.0.0-rc1 - 2013-08-12

first public release


[Unreleased]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/5.1.0...HEAD
[5.1.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/5.0.2...5.1.0
[5.0.2]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/5.0.1...5.0.2
[5.0.1]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/5.0.0...5.0.1
[5.0.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/4.3.0...5.0.0
[4.3.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/4.2.0...4.3.0
[4.2.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/4.1.0...4.2.0
[4.1.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/4.0.1...4.1.0
[4.0.1]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/4.0.0...4.0.1
[4.0.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/3.2.0...4.0.0
[3.2.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v2.3.0...3.2.0
[v2.3.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v2.0.0...v2.3.0
[v2.0.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v6.0...v2.0.0
[v6.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v5.0...v6.0
[v5.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v4.0...v5.0
[v4.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v3.1.2...v4.0
[v3.1.2]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v3.1...v3.1.2
[v3.1]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v3.0.1...v3.1
[v3.0.1]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v3.0...v3.0.1
[v3.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v2.0...v3.0
[v2.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/v1.0...v2.0
[v1.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/1.0.0...v1.0
[1.0.0]: https://github.com/dev-jam/opensesame-plugin-parallel_port_trigger/compare/1.0.0-rc1...1.0.0
