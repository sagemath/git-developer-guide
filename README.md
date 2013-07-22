Git Version of the Sage Developer Manual
========================================

See the current documentation at http://sagemath.github.io/git-developer-guide/


Prerequisites
-------------

To build the manual you need Python and Sphinx installed. If you have
Sage, you can use a Sage shell (run `sage -sh`).



Usage
-----

* The developer manual is in the `/developer` directory in the
  repository root. Edit files there to modify the docs.

* Use the `build` script to build the html documentation.

* Use the `publish` script to copy the documentation to the github
  pages (the web page hosted on github).

* Sphinx uses caching to only rebuild pages as necessary. Sometimes,
  you can get problems with stale caches. It is safe to delete the
  `/html` directory and then rebuild all docs with `./build`.
