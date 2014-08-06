# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import time
from argparser import Parser

class LogCollector(object):

    def __init__(self, device):
        self.strTime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.logFolder = 'logs/'+device+'_'+self.strTime
        if not os.path.exists(self.logFolder):
            os.makedirs(self.logFolder)
        pass



if __name__ == '__main__':
    if len(sys.argv) > 1:
        options = Parser.parser(sys.argv[1:])
        print os.getcwd()
        if 'config' in options:
            config = {}
            with open(options.config) as f:
                config = eval(f.read())
            log = LogCollector(config['device_name'])
