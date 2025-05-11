# Version 0.X.X

## **0.2.0**

### 🎉 New feature

1. Dockerize the project. ([PR#186])

[PR#186]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/186


### 🔨 Breaking changes

1. Doesn't support Python version 3.8 anymore. ([PR#202])

[PR#202]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/202


### 🪲 Bug Fix

#### 🙋‍♂️ For production

1. 💣 Critical bugs:
   1. For the composite action of customized action, it should always `git checkout` the source code from the specific 
      source repo. ([PR#212])

[PR#212]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/212


#### 👨‍💻 For development

1. Update the property classify setting about missing Python version 3.13. ([PR#207])
2. Fix the incorrect regex to match the specific file paths for documentation part. [PR#218]
3. Fix the Poetry configuration for the GitHub dependency bot. ([PR#223])

[PR#207]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/207
[PR#218]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/218
[PR#223]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/223


### ♻️ Refactor

1. Reuse the common function which has been implemented in the library **_Fake-API-Server_** for clear code. ([PR#187])
2. Reuse the new CI workflow about checking deployment state. ([PR#338])

[PR#187]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/187
[PR#338]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/338


### 🍀 Improvement

1. Add setting default value about the current GitHub repository if property `git-info.repo` is empty. ([PR#147])
2. Adjust the default PR body values to be more clear and readable for PR reviewers. ([PR#154])
3. Adjust the PR template setting to be more friendly.
4. Import to use configuration *CODEOWNERS* to manage the owners of source code and remove the deprecated field in GitHub dependency bot. ([PR#377])

[PR#147]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/147
[PR#154]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/154
[PR#220]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/220
[PR#337]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/337


### 📑 Docs

1. Update the content for new changes about the default PR body value. ([PR#181])
2. Let the example code and example result to be more clear. ([PR#217])
3. Add a new section about development details of this project. ([PR#219])
4. Activate the feature about overriding for the documentation UI/UX. ([PR#221])
5. Adjust the note title to be more readable. ([PR#222])

[PR#181]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/181
[PR#217]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/217
[PR#219]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/219
[PR#221]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/221
[PR#222]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/222


### 🤖 Upgrade dependencies

1. Upgrade the Python dependencies.
   1. Bump cryptography from 43.0.3 to 44.0.1 ([PR#201])
   2. Bump jinja2 from 3.1.4 to 3.1.6 ([PR#229])
   3. Bump mkdocs-autorefs from 1.2.0 to 1.4.1 ([PR#238])
   4. Bump mkdocs-material from 9.6.3 to 9.6.12 ([PR#241])
   5. Bump mkdocs-git-revision-date-localized-plugin from 1.3.0 to 1.4.5 ([PR#241])
   6. Bump coverage from 6.5.0 to 7.8.0 ([PR#247])
   7. Bump pre-commit from 3.5.0 to 4.2.0 ([PR#250])
   8. Bump mkdocstrings from 0.26.1 to 0.29.1 ([PR#281])
   9. Bump pylint from 3.2.7 to 3.3.6 ([PR#282])
   10. Bump pytest-rerunfailures from 14.0 to 15.0 ([PR#283])
   11. Bump pytest from 8.3.4 to 8.3.5 ([PR#286])
   12. Bump mkdocstrings-python from 1.11.1 to 1.13.0 ([PR#287])
   13. Bump pytest-cov from 5.0.0 to 6.1.1 ([PR#325])
   14. Bump pylint from 3.3.6 to 3.3.7 ([PR#331])
   15. Bump pytest-rerunfailures from 15.0 to 15.1 ([PR#339])
2. Upgrade pre-commit dependencies. ([PR#200], [PR#330])
3. Upgrade the CI reusable workflows.
   1. Bump Chisanan232/GitHub-Action_Reusable_Workflows-Python from 6.1 to 7.2 ([PR#201])
   2. Bump Chisanan232/GitHub-Action_Reusable_Workflows-Python from 7.2 to 7.3 ([PR#334])

[PR#200]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/200
[PR#201]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/201
[PR#228]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/228
[PR#229]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/229
[PR#238]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/238
[PR#241]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/241
[PR#244]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/244
[PR#247]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/247
[PR#250]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/250
[PR#281]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/281
[PR#282]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/282
[PR#283]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/283
[PR#286]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/286
[PR#287]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/287
[PR#325]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/325
[PR#330]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/330
[PR#331]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/331
[PR#334]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/334
[PR#339]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/339


### 🚮Deprecate

1. Doesn't support Python version 3.8 anymore. ([PR#202])

[PR#202]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance/pull/202


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
