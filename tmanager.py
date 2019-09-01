# .. tmanager:: disable windows defender notification icon manager
#   :key: more details --> startup
#   :names: Windows Defender notification icon
#   :data: Disabled
#   :no_section:
#
#    .. note::
#       This is a free-form RST processed content for any additional
#       information pertaining to this task manager change.
#
#       Metadata can be split over multiple lines.
#
#    See TaskManager class docstring for additional options.
#
#    conf.py options:
#      ms_tmanager_separator: Unicode separator to use for GUI menuselection.
#          This uses the Unicode Character Name resolve a glyph.
#          Default: '\N{TRIANGULAR BULLET}'.
#          Suggestions: http://xahlee.info/comp/unicode_arrows.html
#          Setting this over-rides ms_separator value for task manager
#          display.
#      ms_tmanager_separator_replace: String separator to replace with Unicode
#          separator. Default: '-->'.
#      ms_tmanager_admin: String 'requires admin' modifier for GUI
#          menuselection. Default: ' (as admin)'.
#      ms_tmanager_content: String default GUI menuselection for opening group
#          policy.
#          Default: 'start --> Task Scheduler --> Task Scheduler Library'.
#      ms_tmanager_key_gui: Boolean True to enable GUI menuselection display of
#          task manager key. Default: True.
#
#    Directive Options:
#      key: String main task manager key to modify. Required.
#          e.g. Local Computer Policy --> Administrative Templates.
#      names: String or List of task manager names. Required.
#          e.g. Allow only system backup.
#      data: String or List of subkey data. Required.
#          e.g. Disabled.
#      admin: Flag enable admin requirement display in GUI menuselection.
#      no_section: Flag disable the creation of section using the task manager
#          arguments, instead of a 'tmanager docutils container' block.
#      show_title: Flag show task manager table caption (caption is arguments
#          title).
#      hide_gui: Flag hide GUI menuselection. This also disables :admin:.
#
# A task manager section can be setup to show multiple policy tables without
# additional data if multiple values are changed.
#
# .. tmanager:: disable windows defender notification icon manager
#   :key: more details --> startup
#   :names: Windows Defender notification icon
#   :data: Disabled
#
# .. tmanager:: disable windows defender notification icon manager
#   :key: more details --> startup
#   :names: Windows Defender notification icon
#   :data: Disabled
#   :no_section:
#   :hide_gui:

from . import config
from . import ms_table
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table


class TaskManagerData(ms_table.MsTableData):
  """Structure to hold task manager data and provide convience methods."""
  LENGTH_MISMATCH = ('Mis-matched sets of task manager key data: names and '
                     'data must all contain same number of elements.')


class TaskManager(ms_table.MsTable):
  """Generate task manager elements in a sphinx document.

  conf.py options:
    ms_tmanager_separator: Unicode separator to use for GUI menuselection.
        This uses the Unicode Character Name resolve a glyph.
        Default: '\N{TRIANGULAR BULLET}'.
        Suggestions: http://xahlee.info/comp/unicode_arrows.html
        Setting this over-rides ms_separator value for task manager display.
    ms_tmanager_separator_replace: String separator to replace with Unicode
        separator. Default: '-->'.
    ms_tmanager_admin: String 'requires admin' modifier for GUI menuselection.
        Default: ' (as admin)'.
    ms_tmanager_content: String default GUI menuselection for opening group
        policy. Default: 'start --> Task Scheduler --> Task Scheduler Library'.
    ms_tmanager_key_gui: Boolean True to enable GUI menuselection display of
        task manager key. Default: True.

  Directive Options:
    key: String main task manager key to modify. Required.
        e.g. Local Computer Policy --> Administrative Templates.
    names: String or List of task manager names. Required.
        e.g. Allow only system backup.
    data: String or List of subkey data. Required.
        e.g. Disabled.
    admin: Flag enable admin requirement display in GUI menuselection.
    no_section: Flag disable the creation of section using the task manager
        arguments, instead of a 'tmanager docutils container' block.
    show_title: Flag show task manager table caption (caption is arguments
        title).
    hide_gui: Flag hide GUI menuselection. This also disables :admin:.
  """
  required_arguments = 1
  optional_arguments = 0
  final_argument_whitespace = True
  option_spec = {
    'key': directives.unchanged_required,
    'names': directives.unchanged_required,
    'types': directives.unchanged_required,
    'data': directives.unchanged_required,
    'admin': directives.flag,
    'no_section': directives.flag,
    'show_title': directives.flag,
    'hide_gui': directives.flag,
  }
  has_content = True
  add_index = True

  def __init__(self, *args, **kwargs):
    """Initalize base Table class and generate separators."""
    super().__init__(*args, **kwargs)
    self.sep = config.get_sep(
      self.state.document.settings.env.config.ms_tmanager_separator,
      self.state.document.settings.env.config.ms_separator)
    self.rep = config.get_rep(
      self.state.document.settings.env.config.ms_tmanager_separator_replace,
      self.state.document.settings.env.config.ms_separator_replace)

    self.text_content = (
        self.state.document.settings.env.config.ms_tmanager_content)
    self.key_gui = self.state.document.settings.env.config.ms_tmanager_key_gui

    if 'admin' in self.options:
      self.key_mod = self.state.document.settings.env.config.ms_tmanager_admin
    else:
      self.key_mod = ''

  def _sanitize_options(self):
    """Sanitize directive user input data.

    * Strips whitespace from task manager component key.
    * Converts names, data to python lists with whitespace stripped;
      ensures that the lists are of the same length.
    * Parses directive arguments for title.

    Returns:
      TaskManagerData object containing sanitized directive data.
    """
    key = ''.join([x.strip() for x in self.options['key'].split('\n')])
    names_list = [x.strip() for x in self.options['names'].split(',')]
    data_list = [x.strip() for x in self.options['data'].split(',')]
    title, _ = self.make_title()

    return TaskManagerData(key,
                           [names_list, data_list],
                           title,
                           cols=2,
                           gui=self.key_gui,
                           key_mod=self.key_mod)


def setup(app):
  app.add_config_value('ms_tmanager_admin', ' (as admin)', '')
  app.add_config_value('ms_tmanager_content', 'start --> task manager', '')
  app.add_config_value('ms_tmanager_key_gui', True, '')
  app.add_config_value('ms_tmanager_separator', config.DEFAULT_SEPARATOR, '')
  app.add_config_value('ms_tmanager_separator_replace', config.DEFAULT_REPLACE, '')

  app.add_directive('tmanager', TaskManager)