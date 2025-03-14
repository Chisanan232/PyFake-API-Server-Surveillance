# Fake-API-Server setting

## ``fake-api-server``

The detail settings about how **_PyFake-API-Server-Surveillance_** should run with **_PyFake-API-Server_**. Recently, it
only supports setting with subcommand line [pull].

[pull]: https://chisanan232.github.io/PyFake-API-Server/stable/command-line-usage/rest-server/subcmd-pull/

### ``server-type``

Which server type it should use to identify the target API server configuration.

!!! warning "🚧 Not totally complete"

    Currently, it only supports ``rest-server``.

### ``subcmd``

This section is responsible for the specific subcommand line setting.

#### ``subcmd.<subcommand line>``

Which subcommand line for customizing settings. Please refer to [command line details] of **_PyFake-API-Server_** to
set value.


##### ``subcmd.<subcommand line>.args``

Customize which arguments should use in running the subcommand line. Please refer [command line details] to set the
command line options of the specific subcommand line.

[command line details]: https://chisanan232.github.io/PyFake-API-Server/stable/command-line-usage/

!!! example "Here is a demonstration and how it would transfer as command line"

    Let's give a sample configuration with section ``subcmd``:

    ```yaml linenums="1"
    subcmd:
      pull:
        args:
          - --config-path=./sample-api.yaml
          - --include-template-config
          - --base-file-path=./
          - --base-url=/test/v1
          - --divide-api
    ```

    It customizes how **_PyFake-API-Server-Surveillance_** should
    run the program with the specific options under subcommand line
    ``pull``.

    So above setting also could translate as command line as following:

    ```shell
    >> fake rest-server pull \
        --config-path=./sample-api.yaml \
        --base-file-path=./ \
        --include-template-config \
        --base-url=/test/v1 \
        --divide-api
    ```
