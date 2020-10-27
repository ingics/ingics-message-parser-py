#!/usr/bin/env python

import sys
import pprint
from igsparser import MsdParser as parser

if len(sys.argv) > 1:
    pprint.pprint(vars(parser.parse(sys.argv[1])))
else:
    print('Usage: {} <Beacon Payload>'.format(sys.argv[0]))
    print('Example: {} \'590080BC330100FFFFFFFF000004000000\''.format(sys.argv[0]))
