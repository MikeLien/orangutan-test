# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import sys


class Parser(object):

    @staticmethod
    def pvtArgParse(input):
        parser = argparse.ArgumentParser(description='Orangutan Test Tool by TWQA')
        parser.add_argument('--config', help='repo of config file')
        parser.add_argument('--output-folder', help='repo for saving logs')
        parser.add_argument('--gen-scripts-amount', help='the amount of scripts')
        parser.add_argument('--gen-scripts-steps', help='the steps in a script')
        parser.add_argument('--gen-scripts-output', help='the repo for scripts')
        options = parser.parse_args(input)
        return options

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print Parser.pvtArgParse(sys.argv[1:])
    else:
        testSample = ["--config", "testConfig"]
        print Parser.pvtArgParse(testSample)
