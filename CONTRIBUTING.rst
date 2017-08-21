Contributing
============

When should I contribute?
-------------------------

This documentation was created with the intention that anybody could provide their own research to the community at large.
Because of this we want to make it as straightforward as possible for people to edit and update the documentation. We appreciate
any kind of contribution, be it as small as fixing typos, or as large as a full reverse engineered structure for a file type.
Feel free to ask via Issue or IRC when you are unsure about anything.

Filing an Issue
---------------
When there is something wrong or missing within the documentation, that needs to be addressed
but it's not clear what should be done about it, you can open an issue on the repository for theses docs.
When the issue is related to a specific part of the docs, open that file on GitHub, select the relevant lines,
and click on "Open a new Issue" in the context menu for the selection.
When the issue is not related to a specific part, such a part does not exist, open one directly from the issues overview page.

Issue layout
^^^^^^^^^^^^
Every issue should contain a meaningful title and description on what is meant to be discussed. When referring to parts of the docs,
a link to the docs page or its source code should be provided. Issues are the right place for discussion,
before changing some part of the docs.

Creating a pull request
-----------------------
Usually you will just want to edit a page of the docs. For that, click on "Edit on GitHub" on any page of the actual docs.
Then click the edit symbol (pen) above the preview of the file. Be aware that github can not render/preview all elements of the docs
correctly. Then edit the file and save your changes.

You usually won't have write access to the repository, so github will create a *fork* of the repository and you will be asked if you
want to create a pull request for your changes. Confirm that and we'll review the request and merge it into the docs if we don't have
any objections.

Building the docs locally
-------------------------
If you want to build the docs on your own computer, please install ``make`` (on linux) and ``python``.
It is recommended to use `virtualenv` if you can, run

* ``virtualenv venv`` within the main directory after you cloned the repository and
* ``source venv/bin/activate`` every time you open a new console to build the docs

With `pip` installed, run

* ``pip install sphinx``
* ``pip install sphinx-rtd-theme``

To build the docs, run ``make html`` within the ``/docs`` folder
