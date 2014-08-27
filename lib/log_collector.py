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
        self.logFolder = 'logs/'+device+'_'+self.strTime+'/'
        if not os.path.exists(self.logFolder):
            os.makedirs(self.logFolder)
        pass
        ## TODO: add timer for pull logs regularly

    def log_b2g_ps(self, attach):
        os.system('adb shell b2g-ps -t -p -P --oom > ' + self.logFolder + attach + '/b2g-ps.log')

    def log_b2g_info(self, attach):
        os.system('adb shell b2g-info -t > ' + self.logFolder + attach + '/b2g-info.log')

    def log_b2g_proprank(self, attach):
        os.system('adb shell b2g-procrank --oom > ' + self.logFolder + attach + '/b2g-procrank.log')

    def log_dumpstate(self, attach):
        os.system('adb shell dumpstate > ' + self.logFolder + attach + '/dumpstate.log')

    def log_logcat(self, attach):
        os.system('adb shell logcat -v threadtime -d > ' + self.logFolder + attach + '/logcat.log')

    def log_dmesg(self, attach):
        os.system('adb shell dmesg > ' + self.logFolder + attach + '/dmesg.log')

    def log_get_event(self, attach):
        os.system('adb shell getevent -S > ' + self.logFolder + attach + '/getevent.log')

    def log_crash_report(self):
        os.system('adb pull /data/b2g/mozilla/Crash\ Reports ' + self.logFolder)

    def getLogs(self):
        curTime = time.strftime('%m%d%H%M%S', time.localtime())
        os.makedirs(self.logFolder+curTime)
        if self.option['b2g-ps']:
            self.log_b2g_ps(curTime)
        if self.option['b2g-info']:
            self.log_b2g_info(curTime)
        if self.option['b2g-procrank']:
            self.log_b2g_proprank(curTime)
        if self.option['dumpstate']:
            self.log_dumpstate(curTime)
        if self.option['logcat']:
            self.log_logcat(curTime)
        if self.option['dmesg']:
            self.log_dmesg(curTime)
        if self.option['get-event']:
            self.log_get_event(curTime)

    def getCrashReport(self):
        if self.option['crash-report']:
            self.log_crash_report()

    def gen_report(self):
        report = open(self.logFolder+'report.html', 'w')
        for dir_path, dir_names, dir_files in os.walk(self.logFolder):
            for f in dir_files:
                if dir_names:
                    report.write('File: <a href="%s">%s</a><br>\n' % (f, f))
                else:
                    base = os.path.basename(dir_path)
                    report.write('File: <a href="%s/%s">%s/%s</a><br>\n' % (base, f, base, f))
        report.close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        options = Parser.parser(sys.argv[1:])
        if 'config' in options:
            config = {}
            with open(options.config) as f:
                config = eval(f.read())
            log = LogCollector(config['device_name'], config['logs'])
            log.getLogs()
            log.gen_report()
