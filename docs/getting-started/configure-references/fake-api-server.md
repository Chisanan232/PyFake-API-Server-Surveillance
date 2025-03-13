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

Which subcommand line for customizing settings. Please refer to [command line details] of **_PyFake-API-Server_** to
set value.

#### ``subcmd.<subcommand line>``

This section is responsible for the specific subcommand line setting.


##### ``subcmd.<subcommand line>.args``

Customize which arguments should use in running the subcommand line. Please refer [command line details] to set the
command line options of the specific subcommand line.

[command line details]: https://chisanan232.github.io/PyFake-API-Server/stable/command-line-usage/
