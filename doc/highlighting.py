from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re

code      = """\
Index: exhibit_apachesolr.info
==============================================================
RCS file: exhibit_apachesolr.info
diff -N exhibit_apachesolr.info
--- /dev/null 1 Jan 1970 00:00:00 -0000
+++ exhibit_apachesolr.info 8 Nov 2008 16:18:41 -0000
"""

def get_hl_lines(code):
    i = 1
    lines = []
    for line in code.split('\n'):
        if line.startswith('@h@'):
            lines.append(i)
        i += 1
    return lines

hl_lines = get_hl_lines(code)

if len(hl_lines) != 0:
    hl_regex = re.compile(r'^@h@', re.MULTILINE)
    code     = re.sub(hl_regex, '', code)

lexer     = PythonLexer()
formatter = HtmlFormatter(linenos=True, style='emacs', encoding='utf-8', nowrap=False, hl_lines=hl_lines)
print highlight(code, lexer, formatter)
print formatter.get_style_defs('.highlight')

