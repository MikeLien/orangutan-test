# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import time
from argparser import Parser

class LogCollector(object):

    def __init__(self, device, option):
        self.option = option
        self.strTime = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.logFolder = 'logs/'+device+'_'+self.strTime
        if not os.path.exists(self.logFolder):
            os.makedirs(self.logFolder)
        pass
        ## TODO: add timer for pull logs regularly

    def log_b2g_ps(self, attach):
        os.system('adb shell b2g-ps -t -p -P --oom > b2g-ps_' + attach + '.log')

    def log_b2g_info(self, attach):
        os.system('adb shell b2g-info -t > b2g-info_' + attach + '.log')

    def log_b2g_proprank(self, attach):
        os.system('adb shell b2g-procrank --oom > b2g-procrank_' + attach + '.log')

    def log_dumpstate(self, attach):
        os.system('adb shell dumpstate > dumpstate_' + attach + '.log')

    def log_crash_report(self):
        os.system('adb pull /data/b2g/Crash\ Reports' + self.logFolder)

    def log_logcat(self, attach):
        os.system('adb shell logcat -v threadtime -d > logcat_' + attach + '.log')

    def log_dmesg(self, attach):
        os.system('adb shell dmesg > dmesg_' + attach + '.log')

    def log_get_event(self, attach):
        os.system('adb shell getevent -S > getevent_' + attach + '.log')

    def getLogs(self):
        curTime = time.strftime('%m%d%H%M%S', time.localtime())
        if self.option['b2g-ps']:
            self.log_b2g_ps(curTime)
        if self.option['b2g-info']:
            self.log_b2g_info(curTime)
        if self.option['b2g-procrank']:
            self.log_b2g_proprank(curTime)
        if self.option['dumpstate']:
            self.log_dumpstate(curTime)
        if self.option['crash-report']:
            self.log_crash_report()
        if self.option['logcat']:
            self.log_logcat(curTime)
        if self.option['dmesg']:
            self.log_dmesg(curTime)
        if self.option['get-event']:
            self.log_get_event(curTime)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        options = Parser.parser(sys.argv[1:])
        print os.getcwd()
        if 'config' in options:
            config = {}
            with open(options.config) as f:
                config = eval(f.read())
            log = LogCollector(config['device_name'], config['logs'])
