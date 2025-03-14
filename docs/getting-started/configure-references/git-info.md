# Git setting

## ``git-info``

The detail settings about how to run git operation. In **_PyFake-API-Server-Surveillance_**, it would commit the change
and push to remote repository by itself without any manually operations. So this section targets set some details of its
git operation.


### ``repo``

The target repository naming which need include project owner name. For example, ``Chisanan232/Sample-Fake-Server``.

### ``commit``

The section about setting properties which are relative with ``git commit`` operation.

#### ``commit.author``

The section about setting the author of commit.

##### ``commit.author.name``

The author name. For example, ``Fake-API-Server-Surveillance [bot]``.

??? note "Translate as command line"

    Means the command line operation:

    ```shell
    >>> git config user.name
    ```

##### ``commit.author.email``

The email info of author. For example, ``test@gmail.com``.

??? note "Translate as command line"

    Means the command line operation:

    ```shell
    >>> git config user.email
    ```

#### ``commit.message``

What message it should use to operate ``git commit``.

??? note "Translate as command line"

    Means the command line operation:

    ```shell
    >>> git commit -m "<the value of git-info.commit.message>"
    ```
