# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import mozdevice
import os

class DeviceOperator(object):

    def __init__(self, work_dir):
        self.device = mozdevice.DeviceManagerADB()
        self.work_dir = work_dir
        self.device.mkDir(work_dir)

    def pushBinary(self, local_file):
        remote_file = os.path.join(self.work_dir, os.path.basename(local_file))
        self.device.pushFile(local_file, remote_file)

    def pushScript(self, local_repo):
        self.device.pushDir(local_repo, self.work_dir)

    def getLog(self, local_repo):
        # download logs to local repo
        self.device.moveFile(local_repo)

    def getCrashReport(self, local_repo):
        self.device.getDirectory("/data/b2g/mozilla/Crash\ Reports/", local_repo)
