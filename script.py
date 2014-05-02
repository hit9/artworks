#!/usr/bin/env python
# coding=utf8

"""Usage:
scripy.py <art.txt> [<name>] [--width=<width>]
"""

import os
import sys
import subprocess

from docopt import docopt


args = docopt(__doc__)


art_txt = args.get('<art.txt>')
name = args.get('<name>') or os.path.splitext(art_txt)[0].title()

tpl = open('tpl/index.html').read()
txt = open(art_txt).read().strip('\n')
style_tpl = open('tpl/style.tpl.sass').read()

png = 'png/%s.png' % name

# smart width

lines = txt.split('\n')
max_col = 0

for line in lines:
    if len(line) > max_col:
        max_col = len(line)

width = len(name) * 42 + 7 * max_col + 5
width = args.get('--width') or str(width)

# get css from sass
proc = subprocess.Popen('sass', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=sys.stderr)
stdout, stderr = proc.communicate(input=style_tpl.format(len(lines)))
style = stdout

# render image
content = tpl.format(style, name, txt)
cmd = ['wkhtmltoimage', '--width', width, '-', png]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=sys.stdout,
                        stderr=sys.stderr)
stdout, stderr = proc.communicate(input=content)

sys.stdout.write(png)
