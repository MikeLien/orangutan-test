# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import pdb

import os
import sys
import subprocess
import logging
import signal
from datetime import datetime, timedelta
from device_operator import DeviceOperator
from argparser import Parser
from log_collector import LogCollector
from gen_randomsc import GenRandomSC 

FORMAT = '%(asctime)-15s OrangutanTool %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger( __name__ )

class Runner(object):

    def __init__(self, config, options):
        self.options = options
        self.config = config
        self.scripts = self.getScripts(self.config['script_repo'])

        self.logCollector = LogCollector(self.config['device_name'], self.config['logs'])

        self.forceStopped = False

        # generate scripts
        self.genScript = GenRandomSC().gen_random_sc()
        
        # Push binary and scripts onto device
        logger.info("Orangutan binary: %s" % self.config['orangutan'])
        logger.info("Orangutan work directory: %s" % self.config['work_dir'])

        self.device = DeviceOperator(self.config['work_dir'])
        self.device.pushBinary(self.config['orangutan'])
        self.device.pushScript(self.config['script_repo'])
        
    def getScripts(self, script_repo):
        scripts = []
        for dir_path, dir_names, dir_files in os.walk(script_repo):
            for f in dir_files:
                scripts.extend(f)
        return scripts

    def run(self):
        orng = os.path.join(self.config['work_dir'], self.config['orangutan'])
        command = ['adb', 'shell', orng, self.config['event'], 'script_place_holder']

        for script in self.scripts:
            if not self.forceStopped:
                logger.info("Trigger Script: " + script)
                command[-1] = os.path.join(self.config['work_dir'], script)
                self.currentProcess = subprocess.Popen(command)

    def stopRunning(self):
        self.forceStopped = True
        self.currentProcess.terminate()
        logger.info("Force Stop")

    def collectLog(self):
        self.logCollector.getLogs()
        
def load_config(config_repo):
    logger.info("Load config from %s" % config_repo)
    config = {}
    with open(config_repo) as f:
        config = eval(f.read())
    logger.debug("config %s" % config)
    return config

def main(argv):
    options = Parser.parser(argv)
    config = load_config(options.config)

    startTime = datetime.now()
    logger.info("Starting " + startTime.strftime("%Y/%m/%d %H:%M:%S"))
    runningTime = timedelta(hours=config['execution_time']).total_seconds()
    logger.info("Running Time: %d " % runningTime)

    runner = Runner(config, options)
    signal.signal(signal.SIGALRM, runner.stopRunning)
    signal.alarm(int(runningTime))

    logger.info("Orangutan Test is Done at " + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        Parser.parser(["-h"])
