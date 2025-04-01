# PyFake-API-Server-Surveillance

[**_PyFake-API-Server-Surveillance_**] is a CI tool for
monitoring a specific API end points and keeping fake API server always up-to-date.

[**_PyFake-API-Server-Surveillance_**]: https://github.com/Chisanan232/PyFake-API-Server-Surveillance

## How to use it?

You need to configure a YAML file to set the surveillance details. Let's demonstrate a sample configuration for you:

```yaml
api-doc-url: 'http://192.168.20.113:1111/api-doc'  # The host which is the target API interface host
fake-api-server:
  server-type: rest-server
  subcmd:
    pull:
      args:
        - --config-path=./fake-server-demo/api.yaml
        - --include-template-config
        - --base-file-path=./fake-server-demo/
        - --base-url=/demo/v1
        - --divide-api
github-info:
  pull-request:
    draft: true
    labels:
      - '🤖 fake-api-server bot'
```

From above settings, it means setting an API:

* The API documentation configuration should refer to link _http://127.0.0.1:1111/api-doc_.
* About the section `fake-api-server`
  * Should use `rest-server` type to operate
  * Please use the specific arguments when trying to sync up the API by subcommand line `pull`
    * configuration path is `./fake-server-demo/api.yaml`
    * base directory is `./fake-server-demo/` which would record all the **_Fake-API-Server_** configuration
    * configuration should include `template` section details
    * all the URL has a base URL `/demo/v1` as prefix
    * Divide the API details as a single file
* About the section `github-info`
  * should open pull request as draft
  * pull request should tag as `🤖 fake-api-server bot`

> [!NOTE]
> If you want to know more details of subcommand line *pull* usage, please refer to [**_Fake-API-Server_** documentation].
>
> [**_Fake-API-Server_** documentation]: (https://chisanan232.github.io/PyFake-API-Server/stable/command-line-usage/rest-server/subcmd-pull/)

And save above setting as file ``/User/foo/fake-server-demo/fake-api-server-surveillance.yaml``.

Before running surveillance, please try to change anything at any of API interface which host the documentation at
`http://192.168.20.113:1111/api-doc` and check the running state.

Let's set up an instance to provide service which is the surveillance to monitor target API interface:

```console
docker run --name fake-server-surveillance \
           -v /User/foo/fake-server-demo:/mit-pyfake-api-server-surveillnace \
           -d \
           pyfake-api-server-surveillance:v0.1.0
```

Congratulations! You successfully configure and set up a web server for faking API.

## Environment variables

When you set up a [**_PyFake-API-Server-Surveillance_**] instance by Docker, you can pass one or more environment
variables to set its settings.

`CONFIG_PATH`

This is an option variable. It would set the file path where it should use to configure the APIs and set up web server.
In default, its value is ``./fake-api-server-surveillance.yaml``.

`GITHUB_TOKEN`

The fake server repository GitHub token. It should have 2 priorities to access: `contents` and `pull-requests`.

## Quick reference

* More details of tutorial how to set configuration: [Getting started to configure your APIs].
* [More details] of configuring fake API server surveillance.
* Want to know [entire knowledge of tool **_PyFake-API-Server-Surveillance_**].
* Also be curious of [**_PyFake-API-Server_**].

[Getting started to configure your APIs]: https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/getting-started/
[More details]: https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/getting-started/configure-references/
[entire knowledge of tool **_PyFake-API-Server-Surveillance**]: https://chisanan232.github.io/PyFake-API-Server-Surveillance/stable/
[**_PyFake-API-Server**]: https://chisanan232.github.io/PyFake-API-Server/stable/
