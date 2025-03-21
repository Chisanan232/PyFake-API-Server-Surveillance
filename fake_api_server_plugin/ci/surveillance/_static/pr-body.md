Update [Fake-API-Server](https://github.com/Chisanan232/PyFake-API-Server) configuration because of API changes.

---

👀️ All API changes summary:

| modification state | number (by allow methods of API) |
|--------------------|----------------------------------|
| ➕ new             | {{ NEW_API_NUMBER }}             |
| ✏️ change          | {{ CHANGE_API_NUMBER }}          |
| 🚮 deprecate       | {{ DELETE_API_NUMBER }}          |

<details>
<summary>➕ API (new)</summary>
<ul>

{{ ADD_API_SUMMARY }}

[//]: # (Should be like below content)
[//]: # (* `/test/v1/process`)
[//]: # (  * `PUT`)

</ul>
</details>

<details>
<summary>✏️ API (change)</summary>
<ul>

{{ CHANGE_API_SUMMARY }}

[//]: # (* `/test/v1/sample`)
[//]: # (  * `GET`)
[//]: # (* `/test/v1/foo-feature`)
[//]: # (  * `GET`)
[//]: # (  * `POST`)
[//]: # (  * `DELETE`)

</ul>
</details>

<details>
<summary>🚮 API (deprecate)</summary>
<ul>

{{ DELETE_API_SUMMARY }}

[//]: # (* `/test/v1/deprecate`)
[//]: # (  * `PUT`)

</ul>
</details>
