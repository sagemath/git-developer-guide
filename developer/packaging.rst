.. _chapter-packaging:

==========================
Packaging Third-Party Code
==========================

One of the mottoes of the Sage project is to not reinvent the
wheel. If an algorithm is already implemented in a well-tested library
then consider incorporating that library into Sage. The current list
of available packages are the subdirectories of
``SAGE_ROOT/build/pkgs/``.

Not all of these packages are built by default, they are divided into
standard and optional ones. Standard packages are built by default and
have much more stringent quality requirements. In addition, there are
experimental spkgs (and some legacy optional spkgs) that are just
tarballs containing build scripts.


Inclusion Procedure for New Packages
====================================

For a package to become part of Sage's standard distribution, it
must meet the following requirements:

- **License**. For external packages, the license must be compatible
  with the GNU General Public License, version 3. More precisely, it
  must be allowed to license the code that you wish to include under
  the GPL version 3.  Sage library code (anything which is not an
  external package) must be licensed under the
  "GNU General Public License as published by the Free Software Foundation;
  either version 2 of the License, or (at your option) any later version."
  The Free Software Foundation maintains a long list of
  `licenses and comments about them <http://www.gnu.org/licenses/license-list.html>`_.

- **Build Support**. The code **must** build on all the `fully
  supported platforms
  <http://wiki.sagemath.org/SupportedPlatforms#Fully_supported>`_.

  A standard package should also work on all the platforms where Sage
  is `expected to work
  <http://wiki.sagemath.org/SupportedPlatforms#Expected_to_work>`_ and
  on which Sage `almost works
  <http://wiki.sagemath.org/SupportedPlatforms#Almost_works>`_ but
  since we don't fully support these platforms and often lack the
  resources to test on them, you are not expected to confirm your
  packages works on those platforms.  However, if you can, it is
  better to do so. As noted `here
  <http://wiki.sagemath.org/SupportedPlatforms#Expected_to_work>`_, a
  failure of Sage to work on a platform where it is expected to work,
  will be considered a bug.

  There is no need to worry too much about platforms where Sage will
  `probably not work
  <http://wiki.sagemath.org/SupportedPlatforms#Probably_will_not_work>`_
  though if it's clear that there is significant effort taking place
  to port Sage to a platform, then you should aim to ensure your
  package does not cause unnecessary headaches to those working on the
  port.

  If it's clear that a port is stagnent, with nobody working on it,
  then you can safely ignore it.

  Remarks:

  - Some Sage developers are willing to help you port to OS X, Solaris
    and Windows. But this is no guarantee and you or your project are
    expected to do the heavy lifting and also support those ports
    upstream if there is no Sage developer who is willing to share the
    burden.

  - One of the best ways to ensure your code works on multiple
    platforms is to only use commands which are defined by
    `POSIX.1-2008 <http://www.opengroup.org/onlinepubs/9699919799/>`_
    and only use options which are defined in the POSIX standard. For
    example, do not use the -p option to `uname
    <http://www.opengroup.org/onlinepubs/9699919799/utilities/uname.html>`_
    as the '-p' option is not defined by the POSIX standard, so is not
    portable.  If you must use a non-POSIX command, or a option which
    is not defined by POSIX, then ensure the code only gets executed
    on the platform(s) where that command and/or option will be
    acceptable.


- **Quality**. The code should be "better" than any other available
  code (that passes the two above criteria), and the authors need to
  justify this. The comparison should be made to both Python and other
  software. Criteria in passing the quality test include:

  - Speed

  - Documentation

  - Usability

  - Memory leaks

  - Maintainable

  - Portability

  - Reasonable build time, size, dependencies


- **Previously an optional package**. Usually a new standard package
  must have spent some time as an optional package. However, sometimes
  this is not possible, if for example a new library is needed to
  permit an updated version of a standard package to function.

- **Refereeing**. The code must be refereed, as discussed in
  :ref:`chapter-sage-trac`.


Directory Structure
===================

Third-party packages in Sage consists of two parts: 

#. The tarball as it is distributed by the third party, or as close as
   possible. Valid reasons for modifying the tarball are deleting
   unnecessary files to keeep the download size manageable, but the
   actual code must be unmodified.

#. The build scripts and associated files are in a subdirectory
   ``SAGE_ROOT/build/pkgs/package``, where you replace ``package``
   with a lower-case version of the upstream project name. 

As an example, let us consider a hypothetical FoO project. They
(upstream) distribute a tarball ``foo-1.3.tar.gz``. to package it in
Sage, we create a subdirectory containing the following::

    SAGE_ROOT/build/pkgs/foo
    |-- patches
    |   |-- bar.patch
    |   `-- baz.patch
    |-- checksums.ini
    |-- package-version.txt
    |-- spkg-check
    |-- spkg-install
    |-- spkg-src
    `-- SPKG.txt

We discuss the individual files in the following.


.. _section-spkg-install:

Install Script
--------------


The ``spkg-install`` file is a shell script installing the package,
with ``PACKAGE_NAME`` replaced by the the package name. In the best
case, the upstream project can simply be installed by the usual
configure / make / make install steps. In that case, the build script
would simply be::

    #!/usr/bin/env bash

    ./configure --prefix="$SAGE_LOCAL" --libdir="$SAGE_LOCAL/lib"
    if [ $? -ne 0 ]; then
        echo >&2 "Error configuring PACKAGE_NAME."
        exit 1
    fi

    $MAKE
    if [ $? -ne 0 ]; then
        echo >&2 "Error building PACKAGE_NAME."
        exit 1
    fi

    $MAKE -j1 install
    if [ $? -ne 0 ]; then
        echo >&2 "Error installing PACKAGE_NAME."
        exit 1
    fi




.. _section-spkg-versioning:

Package Versioning
------------------

If you want to bump up the version of an spkg, you need to follow some
naming conventions. Use the name and version number as given by the
upstream project, e.g. ``matplotlib-1.0.1``. If the upstream package is
taken from some revision other than a stable version, you need to
append the date at which the revision is made, e.g. the Singular
package ``singular-3-1-0-4-20090818.p3.spkg`` is made with the
revision as of 2009-08-18. If you start afresh from an upstream
release without any patches to its source code, the resulting spkg
need not have any patch-level labels (appending ".p0" is allowed, but
is optional). For example, ``sagenb-0.6.spkg``
is taken from the upstream stable version ``sagenb-0.6`` without any
patches applied to its source code. So you do not see any patch-level
numbering such as ``.p0`` or ``.p1``.


``package-version.txt``




.. _section-spkg-SPKG-txt:

The SPKG.txt File
-----------------


.. _section-spkg-patching:

Patching Sources
----------------

The ``patches`` directory and 

The main message of this section is: use the GNU program ``patch`` to
apply patches to files in ``src/``.  GNU patch is distributed with
Sage, so if you are writing an spkg which is not part of the standard
Sage distribution, you may use ``patch`` in the ``spkg-install``
script freely. 


- ``patches/``: this directory contains patches to source files in
  ``src/``.  See :ref:`section-old-spkg-patching-overview`.  Patches
  to files in ``src/`` should be applied in ``spkg-install``, and all
  patches must be documented in ``SPKG.txt``, i.e. what they do, if
  they are platform specific, if they should be pushed upstream,
  etc. To ensure that all patched versions of upstream source files
  under ``src/`` are under revision control, the whole directory
  ``patches/`` must be under revision control.



If there are any patches then your ``spkg-install`` script should
contain a section like this::

    for patch in ../patches/*.patch; do
        [ -r "$patch" ] || continue  # Skip non-existing or non-readable patches
        patch -p1 <"$patch"
        if [ $? -ne 0 ]; then
            echo >&2 "Error applying '$patch'"
            exit 1
        fi
    done

which applies the patches to the sources.


.. _section-spkg-src:

Modified Tarballs
-----------------

The ``spkg-src`` file is optional, and ideally not used at all. 


Checksums
---------

``checksums.ini``
