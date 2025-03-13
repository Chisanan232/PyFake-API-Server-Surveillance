# Configuration reference

Here is the details of **_PyFake-API-Server-Surveillance_** configuration.

## ``api-doc-url``

The end point of the target API documentation configuration for monitoring.

## ``fake-api-server``

The section to set the details of **_PyFake-API-Server_**. Please refer to [here](./fake-api-server.md) to get more
details.

## ``git-info``

The section to set the details of git operation in program. Please refer to [here](./git-info.md) to get more details.

## ``github-info``

The section to set the details of GitHub operation in program. Please refer to [here](./github-info.md) to get more
details.

## ``accept_config_not_exist``

This is a boolean type value. If it's ``false``, it would raise a runtime error if it cannot find the **_PyFake-API-Server_**
configuration in CI process, or it won't with ``true``.
