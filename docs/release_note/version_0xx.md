# Version 0.X.X

## 0.1.0

### 🎉 New feature

1. Newborn of **_PyFake-API-Server-Surveillance_**.
2. A Python library about monitoring specific API interface and keeping **_PyFake-API-Server_** config up-to-update.
3. A customized action for GitHub Action.
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
            uses: ./
            with:
              config-path: <your fake-api-server-surveillance config>
            env:
              GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    ```


### 📑 Docs

1. Add documentation for this Python base CI tool.


### 🤖 Upgrade dependencies

1. Upgrade pre-commit dependencies.
