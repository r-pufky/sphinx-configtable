# ct: Config Table sphinx extensions for documentation.
#
# See README.md or files for detailed documentation and config values.

import re
from . import cmdmenu
from . import config

from .windows import firewall
from .windows import gpolicy
from .windows import regedit
from .windows import service
from .windows import tmanager
from .windows import tschedule

def setup(app):
  app.add_config_value('ct_separator', config.DEFAULT_SEPARATOR, '')
  app.add_config_value('ct_separator_replace', config.DEFAULT_REPLACE, '')
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