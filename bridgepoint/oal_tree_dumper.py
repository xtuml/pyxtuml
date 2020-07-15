# encoding: utf-8
# Copyright (C) 2020 John Törnblom
#
# This file is part of pyxtuml.
#
# pyxtuml is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# pyxtuml is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with pyxtuml. If not, see <http://www.gnu.org/licenses/>.

'''
Dump OAL token stream and AST to stdout
'''

import logging
import sys
import xtuml.tools

from ply import lex
from ply import yacc

from . import oal


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    
    print ('Enter the character stream below. Press Ctrl-D to begin parsing.')
    print ('')
    s = sys.stdin.read()
    
    print ('--------- Token Stream ----------')
    parser = oal.OALParser()
    lexer = lex.lex(module=parser)
    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    print ('--------- Syntax Tree ----------')
    root = oal.parse(s)
    w = xtuml.tools.Walker()
    w.visitors.append(xtuml.tools.NodePrintVisitor())
    w.accept(root)


    
