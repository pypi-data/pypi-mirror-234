# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['majormode',
 'majormode.perseus',
 'majormode.perseus.agent',
 'majormode.perseus.bootstrap',
 'majormode.perseus.service',
 'majormode.perseus.service.account',
 'majormode.perseus.service.account.test',
 'majormode.perseus.service.application',
 'majormode.perseus.service.application.test',
 'majormode.perseus.service.area',
 'majormode.perseus.service.area.data.vietnam',
 'majormode.perseus.service.area.script',
 'majormode.perseus.service.notification',
 'majormode.perseus.service.notification.agent',
 'majormode.perseus.service.status',
 'majormode.perseus.service.team',
 'majormode.perseus.service.team.agent',
 'majormode.perseus.service.team.test',
 'majormode.perseus.service.version',
 'majormode.perseus.service.version.test']

package_data = \
{'': ['*'],
 'majormode.perseus': ['db/*'],
 'majormode.perseus.service.account': ['db/*', 'template/*'],
 'majormode.perseus.service.application': ['db/*'],
 'majormode.perseus.service.area': ['db/*'],
 'majormode.perseus.service.notification': ['db/*'],
 'majormode.perseus.service.status': ['doc/api/*'],
 'majormode.perseus.service.team': ['db/*', 'template/*'],
 'majormode.perseus.service.version': ['doc/api/*']}

install_requires = \
['perseus-core-library>=1.19,<2.0',
 'perseus-getenv-library>=1.0,<2.0',
 'perseus-microrm-library>=1.3,<2.0',
 'pillow>=10.0,<11.0',
 'prosoponym>=1.0.7,<2.0.0',
 'psutil>=5.9.4,<6.0.0',
 'pymemcache>=4.0.0,<5.0.0',
 'setuptools>=68.2.2,<69.0.0',
 'tornado>=6.2,<7.0']

setup_kwargs = {
    'name': 'perseus-restful-api-framework',
    'version': '1.27.4',
    'description': 'Python server framework for quickly building RESTful APIs with minimal effort',
    'long_description': '# Perseus: RESTful API Server Framework\n\nPerseus is a Python framework for quickly building RESTful API servers with minimal effort.\n\nPerseus provides an initial set of core services that supports the following features:\n\n- Client application registration with API keys generation\n- Client application access control with RESTful request signature\n- Client application and RESTful API server version compatibility check\n- User authentication and session management\n- Team/group management\n- RESTful request logging with data sensitiveness support\n- RESTful service automatic discovery\n- HTTP request query parameters & body JSON message automatically parsing (depending on the HTTP method used) with data type check and conversion\n\nPerseus is based on [Tornado](https://www.tornadoweb.org/) for handling client network connection.\n\n## RESTful API Request Handler\n\n```python\nfrom majormode.perseus.service.base_http_handler import HttpRequest\nfrom majormode.perseus.service.base_http_handler import HttpRequestHandler\nfrom majormode.perseus.service.base_http_handler import http_request\n\nimport AttendantService\n\n\nclass AttendantServiceHttpRequestHandler(HttpRequestHandler):\n    @http_request(r\'^/attendant/session$\',\n                  http_method=HttpRequest.HttpMethod.POST,\n                  authentication_required=False,\n                  sensitive_data=True,\n                  signature_required=False)\n    def sign_in(self, request):\n        email_address = request.get_argument(\n            \'email_address\',\n            data_type=HttpRequest.ArgumentDataType.email_address,\n            is_required=True)\n\n        password = request.get_argument(\n            \'password\',\n            data_type=HttpRequest.ArgumentDataType.string,\n            is_required=True)\n\n        return AttendantService().sign_in(request.app_id, email_address, password)\n```\n\n## Configure the environment variables\n\n```env\n# Copyright (C) 2021 Majormode.  All rights reserved.\n#\n# Permission is hereby granted, free of charge, to any person obtaining\n# a copy of this software and associated documentation files (the\n# "Software"), to deal in the Software without restriction, including\n# without limitation the rights to use, copy, modify, merge, publish,\n# distribute, sublicense, and/or sell copies of the Software, and to\n# permit persons to whom the Software is furnished to do so, subject to\n# the following conditions:\n#\n# The above copyright notice and this permission notice shall be\n# included in all copies or substantial portions of the Software.\n#\n# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\n# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\n# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\n# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY\n# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,\n# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE\n# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n# Connection properties of the RESTful API server instances.  Defaults\n# to 127.0.0.1:8081.\nAPI_SERVER_HOSTNAME=127.0.0.1\nAPI_SERVER_PORTS=\n\n# Root path of the Network File System (NFS) -- referring to the\n# distributed file system (not the protocol) -- where the Content\n# Delivery Network (CDN) files are stored into, such as avatars, etc.\nCDN_NFS_ROOT_PATH=\n\n# Hostname of the Content Delivery Network (CDN) server that hosts media\n# files such as avatars, etc.\nCDN_URL_HOSTNAME=\n\n# Environment stage of the API server instances.  Possible values are:\n#\n# - dev\n# - int\n# - staging\n# - prod\n#\n# Defaults to `dev`.\nENVIRONMENT_STAGE=\n\n# Connection properties to a Memcached server (a distributed memory\n# object caching system).  Defaults to 127.0.0.1:11211.\nMEMCACHED_HOSTNAME = \'127.0.0.1\'\nMEMCACHED_PORT = 11211\n\n# Threshold for the logger to level.  Logging messages which are less\n# severe than the specified level will be ignored; logging messages\n# which have this severity level or higher will be emitted.  Possible\n# values are:\n#\n# - debug\n# - info\n# - warning\n# - error\n# - critical\n#\n# Default to \'debug\'.\nLOGGING_LEVEL=\n\n# Environment variables to select default parameter values to connect\n# to PostgreSQL Relational Database Management System.\nPG_HOSTNAME=localhost\nPG_PORT=5432\nPG_DATABASE_NAME=\nPG_USERNAME=\nPG_PASSWORD=\n```\n\n## Run the RESTful API Server Processes\n\n```bash\n$ fab start --port=65180,65181,...\n```\n\nHashtags/Topics: `#perseus` `#restful` `#api` `#server` `#framework` `#python`\n',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel.caune@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/majormode/perseus-restful-api-server-framework',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
