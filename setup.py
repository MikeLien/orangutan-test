# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages

PACKAGE_VERSION = '0.1'

# dependencies
with open('requirements.txt') as f:
    deps = f.read().splitlines()

setup(name='orangutan-test',
      version=PACKAGE_VERSION,
      description='tools for executing orangutan',
      classifiers=[],
      keywords='mozilla',
      author='Mozilla Taipei QA team',
      author_email='tw-qa@mozilla.org',
      url='https://github.com/Mozilla-TWQA/orangutan-test',
      license='MPL',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points={"console_scripts": ["runcertsuite = certsuite:harness_main",
                                        "cert = certsuite:certcli",
                                        "webapirunner = webapi_tests.runner:main"]})
