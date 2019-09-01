# ms: Microsoft sphinx extensions for documentation.
#
# See files for detailed documentation and config values.
#
# conf.py
# -------
#   ms_separator: Unicode default separator to render for all ms extensions.
#       Default: '\N{TRIANGULAR BULLET}'
#   ms_separator_replace: String default separator to be replace with Unicode
#       separator for all ms extensions. Default: '-->'
#
# gpolicy
# -------
# Group Policy Extension Directive. Renders group policy settings.
#
# .. gpolicy:: Disable windows Defender Service
#   :key: Computer Configuration --> Administrative Templates
#   :names: Turn off Windows Defender
#   :data: Enabled
#
#    .. note::
#       This is a free-form RST processed content for any additional
#       information pertaining to this group policy change.
#
#       See GroupPolicy class docstring for additional options.
#
#       A policy section can be setup to show multiple policy tables without
#       additional data if multiple values are changed.
#
# regedit
# -------
# Registry Extenstion Directive. Renders Registry settings.
#
# .. regedit:: Change some Registry Values
#   :key:   HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\
#   :names: GameDVR_Enabled, other
#   :types: DWORD,           DWORD64
#   :data:  0,               3
#   :admin:
#
#    .. note::
#       This is a free-form RST processed content for any additional
#       information pertaining to this registry change.
#
#       Single or multile registry values can be used in the directive.
#
#       See RegEdit class docstring for additional options.
#
# cmdmenu
# -------
# Custom menuselection role that allows for custom separator.
#
# :cmdmenu:`start --> app`
#   Role for menuselection with custom separator.
#
#   See CmdMenu class docstring for additional options.
#
# tschedule
# ---------
# Task Scheduler Extension Directive. Renders Task Scheduler settings.
#
# .. tschedule:: Disable OneDrive schedule update task
#   :key: OneDrive Standalone Update Task v2
#   :names: Task
#   :data: Disabled
#
#    .. note::
#       This is a free-form RST processed content for any additional
#       information pertaining to this group policy change.
#
#       See TaskScheduler class docstring for additional options.
#
#       A policy section can be setup to show multiple policy tables without
#       additional data if multiple values are changed.
#
# tmanager
# --------
# Task Manager Extension Directive. Renders Task Manager settings.
#
# .. tmanager:: Disable OneDrive schedule update task
#   :key: OneDrive Standalone Update Task v2
#   :names: Task
#   :data: Disabled
#
#    .. note::
#       This is a free-form RST processed content for any additional
#       information pertaining to this group policy change.
#
#       See TaskScheduler class docstring for additional options.
#
#       A policy section can be setup to show multiple policy tables without
#       additional data if multiple values are changed.
#  add firewall service

import re
from . import cmdmenu
from . import config
from . import firewall
from . import gpolicy
from . import regedit
from . import service
from . import tmanager
from . import tschedule

def setup(app):
  app.add_config_value('ms_separator', config.DEFAULT_SEPARATOR, '')
  app.add_config_value('ms_separator_replace', config.DEFAULT_REPLACE, '')

  cmdmenu.setup(app)
  firewall.setup(app)
  gpolicy.setup(app)
  regedit.setup(app)
  service.setup(app)
  tmanager.setup(app)
  tschedule.setup(app)

  return {
    'version': '0.1',
    'parallel_read_safe': True,
    'parallel_write_safe': True,
  }