#!/usr/bin/env python
#
# Copyright 2024 Acme Gating, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import configparser
import yaml


def make_project(project_name):
    return {
        'project': {
            'name': project_name,
            'templates': ['submodule-jobs'],
        }
    }


def main():
    output = []
    gitmodules = configparser.ConfigParser()
    gitmodules.read('.gitmodules')
    for section in gitmodules.sections():
        if not section.startswith('submodule'):
            continue
        submodule = gitmodules[section]
        url = submodule['url']
        if not url.startswith("../"):
            raise Exception(f"{section} URL does not have relative path: {url}")
        branch = submodule.get('branch')
        if branch and branch != '.':
            raise Exception(f"{section} branch is not '.'")
        project_name = url[3:]
        output.append(make_project(project_name))
    with open('zuul.d/submodules.yaml', 'w') as f:
        yaml.dump(output, f)


if __name__ == "__main__":
    main()
