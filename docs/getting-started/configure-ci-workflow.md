# Set up surveillance with CI

Recently, it only supports GitHub Action to run **_PyFake-API-Server-Surveillance_** to monitor. So let's set up the
monitoring automation by GitHub Action.

!!! tip "What is different between **Pure value** and **Object for truly function**?"

    It's recommanded that using [schedule event] in GitHub Action to monitor target end point.

    [schedule event]: https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule


```yaml title=".github/workflows/monitor.yaml"
name: Monitor API interface

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
        uses: ./
        with:
          config-path: <your fake-api-server-surveillance config>
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

!!! note "Please remember set necessary authentication for this monitoring CI workflow"

    PyFake-API-Server-Surveillance will do some operations which must be
    authenticated by project owner:

    * Commit the change and push to repository

        If it find something changes, it would commit all the changes and
        push to remote repository finally. So it would need the permission
        as ``write`` level at ``contents`` in GitHub Action workflow setting.

        ```yaml
        permissions:
          contents: write  # Need this to push commits
        ```

    * Open a pull request in repository

        If it find something changes, it would open pull request which
        includes all the changesto remote repository finally. So it would
        need the permission as ``pull-requests`` level at ``contents`` in
        GitHub Action workflow setting.

        ```yaml
        permissions:
          pull-requests: write  # Need this to push commits
        ```

    Finally, please don't forget set the ``GITHUB_TOKEN`` for the action:

    ```yaml hl_lines="7-8"
    ...

      - name: Run Fake-API-Server-Surveillance
        uses: ./
        with:
          config-path: <your fake-api-server-surveillance config>
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    ...
    ```

    About more details of permission setting of GITHUB_TOKEN, please refer
    to [GitHub Action document].

    [GitHub Action document]: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/controlling-permissions-for-github_token

Congratulations! You have done all the preparation for using **_PyFake-API-Server-Surveillance_** to automatically
monitoring target end point! You will NEVER miss any changes of it. Just enjoy it with coffee ☕️.
