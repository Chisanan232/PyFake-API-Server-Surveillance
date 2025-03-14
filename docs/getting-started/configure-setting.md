# Configure your **_PyFake-API-Server-Surveillance_**

It configures the detail settings of **_PyFake-API-Server-Surveillance_** by YAML syntax, and must have either a
``.yml`` or ``.yaml`` file extension. If you're new to YAML and want to learn more, see "[Learn YAML in Y minutes.]"

[Learn YAML in Y minutes.]: https://learnxinyminutes.com/docs/yaml/


## What settings are necessary?

In **_PyFake-API-Server-Surveillance_** realm, only 1 thing it needs to use, but it doesn't know: the end point of API
documentation configuration.

So let's configure the lowest necessary configuration as below:

```yaml title="fake-api-server-surveillance.yaml"
api-doc-url: 'http://127.0.0.1:1111/api-doc'
```

How easily it is! Now we have done the configuration of **_PyFake-API-Server-Surveillance_**. Let's go to next step to
set up a surveillance to monitor.
