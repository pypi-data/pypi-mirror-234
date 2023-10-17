"""
this module provides the directive python.
"""

from docutils.parsers.rst import directives
from docutils.nodes import raw
from docutils.nodes import General
from docutils.nodes import Element
from docutils.nodes import caption
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx
from ansi2html import Ansi2HTMLConverter

from .validators import parse_theme
from .execute import get_python_disassembly
from .execute import wrap_content
from .utilities import caption_wrapper

class DisassemblyNode(General, Element):
    """
    python directive.
    """

class DisassemblyContentNode(General, Element):
    """
    content of python.
    """

class DisassemblyCaptionNode(caption):
    """
    caption of python directive.
    """

class DisassemblyDirective(SphinxDirective):
    """
    an environment for python.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
        'font-size': directives.unchanged,
        'theme': parse_theme,
        'caption': directives.unchanged_required,
        'begin': directives.positive_int,
        'end': directives.positive_int,
    }

    def run(self):
        """Render this environment"""
        overflow_style = 'overflow-x:auto;' if self.options.get('overflow', 'scroll') == 'scroll' else 'white-space:pre-wrap;'
        font_size = self.options.get('font-size')
        theme = self.options.get('theme', 'light')
        begin = self.options.get('begin', 1)
        end = self.options.get('end')

        file_path, *_ = self.content
        _, file_path = self.env.relfn2path(file_path)
        convertor = Ansi2HTMLConverter(dark_bg=(theme == 'dark'), line_wrap=False, inline=True)

        with open(file_path, 'r', encoding='utf8') as file:
            output = get_python_disassembly(file.read(), begin, end)

        html = convertor.convert(output)
        node = caption_wrapper(self, DisassemblyNode(), DisassemblyCaptionNode, self.options.get("caption"))

        content = DisassemblyContentNode()
        content.children.append(raw('', wrap_content(html, overflow_style, theme, font_size), format='html'))
        node.children.append(content)
        self.add_name(node)
        return [node]

def visit_python_node(self, node):
    """
    enter :class:`DisassemblyNode` in html builder.
    """
    self.body.append(self.starttag(node, "div", CLASS="python-disassembly"))

def depart_python_node(self, _node):
    """
    leave :class:`DisassemblyNode` in html builder.
    """
    self.body.append("</div>")

def visit_caption_node(self, node):
    """
    enter :class:`DisassemblyCaptionNode` in html builder
    """
    if not node.astext():
        return

    self.body.append(self.starttag(node, "div", CLASS="python-disassembly-caption"))
    self.add_fignumber(node.parent)
    self.body.append(" ")
    self.body.append(self.starttag(node, "span", CLASS="caption-text"))

def depart_caption_node(self, node):
    """
    leave :class:`DisassemblyCaptionNode` in html builder
    """
    if not node.astext():
        return

    self.body.append("</span>")
    self.body.append("</div>")

def visit_content_node(self, node):
    """
    enter :class:`DisassemblyContentNode` in html builder.
    """
    self.body.append(self.starttag(node, "div", CLASS='highlight-rst notranslate highlight'))

def depart_content_node(self, _node):
    """
    leave :class:`DisassemblyContentNode` in HTML builder.
    """
    self.body.append("</div>")

def initialize_numfig_format(_application, config):
    """
    initialize :confval:`numfig_format`.
    """
    config.numfig_format['python-disassembly'] = 'Python Disassembly %s'

def setup(application: Sphinx):
    """
    setup python directive.
    """

    application.add_directive('python-disassembly', DisassemblyDirective)

    application.connect(event="config-inited", callback=initialize_numfig_format)

    application.add_enumerable_node(
        node=DisassemblyNode,
        figtype='python-disassembly',
        html=(visit_python_node, depart_python_node),
        singlehtml=(visit_python_node, depart_python_node),
    )
    application.add_node(
        node=DisassemblyCaptionNode,
        override=True,
        html=(visit_caption_node, depart_caption_node),
        singlehtml=(visit_caption_node, depart_caption_node),
    )
    application.add_node(
        node=DisassemblyContentNode,
        html=(visit_content_node, depart_content_node),
        singlehtml=(visit_content_node, depart_content_node),
    )
