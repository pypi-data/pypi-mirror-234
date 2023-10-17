# Copyright (c) 2017-2020 Cloudify Platform Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
import pathlib
import setuptools


def get_version():
    current_dir = pathlib.Path(__file__).parent.resolve()

    with open(os.path.join(current_dir, 'cloudify_common_sdk/__version__.py'),
              'r') as outfile:
        var = outfile.read()
        return re.search(r'\d+.\d+.\d+', var).group()


setuptools.setup(
    name='cloudify-utilities-plugins-sdk',
    version=get_version(),
    author='Cloudify Platform Ltd.',
    author_email='hello@cloudify.co',
    description='Utilities SDK for extending Cloudify',
    long_description="""
        # Cloudify Utilities SDK

        Utilities SDK for extending Cloudify features.
    """,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    url="https://github.com/cloudify-incubator/cloudify-utilities-plugins-sdk",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3==1.23.10',
        'cloudify-common>=4.5.5',
        'paramiko>=2.7.1',  # terminal
        "Jinja2>=2.7.2",  # terminal
        "pycdlib",  # cdrom image
        'pyyaml>=5.4.1',  # cloudinit and rest
        'requests>=2.7.0,<3.0.0',
        'xmltodict',   # rest
        "gitdb>=0.6.4",  # shared download resource
        "GitPython",  # shared download resource
        "cfy-lint>=0.0.34",
        'psutil',
        'packaging>=17.1,<=21.3',
        'kubernetes==v26.1.0',
        'google-auth==2.15.0',
        'msrestazure==0.6.4',
        'azure-identity',
        'azure-mgmt-containerservice==17.0.0',
    ]
)
