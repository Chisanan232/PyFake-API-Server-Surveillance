# How it works

Without **_PyFake-API-Server-Surveillance_**, you're working workflow of keeping **_PyFake-API-Server_** configuration
to be up-to-date would be like following:

1. Check the target API interface changes or not
2. If it has changes, update the **_PyFake-API-Server-Surveillance_** configuration

With **_PyFake-API-Server-Surveillance_**, you'll do nothing at all and still could keep **_PyFake-API-Server_**
configuration to be up-to-date automatically. And workflow of **_PyFake-API-Server-Surveillance_** is totally same with
above. It just automates them.

## **_PyFake-API-Server-Surveillance_** workflow

1. Deserialize the configuration details and action inputs from CI workflow.
2. Get the latest API documentation configuration.[^1]
3. Convert the API documentation configuration to **_PyFake-API-Server_** configuration and compare it with current
version configuration.
4. Update the **_PyFake-API-Server_** configuration.
5. Commit the new changes.[^2]
6. Push to remote repository about the fake server configuration.[^2]
7. Open a pull request in remote repository.[^3]
8. Notify the result. (should implemented by yourself, do nothing in default)[^4]

  [^1]:
    **_PyFake-API-Server-Surveillance_** uses API documentation
    configuration to judge it has changes or not.
  [^2]:
    It would use the details about [git info in configuration] to
    do some git operations.
  [^3]:
    It would use the details about [GitHub info in configuration] to
    do some GitHub operations.
  [^4]:
    In default, it would do nothing. But developers could implement
    it with [notification function] in runner object.

    [git info in configuration]: ../getting-started/configure-references/git-info.md
    [GitHub info in configuration]: ../getting-started/configure-references/github-info.md
    [notification function]: ../../getting-started/api-references/runner/#fake_api_server_plugin.ci.surveillance.runner.FakeApiServerSurveillance._notify
