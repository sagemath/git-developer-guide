.. _chapter-manual-git:

================
GIT The Hard Way
================

For beginners to Sage development we recommend using the Sage
development scripts as explained in :ref:`chapter-walk-through`, which
simplify using git and the trac server. However, you can use git
directly to work on Sage if you want to take off the training
wheels. This chapter will tell you how to do so assuming some
basic familiarity with git.

.. warning::

    For now, use the ``build_system`` branch instead of master. This
    will be changed soon.


We assume that you have a copy of the Sage git repository, for example
by running::

    [user@localhost ~]$ git clone git://github.com/sagemath/sage.git -b build_system
    [user@localhost ~]$ cd sage
    [user@localhost sage]$ make



Branching Out
=============

.. TODO::

    create branches, switch between branches



The Trac Server
===============

The Sage trac server also hold a copy of the Sage repository, it is
served via ssh but at the non-standard port 2222. To add it as a
remote repository to your local git repository, use the command::

    [user@localhost sage]$ git remote add trac ssh://git@trac.sagemath.org:2222/sage.git -t master
    [user@localhost sage]$ git remote -v
    origin	git://github.com/sagemath/sage.git (fetch)
    origin	git://github.com/sagemath/sage.git (push)
    trac	ssh://git@trac.sagemath.org:2222/sage.git (fetch)
    trac	ssh://git@trac.sagemath.org:2222/sage.git (push)

Instead of ``trac`` you can use any local name you want, of course. It
is perfectly fine to have multiple remote repositories for git, think
of them as bookmarks. You can then use ``git pull`` to get changes and
``git push`` to upload your local changes using::

    [user@localhost sage]$ git <push|pull> trac [ARGS]


Checking Out Tickets
--------------------

Trac tickets that are finished or in the process of being worked on
can have a git branch attached to them. This is the "Branch:" field in
the ticket description. The branch name is generally of the form
``u/user/description``, where ``user`` is the name of the user who
made the branch and ``description`` is some free-form short
description (and can include further slashes).

If you want to work with the changes in that remote branch, you must
make a local copy. In particular, git has no concept of directly
working with the remote branch, the remotes are only bookmarks for
things that you can get from/to the remote server. Your local branch
can have a different name, for example::

    [user@localhost sage]$ git checkout -b my_branch trac/u/user/description
    Branch my_branch set up to track remote branch u/user/description from trac by rebasing.
    Switched to a new branch 'my_branch'

creates a new branch in your local git repository named ``my_branch``
and switches to it. It is based on the remote ``u/user/description``,
so you start out with the same files as in that ticket. You can then
edit files and commit changes to your local branch.


Pushing Your Changes to a Ticket
--------------------------------

To add your local branch to a trac ticket, you first have to upload it
to the Sage trac repository and then put its name into the "Branch:"
field on the trac ticket.

Having set up your SSH key as described in
:ref:`section-trac-ssh-key`, you have push permissions to branches of
the form ``u/user/*`` where ``user`` is your trac username and ``*``
is a wildcard, that is, any valid git branch name. By default, you do
*not* have push permissions to other user's branches or the Sage
master branch. To push your branch to trac use::

    git push my_branch:u/user/description

where

* ``my_branch`` is the name of your local branch,
* ``user`` is your trac username,
* ``description`` is some (short but self-explanatory) description of
  your branch.

Then, in order to use this branch as the proposed change on a trac
ticket, just fill its name ``u/user/description`` into the "Branch:"
field of the ticket description.

The ``Branch`` field is color coded: red means there is an issue,
green means it will merge cleanly into ``master``. If it is red, the
tooltip will tell you what is wrong.  If it is green, then it will
link to a diff of the changes against ``u/ohanar/build_system``. (This
is temporary until [#14480](http://trac.sagemath.org/14480) is merged
into the ``master`` branch.)



Merging and Rebasing
--------------------





Reset and Recovery
------------------

Git makes it very hard to truly mess up. Here is a short way to get
back onto your feet, no matter what. First, if you just want to go
back to a working Sage installation you can always abandon your
working branch by switching to your local copy of the ``build_system``
branch::

    [user@localhost sage]$ git checkout build_system

As long as you didn't make any changes to the ``build_system`` branch
directly, this will give you back a working Sage.

If you want to keep your branch but go back to a previous commit you
can use the reset command. For this, look up the commit in the log
which is some 40-digit hexadecimal number. Then use ``git reset
--hard`` to revert your files back to the previous state::

    [user@localhost sage]$ git log
    ...
    commit eafaedad5b0ae2013f8ae1091d2f1df58b72bae3
    Author: First Last <user@email.com>
    Date:   Sat Jul 20 21:57:33 2013 -0400

        Commit message
    ...
    [user@localhost sage]$ git reset --hard eafae

You only need to type the first couple of hex digits, git will
complain if this does not uniquely specify a commit. Also, there is
the useful abbreviation ``HEAD~`` for the previous commit.
