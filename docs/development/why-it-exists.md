# Why it exists

**_PyFake-API-Server-Surveillance_** would base on the settings of configurations includes **_PyFake-API-Server-Surveillance_**
and **_GitHub Action_** to set up a CI workflow to auto-check the target API interface and auto-update if it has any changes.
But, how it exactly works?

Please consider one thing, you're the maintainer of the fake API server instance which be set up by **_PyFake-API-Serve_**,
so you always need to take care the specification or API interface every time because you worry about the **_PyFake-API-Serve_**
configuration be outdated with the latest version. It may reduce the burden of faking an API server for test, but it
increases the burden of checking the API interface changes from source code, API documentation or specification, etc.

First of all, you will find the changes from specification or planner notification. However, in some terrible cases, planner
may adjust specification in the sly and doesn't notify you. And you also doesn't find the changes from source code or API
documentation like Swagger or OpenAPI. ~~So, you'll be anger and fire the projects and planners.~~ And it might break some
features in Font-End side. It's terrible for web services.

So this tool be designed and implemented for automations of checking and updating **_PyFake-API-Serve_** configuration.
It could let developers be focus on their job only without keep checking the API interface changes. With **_GitHub_**
**_Action_** could totally automatically check the changes and keep the **_PyFake-API-Serve_** configuration to be up-to-date.
