# PyFake-API-Server-Surveillance

[![PyPI](https://img.shields.io/pypi/v/fake-api-server-surveillance?color=%23099cec&amp;label=PyPI&amp;logo=pypi&amp;logoColor=white)](https://pypi.org/project/fake-api-server-surveillance)
[![Release](https://img.shields.io/github/release/Chisanan232/PyFake-API-Server-Surveillance.svg?label=Release&logo=github)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/releases)
[![CI](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/ci.yaml/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/Chisanan232/PyFake-API-Server-Surveillance/graph/badge.svg?token=GJYBfInkzX)](https://codecov.io/gh/Chisanan232/PyFake-API-Server-Surveillance)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Chisanan232/PyFake-API-Server-Surveillance/master.svg)](https://results.pre-commit.ci/latest/github/Chisanan232/PyFake-API-Server-Surveillance/master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Chisanan232_PyFake-API-Server-Surveillance&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Chisanan232_PyFake-API-Server-Surveillance)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🤖 A CI tool for monitoring a specific API end points and keeping fake API server always up-to-date.

[Overview](#overview) | [Python versions support](#Python-versions-support) | [Quickly Start](#quickly-start) | [Documentation](#documentation)
<hr>


## Overview

Do you ever have experience about Back-End side does something change on the sly, but they don't sync the change with
Font-End side and cause it be broken? Even you may have tool which could fake an API server, but you still need to update
it manually (if you know the change). This tool Fake-API-Server-Surveillance targets to resolve this issue by everyone
could automate the process about monitoring and updating the fake server which be built by [**Fake-API-Server**].

[**Fake-API-Server**]: https://github.com/Chisanan232/PyFake-API-Server

## Python versions support

The code base of **_PyFake-API-Server-Surveillance_** depends on another library [**Fake-API-Server**].
So it also only supports Python 3.8 version up.

[![Supported Versions](https://img.shields.io/pypi/pyversions/fake-api-server-surveillance.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/fake-api-server-surveillance)


## Quickly Start

Here section would lead you quickly start to set up your first automation with **_PyFake-API-Server-Surveillance_** for
keep monitoring Back-End side and keep the fake server always be the latest version under surveillance easily.

In basically, it has 3 steps: prepare your fake server, configure **_PyFake-API-Server-Surveillance_** and set action for
GitHub Action.

* [Prepare Fake-API-Server](#prepare-fake-api-server)
* [Configure](#configure-fake-api-server-surveillance)
* [Set action](#configure-github-action-ci-setting)

### Prepare **Fake-API-Server**

First of all, this tool only for [**Fake-API-Server**]. So you must have a GitHub project which records the details
configuration of [**Fake-API-Server**].

### Configure **Fake-API-Server-Surveillance**

The detail settings of **Fake-API-Server-Surveillance** would be configured by YAML file. Here provide a sample
configuration:

```yaml
api-doc-url: 'http://127.0.0.1:1111/swagger-api'
fake-api-server:
  server-type: rest-server
  subcmd:
    pull:
      args:
        - --config-path=./api.yaml
        - --include-template-config
        - --base-file-path=./
        - --base-url=/test/v1
        - --divide-api
git-info:
  repo: 'TestUser/Back-End-Project'
  commit:
    author:
      name: 'TestUser'
      email: 'test@gmail.com'
    message: ' 🧪 test commit message.'
github-info:
  pull-request:
    title: '🤖 Update API configuration'
    body: '🚧 test content ...'
    draft: true
    labels:
      - '🤖 update by bot'
```

### Configure GitHub Action CI setting

Add a single CI workflow which only for monitoring Back-End side change as a scheduler:

```yaml
name: Monitor Back-End API interface

on:
  # In generally, it's reasonable that using schedule feature of GitHub Action to monitor the Back-End side API change..
  schedule:
    - cron: "15 4,5 * * *"   # <=== Change this value

permissions:
  contents: write  # Need this to push commits
  pull-requests: write  # Need this to open pull request

jobs:
  monitor-and-update:
    runs-on: ubuntu-latest
    steps:
      # Clone the fake-api-server config
      - name: Clone project
        uses: actions/checkout@v4

      # Monitor and update the config if it needs by opening pull request
      - name: Run Fake-API-Server-Surveillance
        uses: actions/PyFake-API-Server-Surveillance@v0.2.0
        with:
          config-path: <your fake-api-server-surveillance config>
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Congratulation! Now, you could just have a coffee and do anything you want to do without being worry about the fake
server be expired. The CI workflow would be the trustworthy partner to help you keep monitoring and updating the fake
server if it needs without missing any change.


## Documentation

[![documentation](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/documentation.yaml/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/documentation.yaml)

The [documentation](https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/) contains more details, demonstrations and anything you need about **_PyFake-API-Server-Surveillance_**.

* [Getting start](https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/getting-started/version-requirements/) helps you start to prepare environment, install dependencies and configure the detail settings with explanation in detail.
    * How to [configure the details of surveillance](https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/getting-started/configure-your-api/)?
    * I have configuration right now. How can I [set up a monitoring automation by CI](https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/getting-started/setup-web-server/)?
* Want to learn more how to use it?
    * Want to know more [detail settings](https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/configure-references/config-basic-info/) to customize surveillance?
* About the [release notes](https://chisanan232.github.io/PyFake-API-Server-Surveillance/latest/release_note/).


## Coding style and following rules

**_PyFake-API-Server-Surveillance_** follows coding styles **_black_** and **_PyLint_** to control code quality.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)


## Downloading state

**_PyFake-API-Server-Surveillance_** still a young open source which keep growing. Here's its download state:

[![Downloads](https://pepy.tech/badge/fake-api-server-surveillance)](https://pepy.tech/project/fake-api-server-surveillance)
[![Downloads](https://pepy.tech/badge/fake-api-server-surveillance/month)](https://pepy.tech/project/fake-api-server-surveillance)


## License

[MIT License](./LICENSE)
