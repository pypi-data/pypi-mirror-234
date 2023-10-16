# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sceptre',
 'sceptre.cli',
 'sceptre.config',
 'sceptre.diffing',
 'sceptre.hooks',
 'sceptre.plan',
 'sceptre.resolvers',
 'sceptre.template_handlers']

package_data = \
{'': ['*'], 'sceptre': ['stack_policies/*']}

install_requires = \
['boto3>=1.20.27,<2.0.0',
 'cfn-flip>=1.2.3,<2.0.0',
 'click>=7.0,<9.0',
 'colorama>=0.2.5,<0.4.4',
 'deepdiff>=5.5,<6.0',
 'deprecation>=2.0,<3.0',
 'jinja2>=3.0,<4.0',
 'jsonschema>=3.2,<3.3',
 'networkx>=2.6,<2.7',
 'packaging>=16.8,<22.0',
 'pyyaml>=6.0,<7.0',
 'sceptre-cmd-resolver>=2.0,<3.0',
 'sceptre-file-resolver>=1.0,<2.0']

extras_require = \
{'docs': ['sphinx>=1.6.5,<=5.1.1',
          'sphinx-click>=2.0.1,<4.0.0',
          'sphinx-rtd-theme==0.5.2',
          'sphinx-autodoc-typehints==1.19.2',
          'docutils<0.17'],
 'troposphere': ['troposphere>=4,<5']}

entry_points = \
{'console_scripts': ['sceptre = sceptre.cli:cli'],
 'sceptre.hooks': ['asg_scheduled_actions = '
                   'sceptre.hooks.asg_scaling_processes:ASGScalingProcesses',
                   'cmd = sceptre.hooks.cmd:Cmd'],
 'sceptre.resolvers': ['environment_variable = '
                       'sceptre.resolvers.environment_variable:EnvironmentVariable',
                       'file_contents = '
                       'sceptre.resolvers.file_contents:FileContents',
                       'join = sceptre.resolvers.join:Join',
                       'no_value = sceptre.resolvers.no_value:NoValue',
                       'select = sceptre.resolvers.select:Select',
                       'split = sceptre.resolvers.split:Split',
                       'stack_attr = sceptre.resolvers.stack_attr:StackAttr',
                       'stack_output = '
                       'sceptre.resolvers.stack_output:StackOutput',
                       'stack_output_external = '
                       'sceptre.resolvers.stack_output:StackOutputExternal',
                       'sub = sceptre.resolvers.sub:Sub'],
 'sceptre.template_handlers': ['file = sceptre.template_handlers.file:File',
                               'http = sceptre.template_handlers.http:Http',
                               's3 = sceptre.template_handlers.s3:S3']}

setup_kwargs = {
    'name': 'sceptre',
    'version': '4.3.0',
    'description': 'An AWS Cloud Provisioning Tool',
    'long_description': '# Sceptre\n\n[![CircleCI](https://img.shields.io/circleci/build/github/Sceptre/sceptre?logo=circleci)](https://app.circleci.com/pipelines/github/Sceptre)\n[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/sceptreorg/sceptre?logo=docker&sort=semver)](https://hub.docker.com/r/sceptreorg/sceptre)\n[![PyPI](https://img.shields.io/pypi/v/sceptre?logo=pypi)](https://pypi.org/project/sceptre/)\n[![PyPI - Status](https://img.shields.io/pypi/status/sceptre?logo=pypi)](https://pypi.org/project/sceptre/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sceptre?logo=pypi)](https://pypi.org/project/sceptre/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/sceptre?logo=pypi)](https://pypi.org/project/sceptre/)\n[![License](https://img.shields.io/pypi/l/sceptre?logo=apache)](https://github.com/Sceptre/sceptre/blob/main/LICENSE)\n\n## About\n\nSceptre is a tool to drive\n[AWS CloudFormation](https://aws.amazon.com/cloudformation). It automates the\nmundane, repetitive and error-prone tasks, enabling you to concentrate on\nbuilding better infrastructure.\n\n## Features\n\n- Code reuse by separating a Stack\'s template and its configuration\n- Support for templates written in JSON, YAML, Jinja2 or Python DSLs such as\n  Troposphere\n- Dependency resolution by passing of Stack outputs to parameters of dependent\n  Stacks\n- Stack Group support by bundling related Stacks into logical groups (e.g. dev\n  and prod)\n- Stack Group-level commands, such as creating multiple Stacks with a single\n  command\n- Fast, highly parallelised builds\n- Built in support for working with Stacks in multiple AWS accounts and regions\n- Infrastructure visibility with meta-operations such as Stack querying\n  protection\n- Support for inserting dynamic values in templates via customisable Resolvers\n- Support for running arbitrary code as Hooks before/after Stack builds\n\n## Benefits\n\n- Utilises cloud-native Infrastructure as Code engines (CloudFormation)\n- You do not need to manage state\n- Simple templates using popular templating syntax - Yaml & Jinja\n- Powerful flexibility using a mature programming language - Python\n- Easy to integrate as part of a CI/CD pipeline by using Hooks\n- Simple CLI and API\n- Unopinionated - Sceptre does not force a specific project structure\n\n## Install\n\n### Using pip\n\n`$ pip install sceptre`\n\nMore information on installing sceptre can be found in our\n[Installation Guide](https://docs.sceptre-project.org/latest/docs/install.html)\n\n### Using Docker Image\n\nView our [Docker repository](https://hub.docker.com/repositories/sceptreorg).\nImages available from version 2.0.0 onward.\n\nTo use our Docker image follow these instructions:\n\n1. Pull the image `docker pull sceptreorg/sceptre:[SCEPTRE_VERSION_NUMBER]` e.g.\n   `docker pull sceptreorg/sceptre:2.5.0`. Leave out the version number if you\n   wish to run `latest` or run `docker pull sceptreorg/sceptre:latest`.\n\n2. Run the image. You will need to mount the working directory where your\n   project resides to a directory called `project`. You will also need to mount\n   a volume with your AWS config to your docker container. E.g.\n\n`docker run -v $(pwd):/project -v /Users/me/.aws/:/root/.aws/:ro sceptreorg/sceptre:latest --help`\n\nIf you want to use a custom ENTRYPOINT simply amend the Docker command:\n\n`docker run -ti --entrypoint=\'\' sceptreorg/sceptre:latest sh`\n\nThe above command will enter you into the shell of the Docker container where\nyou can execute sceptre commands - useful for development.\n\nIf you have any other environment variables in your non-docker shell you will\nneed to pass these in on the Docker CLI using the `-e` flag. See Docker\ndocumentation on how to achieve this.\n\n## Example\n\nSceptre organises Stacks into "Stack Groups". Each Stack is represented by a\nYAML configuration file stored in a directory which represents the Stack Group.\nHere, we have two Stacks, `vpc` and `subnets`, in a Stack Group named `dev`:\n\n```sh\n$ tree\n.\n├── config\n│\xa0\xa0 └── dev\n│\xa0\xa0      ├── config.yaml\n│\xa0\xa0      ├── subnets.yaml\n│\xa0\xa0      └── vpc.yaml\n└── templates\n    ├── subnets.py\n    └── vpc.py\n```\n\nWe can create a Stack with the `create` command. This `vpc` Stack contains a\nVPC.\n\n```sh\n$ sceptre create dev/vpc.yaml\n\ndev/vpc - Creating stack dev/vpc\nVirtualPrivateCloud AWS::EC2::VPC CREATE_IN_PROGRESS\ndev/vpc VirtualPrivateCloud AWS::EC2::VPC CREATE_COMPLETE\ndev/vpc sceptre-demo-dev-vpc AWS::CloudFormation::Stack CREATE_COMPLETE\n```\n\nThe `subnets` Stack contains a subnet which must be created in the VPC. To do\nthis, we need to pass the VPC ID, which is exposed as a Stack output of the\n`vpc` Stack, to a parameter of the `subnets` Stack. Sceptre automatically\nresolves this dependency for us.\n\n```sh\n$ sceptre create dev/subnets.yaml\ndev/subnets - Creating stack\ndev/subnets Subnet AWS::EC2::Subnet CREATE_IN_PROGRESS\ndev/subnets Subnet AWS::EC2::Subnet CREATE_COMPLETE\ndev/subnets sceptre-demo-dev-subnets AWS::CloudFormation::Stack CREATE_COMPLETE\n```\n\nSceptre implements meta-operations, which allow us to find out information about\nour Stacks:\n\n```sh\n$ sceptre list resources dev/subnets.yaml\n\n- LogicalResourceId: Subnet\n  PhysicalResourceId: subnet-445e6e32\n  dev/vpc:\n- LogicalResourceId: VirtualPrivateCloud\n  PhysicalResourceId: vpc-c4715da0\n```\n\nSceptre provides Stack Group level commands. This one deletes the whole `dev`\nStack Group. The subnet exists within the vpc, so it must be deleted first.\nSceptre handles this automatically:\n\n```sh\n$ sceptre delete dev\n\nDeleting stack\ndev/subnets Subnet AWS::EC2::Subnet DELETE_IN_PROGRESS\ndev/subnets - Stack deleted\ndev/vpc Deleting stack\ndev/vpc VirtualPrivateCloud AWS::EC2::VPC DELETE_IN_PROGRESS\ndev/vpc - Stack deleted\n```\n\n> Note: Deleting Stacks will _only_ delete a given Stack, or the Stacks that are\n> directly in a given StackGroup. By default Stack dependencies that are\n> external to the StackGroup are not deleted.\n\nSceptre can also handle cross Stack Group dependencies, take the following\nexample project:\n\n```sh\n$ tree\n.\n├── config\n│\xa0\xa0 ├── dev\n│\xa0\xa0 │\xa0\xa0 ├── network\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 └── vpc.yaml\n│\xa0\xa0 │\xa0\xa0 ├── users\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 └── iam.yaml\n│\xa0\xa0 │\xa0\xa0 ├── compute\n│\xa0\xa0 │\xa0\xa0 │\xa0\xa0 └── ec2.yaml\n│\xa0\xa0 │\xa0\xa0 └── config.yaml\n│\xa0\xa0 └── staging\n│\xa0\xa0     └── eu\n│\xa0\xa0         ├── config.yaml\n│\xa0\xa0         └── stack.yaml\n├── hooks\n│\xa0\xa0 └── stack.py\n├── templates\n│\xa0\xa0 ├── network.json\n│\xa0\xa0 ├── iam.json\n│\xa0\xa0 ├── ec2.json\n│\xa0\xa0 └── stack.json\n└── vars\n    ├── dev.yaml\n    └── staging.yaml\n```\n\nIn this project `staging/eu/stack.yaml` has a dependency on the output of\n`dev/users/iam.yaml`. If you wanted to create the Stack `staging/eu/stack.yaml`,\nSceptre will resolve all of it\'s dependencies, including `dev/users/iam.yaml`,\nbefore attempting to create the Stack.\n\n## Usage\n\nSceptre can be used from the CLI, or imported as a Python package.\n\n## CLI\n\n```text\nUsage: sceptre [OPTIONS] COMMAND [ARGS]...\n\n  Sceptre is a tool to manage your cloud native infrastructure deployments.\n\nOptions:\n  --version                  Show the version and exit.\n  --debug                    Turn on debug logging.\n  --dir TEXT                 Specify sceptre directory.\n  --output [text|yaml|json]  The formatting style for command output.\n  --no-colour                Turn off output colouring.\n  --var TEXT                 A variable to replace the value of an item in\n                             config file.\n  --var-file FILENAME        A YAML file of variables to replace the values\n                             of items in config files.\n  --ignore-dependencies      Ignore dependencies when executing command.\n  --merge-vars               Merge variables from successive --vars and var\n                             files.\n  --help                     Show this message and exit.\n\nCommands:\n  create         Creates a stack or a change set.\n  delete         Deletes a stack or a change set.\n  describe       Commands for describing attributes of stacks.\n  estimate-cost  Estimates the cost of the template.\n  execute        Executes a Change Set.\n  generate       Prints the template.\n  launch         Launch a Stack or StackGroup.\n  list           Commands for listing attributes of stacks.\n  new            Commands for initialising Sceptre projects.\n  set-policy     Sets Stack policy.\n  status         Print status of stack or stack_group.\n  update         Update a stack.\n  validate       Validates the template.\n```\n\n## Python\n\nUsing Sceptre as a Python module is very straightforward. You need to create a\nSceptreContext, which tells Sceptre where your project path is and which path\nyou want to execute on, we call this the "command path".\n\nAfter you have created a SceptreContext you need to pass this into a\nSceptrePlan. On instantiation the SceptrePlan will handle all the required steps\nto make sure the action you wish to take on the command path are resolved.\n\nAfter you have instantiated a SceptrePlan you can access all the actions you can\ntake on a Stack, such as `validate()`, `launch()`, `list()` and `delete()`.\n\n```python\nfrom sceptre.context import SceptreContext\nfrom sceptre.plan.plan import SceptrePlan\n\ncontext = SceptreContext("/path/to/project", "command_path")\nplan = SceptrePlan(context)\nplan.launch()\n```\n\nFull API reference documentation can be found in the\n[Documentation](https://docs.sceptre-project.org/)\n\n## Tutorial and Documentation\n\n- [Get Started](https://docs.sceptre-project.org/latest/docs/get_started.html)\n- [Documentation](https://docs.sceptre-project.org/)\n\n## Communication\n\nSceptre community discussions happen in the #sceptre chanel in the\n[og-aws Slack](https://github.com/open-guides/og-aws).  To join click\non <http://slackhatesthe.cloud/> to create an account and join the\n#sceptre channel.\n\nFollow the [SceptreOrg Twitter account](https://twitter.com/SceptreOrg) to get announcements on the latest releases.\n\n## Contributing\n\nSee our [Contributing Guide](CONTRIBUTING.md)\n\n## Sponsors\n\n[![Sage Bionetworks](sponsors/sage_bionetworks_logo.png "Sage Bionetworks")](https://sagebionetworks.org)\n\n[![GoDaddy](sponsors/godaddy_logo.png "GoDaddy")](https://www.godaddy.com)\n\n[![Cloudreach](sponsors/cloudreach_logo.png "Cloudreach")](https://www.cloudreach.com)\n',
    'author': 'Sceptre',
    'author_email': 'sceptreorg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Sceptre/sceptre',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
