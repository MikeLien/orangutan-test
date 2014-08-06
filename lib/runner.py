# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
from datetime import datetime, timedelta

from env_setup import DeviceOperator

class Runner(object):

    def __init__(self, options, time):
        self.options = options
        self.startTime = datetime.now()

    def load_config(self, config_repo):
        config = {}
        with open(config_repo) as f:
            self.config = eval(f.read())
        return config

    def getScripts(self, script_repo):
        scripts = []
        for dir_path, dir_names, dir_files in os.walk(script_repo):
            for f in dir_files:
                scripts.extend(f)
        return scripts

    def runner(self):
        self.config = load_config(options['config'])

        ## TODO: check if need to generate scripts

        scripts = getScripts(self.config['script_repo'])

        self.device = DeviceOperator(self.config['work_dir'])
        self.device.pushBinary(self.config['orngutan'], self.config['work_dir'])
        self.device.pushScript(self.config['scripts_repo'], self.config['work_dir'])

        # Time check

        while datetime.now() < self.startTime + timedelta(hours=self.config['execution_time']):
            # execution
            ## TODO: create another process to monitor status
            continue

        ## TODO: Force close the subprocess

        ## TODO: Collect log

## TODO: Main for testing purpose

if __name__ == '__main__':
    pass
