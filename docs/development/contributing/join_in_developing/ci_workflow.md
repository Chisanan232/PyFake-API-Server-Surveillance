# CI workflow

This project has multiple CI workflows to let developers could do the best at focusing on writing code, doesn't get 
distracted by other chores. And some CI workflows could guarantee the project code quality, validation of feature could 
work finely, etc.

Here records all the CI workflows of this project runs.

## Pre-Commit CI

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Chisanan232/PyFake-API-Server-Surveillance/master.svg)](https://results.pre-commit.ci/latest/github/Chisanan232/PyFake-API-Server-Surveillance/master)

* CI state

    Here's the state of [workflow](https://results.pre-commit.ci/latest/github/Chisanan232/PyFake-API-Server-Surveillance/master).

* Trigger points

    Every git commit. This workflow always runs before each CI workflows.

* Target doing

    Doing some checking of Python code and YAML format configuration.

## Source code by PR bot CI

[![Bot CI](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/bot-ci.yaml/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/bot-ci.yaml)

* CI state

    Here's the state of [workflow](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/bot-ci.yaml).

* Trigger points

    When any PRs be opened by [GitHub dependency bot](https://docs.github.com/en/code-security/dependabot) and also be 
    tagged by tag ``dependencies``, it would trigger this CI workflow.

* Target doing

    Run all tests includes unit tests, integration tests and system tests to guarantee all the project features work 
    finely with the dependency upgrading.

!!! note "Only run tests"

    This CI workflow won't upload test coverage report and also won't trigger
    SonarQube scan of code quality.

![pr bot ci]

[pr bot ci]: ../../../_images/development/contributing/join_in_developing/bot_pr_ci.png

## Source code CI

[![CI](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/ci.yaml/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/ci.yaml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Chisanan232_PyFake-API-Server-Surveillance&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Chisanan232_PyFake-API-Server-Surveillance)
[![codecov](https://codecov.io/gh/Chisanan232/PyFake-API-Server-Surveillance/graph/badge.svg?token=GJYBfInkzX)](https://codecov.io/gh/Chisanan232/PyFake-API-Server-Surveillance)

* CI state
* 

    Here's the state of [workflow](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/ci.yaml).

* Trigger points

    General PR which be opened in developer branch as naming format ``develop/**`` and also ignore some specific files 
    or directories like CI workflow folder, documentation folder, etc. And also the PR doesn't have tag ``dependencies``.

* Target doing

    It would run all [tests] ([unit test], [integration test] and [system test]) and record all [test coverage reports] 
    of each test with different runtime environment OS and Python version. It would also trigger [SonarQube] scan to check
    coding style (this would also be checked in [pre-commit CI]), security or something details about code quality. And 
    finally, it would try to test to run the command line ``mock`` to ensure it should work finely.

[tests]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/tree/master/test
[unit test]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/tree/master/test/unit_test
[integration test]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/tree/master/test/integration_test
[system test]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/tree/master/test/system_test

[test coverage reports]: https://app.codecov.io/gh/Chisanan232/PyFake-API-Server-Surveillance
[SonarQube]: https://sonarcloud.io/summary/new_code?id=Chisanan232_PyFake-API-Server-Surveillance
[pre-commit CI]: https://results.pre-commit.ci/run/github/901659765/1744171173.8RV_66z2TtCE36bs0f5Syw

![source code ci]

[source code ci]: ../../../_images/development/contributing/join_in_developing/source_code_ci.png

## CD

[![CD](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/cd.yaml/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/cd.yaml)

* CI state

    Here's the state of [workflow](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/cd.yaml).

* Trigger points

    Only occur version info change in the source code module ``__pkg_info__``.

* Target doing

    It would create new git tag and git release info. After tag and release building, it would build the source code as 
    Python package and push it to [PyPI] service.

[PyPI]: https://pypi.org/project/fake-api-server-surveillance/

![cd]

[cd]: ../../../_images/development/contributing/join_in_developing/cd.png

!!! question "How to trigger the deployment workflow exactly?"

    In the Python projects which be builded by [Chisanan232], it
    must have a module about the Python package info. And it has
    software version info ``__version__``. It has only one way to
    trigger the deployment workflow: update the version info.

    In package info [source code]:

    ```python
    ... # other code

    __version__ = "0.2.0"    # update this version info to trigger the CD workflow

    ... # other code
    ```

[Chisanan232]: https://github.com/Chisanan232
[source code]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/blob/master/pymock_server/__pkg_info__.py#L17

## Docker CI

[![docker](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/docker.yaml/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/docker.yaml)

* CI state

    Here's the state of [workflow](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/docker.yaml).

* Trigger points

    Same as CI workflow [CD](#cd).

* Target doing

    It would build the Docker image and push it to [DockerHub].

[DockerHub]: https://hub.docker.com/repository/docker/chisanan232/pyfake-api-server-surveillance/general

## Documentation CI

[![documentation](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/documentation.yaml/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/documentation.yaml)
[![pages-build-deployment](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/pages/pages-build-deployment)

* CI state

    Here's the state of workflows.

    * Build versioning documentation: [workflow](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/documentation.yaml)
    * Deploy versioning content: [workflow](https://github.com/Chisanan232/PyFake-API-Server-Surveillance/actions/workflows/pages/pages-build-deployment)

* Trigger points

    * For **latest** version: 

        All relative files about documentation includes CI workflow, document content, etc.

    * For **latest stable** version: 

        Same as CI workflow [CD](#cd).

* Target doing

    It would build versioning content and commit it into git branch ``gh-pages`` to trigger another CI workflow. And
    the GitHub Pages CI workflow would deploy the [documentation] into [GitHub pages].

    It has 2 different workflows for different versions:

    * For deployment **latest** version document: 
    
        About any files which relative documentation be updated, it would deploy the content to documentation. So the
        content of this version would always be the latest.
    
    * For deployment **latest stable** version document: 
    
        Only when software version be updated in package info module would trigger the after-process of this workflow,
        it would try to get the software version as the version to deploy the content to specific version of documentation.

[documentation]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/tree/master/docs
[GitHub pages]: https://chisanan232.github.io/pyfake-api-server-surveillance/stable/

![documentation cd]

[documentation cd]: ../../../_images/development/contributing/join_in_developing/documentation_cd_workflow.png


!!! tip "After version info change, it would trigger these CI/CD workflows"

    When occur version info change, it would trigger following
    CI/CD workflows:

    * [Source code deployment](#cd)
    * [Docker image deployment](#docker-ci)
    * [Stable version documentation deployment](#documentation-ci)
