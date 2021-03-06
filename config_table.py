# Base config table template. Abstract classes. Do not use directly.

import inspect
from . import config
from . import cmdmenu
from docutils import nodes
from docutils.parsers.rst.directives.tables import Table


class ConfigTableData(object):
  """Structure to hold config table data and provide convience methods.

  Attributes:
    LENGTH_MISMATCH: String explanation of data mismatch.
    key: String whitespace striped text for 'KEY_TITLE:'. See ConfigTable.
    data: List of Lists containing string data to display in table per column.
        Order is preserved. Minimum one list, all lists need at least one
        element.
    title: nodes.title object containing parsed directive arguments as title.
    key_title_gui: Boolean True to render table key as a menuselection role.
    key_title_admin_text: String title modifier for GUI key display.
  """
  LENGTH_MISMATCH = ('Abstract ConfigTableData length mismatch error. You '
                     'should not see this.')

  def __init__(self,
               key=None,
               data=None,
               title=None,
               key_title_gui=False,
               key_title_admin_text=None):
    """Initialize config table data structure with data or defaults.

    Args:
      key_title: String directive option key. Default: None.
      data: List of Lists containing string data to display in table (each list
          is rendered as a column). Order is preserved. Minimum one list.
      title: nodes.title object. Default: nodes.title().
      key_title_gui: Boolean True to render table key as a menuselection role.
          Default: False (render as normal text).
      key_title_admin_text: String key modifier for GUI display. Default: ''.

    Raises:
      ValueError if names, types and data lists lengths do not match.
    """
    # TODO: convert to key_title when all converted.
    self.key = key
    self.data = data or [[]]
    self.title = title or nodes.title()
    self.key_title_gui = key_title_gui
    self.key_title_admin_text = key_title_admin_text or ''

    required_length = len(self.data[0])
    if not all(len(lst) == required_length for lst in self.data[1:]):
      raise ValueError

  def raw_title(self):
    """Return title attribute as String."""
    return self.title.astext()

  def zip(self):
    """Return zip of all data elements together.

    Returns:
      zip() containing all list data.
    """
    return zip(*self.data)


class ConfigTable(Table):
  """ Abstract config table encapulsation of Table.

  .. configtable:: {DIRECTIVE TITLE}
    :data.key_title:   {KEY TITLE}
    :data.data[0]: {COL 1}
    ...
    :data.data[4]: {COL 4}


  A table is rendered using the following template, implementations of
  ConfigTable should set these options as needed:

  SECTION: {DIRECTIVE TITLE}
  LAUNCH: {self.text_launch (always rendered with :cmdmenu:)}
  CAPTION: {DIRECTIVE TITLE}
  +-----------------------------+
  | KEY_TITLE: {data.key_title} |
  +---------+-----+-------------+
  | {COL 1} | ... | {COL 4}     |
  +---------+-----+-------------+

    SUBTEXT: {ANY ADDTIONAL RST TEXT TO RENDER}

  Directives:
    :no_section: Flag to disable creation of 'SECTION:'.
    :no_launch: Flag to disable creation of 'LAUNCH:'.
    :no_caption: Flag to disable creation of 'CAPTION:'.
    :no_key_title: Flag to disable creation of row 'KEY_TITLE:'.
  """

  def run(self):
    """Run the config table generation directive.

    Determine the calling class name and label directive accordingly.

    Returns:
      List containing config table directive.
    """
    caller_name = inspect.currentframe().f_locals['self'].__class__.__name__
    directive = []

    try:
      data = self._sanitize_options()
    except ValueError as e:
      return [self.state_machine.reporter.error(
          data.LENGTH_MISMATCH,
          nodes.literal_block(self.block_text, self.block_text),
          line=self.lineno)]

    if 'no_section' in self.options:
      directive_node = nodes.container(rawsource='\n'.join(self.content),
                                       ids=[data.raw_title()])
      directive_node.set_class(caller_name)
      directive = [directive_node]
      container = directive_node
    else:
      section_target, section = self._section(data.raw_title())
      directive = [section_target, section]
      container = section

    if 'no_launch' not in self.options:
      container += self._gui_command('%s%s' % (self.text_launch, data.key_title_admin_text),
                                     self.sep,
                                     self.rep)

    container += self.build_table(data)
    self.state.nested_parse(self.content, self.content_offset, container)

    return directive

  def build_table(self, data):
    """Build a table to display values.

    Args:
      data: Data object containing source data.

    Side Effects:
      'show_title' directive option will remove the inclusion of a generated
          caption for table.

    Returns:
      nodes.table constructed with source data.
    """
    table = nodes.table()
    table_group = nodes.tgroup(cols=len(data.data))
    table += table_group

    table_group.extend(
        [nodes.colspec(colwidth=1, colname='c%s' % i) for i in range(len(data.data))]
    )

    table_body = nodes.tbody()
    table_group += table_body
    rows = []

    if 'no_key_title' not in self.options:
      key_row = nodes.row()
      key_entry = nodes.entry(morecols=len(data.data))
      if data.key_title_gui:
        key_entry += self._gui_command(data.key, self.sep, self.rep)
      else:
        key_entry += nodes.paragraph(text=data.key)
      key_row += key_entry
      rows.append(key_row)

    for element in data.zip():
      reg_row = nodes.row()
      for cell in element:
        entry = nodes.entry()
        entry += nodes.paragraph(text=cell)
        reg_row += entry
      rows.append(reg_row)
    table_body.extend(rows)

    self.add_name(table)
    if 'no_caption' not in self.options:
      table.insert(0, data.title)

    return table

  def _parse_list(self, key, split=','):
    """Parse directive list and returned sanitized python list.

    Args:
      key: String key to use for self.options dictionary.
      split: String character to split list on. Default: ','.

    Returns:
      List containing directive option with whitespace stripped,
      split on the split value.
    """
    return [x.strip() for x in self.options[key].split(split)]

  def _gui_command(self, text, sep, rep):
    """Render a menuselection node specifically for given text.

    Args:
      text: String content text to use. Default: gpolicy_content.
      sep: Unicode separator to use rendering menu.
      rep: String separator string to replace with Unicode string.

    Returns:
      list[nodes.Node] containing group policy menuselection data.
    """
    return cmdmenu.gen_menu(text, sep, rep)

  def _section(self, title):
    """Generate section node for given title.

    title:
      title: String title to use when creating a section.

    Returns:
      Tuple (nodes.target, nodes.section) section nodes.
    """
    target = nodes.target()
    section = nodes.section()
    section_text_nodes, _ = self.state.inline_text(title, self.lineno)
    section_title = nodes.title(title, '', *section_text_nodes)
    section += section_title
    self.state.add_target(title, '', target, self.lineno)

    return (target, section)
