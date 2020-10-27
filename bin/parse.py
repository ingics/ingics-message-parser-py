#!/usr/bin/env python

import sys
import pprint
from igsparser import MessageParser as parser

def cb(data, index):
    pprint.pprint(vars(data))

if len(sys.argv) > 1:
    parser.parse(sys.argv[1], cb)
else:
    print('Usage: {} <iGS Message>'.format(sys.argv[0]))
    print('Example: bin/parse.py \'$GPRP,F973D9D36662,E7DAE08E6FC3,-87,02010612FF590080BC330100FFFFFFFF000004000000\'')
