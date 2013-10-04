.. _chapter-manual-git:

================
Git the Hard Way
================

For beginners to Sage development we recommend using the Sage
development scripts as explained in :ref:`chapter-walk-through`, which
simplify using git and the trac server. However, you can use git
directly to work on Sage if you want to take off the training
wheels. This chapter will tell you how to do so assuming some
basic familiarity with git.

We assume that you have a copy of the Sage git repository, for example
by running::

    [user@localhost ~]$ git clone git://github.com/sagemath/sage.git -b master
    [user@localhost ~]$ cd sage
    [user@localhost sage]$ make

.. warning::

    For now, use the ``public/sage-git/master`` branch instead of
    master. This will be changed soon.

.. _section-git-branch:

Branching Out
=============

A branch is any set of changes that deviates from the current official
Sage tree. Whenever you start developing some new feature or fix a bug
you should first create a new branch to hold the changes. It is easy
to create a new branch, just check out (switch to) the branch from
where you want to start (that is, ``build_system``) and use the *git
branch* command::

    [user@localhost sage]$ git checkout build_system
    [user@localhost sage]$ git branch my_new_branch
    [user@localhost sage]$ git checkout my_new_branch
    [user@localhost sage]$ git branch
      build_system
    * my_new_branch

Without an argument, the *git branch* command just displays a list of
all local branches with the current one marked by an asterisk. Also
note that *git branch* creates a new branch, but does not switch to
it. To avoid typing the new branch name twice you can use the shortcut
``git checkout -b my_new_branch`` to create and switch to the new
branch in one command.


.. _section-git-commit:

Commits (Snapshots)
===================

Once you have your own branch feel free to make any changes as you
like. Whenever you have reached your goal, a milestone towards it, or
just feel like you got some work done you should commit your
changes. That is, snapshot the state of all files in the
repository. First, you need to *stage* the changed files, which tells
git which files you want to be part of the next commit::

    ... edit foobar.txt ...

    [user@localhost sage]$ git status
    # On branch build_system
    # Untracked files:
    #   (use "git add <file>..." to include in what will be committed)
    #
    #       foobar.txt
    nothing added to commit but untracked files present (use "git add" to track)

    [user@localhost sage]$ git add foobar.txt
    [user@localhost sage]$ git status
    # On branch build_system
    # Changes to be committed:
    #   (use "git reset HEAD <file>..." to unstage)
    #
    #	new file:   foobar.txt
    #

Once you are satisfied with the list of staged files, you create a new
snapshot with the *commit* command::

    [user@localhost sage]$ git commit
    ... editor opens ...
    [build_system 31331f7] Added the very important foobar text file
     1 file changed, 1 insertion(+)
      create mode 100644 foobar.txt

This will open an editor for you to write your commit message. The
commit message should generally have a one-line description, followed
by an empty line, followed by further explanatory text::

    Added the very important foobar text file

    This is an example commit message. You see there is a one-line
    summary followed by more detailed description, if necessary.

You can then continue working towards your next milestone, make
another commit, repeat until finished. As long as you do not
*checkout* another branch, all commits that you make will be part of
the branch that you created.



.. _section-git-trac:

The Trac Server
===============

The Sage trac server also holds a copy of the Sage repository, it is
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

.. note::
   
    In the command above we set up the remote to only track the
    ``master`` branch on the trac server (the ``-t master``
    option). This avoids clutter by not automatically downloading all
    branches ever created. But it also means that you will not fetch
    everything that is on trac by default, and you need to explicitly
    tell git which branch you want to get from trac. See the
    :ref:`section-git-checkout` section for examples.

The way we set up the remote here is via ssh authentication (the
``ssh://`` part), this requires you to have a trac account and to set
up your ssh public key as described in
:ref:`section-trac-ssh-key`. Authentication is necessary if you want
to upload anything to ensure that it really is from you. However, if
you just want to download branches from the trac server then you can
set up the remote to use the git protocol without authentication::

    [user@localhost sage]$ git remote add trac git://trac.sagemath.org/sage.git -t master

Setting up the remote repository this way allows you to do perform all
steps covered this manual (except for :ref:`section-git-push`) without
having a trac account. To switch between the two setups, just remove
the current remote repository with ``git remote remove trac`` and then
run the respective ``git remote add trac ...`` command.
     



.. _section-git-checkout:

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
things that you can get from/to the remote server. Hence, the first
thing you should do is to get everything from the trac server's branch
into your local repository. This is achieved by::

    [user@localhost sage]$ git fetch trac u/user/description
    remote: Counting objects: 62, done.
    remote: Compressing objects: 100% (48/48), done.
    remote: Total 48 (delta 42), reused 0 (delta 0)
    Unpacking objects: 100% (48/48), done.
    From ssh://trac.sagemath.org:2222/sage
    * [new branch]      u/user/description -> FETCH_HEAD

The ``u/user/description`` branch is now temporarily (until you fetch
something else) stored in your local git database under the alias
``FETCH_HEAD``. In the second step, we make it available as a new
local branch and switch to it. Your local branch can have a different
name, for example::

    [user@localhost sage]$ git checkout -b my_branch FETCH_HEAD
    Switched to a new branch 'my_branch'

creates a new branch in your local git repository named ``my_branch``
and modifies your local Sage filesystem tree to the state of the files
in that ticket. You can now edit files and commit changes to your
local branch.


.. _section-git-push:

Pushing Your Changes to a Ticket
--------------------------------

To add your local branch to a trac ticket, you should first decide on
a name on the Sage trac repository. In order to avoid name clashes,
you have push permissions to branches of the form ``u/user/*`` where
``user`` is your trac username and ``*`` is a wildcard, that is, any
valid git branch name. By default, you do *not* have push permissions
to other user's branches or the Sage master branch. In the following,
we will be using ``u/user/description`` as the branch name, where it
is understood that you replaced

* ``user`` with your trac username, and
* ``description`` with some (short but self-explanatory) description of
  your branch. May contain further slashes, but spaces are not allowed.

Your first step should be to put your chosen name into the "Branch:"
field on the trac ticket. To push your branch to trac you then use
either::

    [user@localhost sage]$ git push --set-upstream trac HEAD:u/user/description

if you started the branch yourself and do not follow any other branch,
or use::

    [user@localhost sage]$ git push trac HEAD:u/user/description

if your branch already has an upstream branch.  The ``HEAD`` means
that you are pushing the most recent commit (and, by extension, all of
its parent commits) of the current local branch to the remote
branch. The remaining arguments are

* ``user`` is your trac username,
* ``description`` the description of your branch.

The ``Branch`` field is color coded: red means there is an issue,
green means it will merge cleanly into ``master``. If it is red, the
tooltip will tell you what is wrong.  If it is green, then it will
link to a diff of the changes against ``u/ohanar/build_system``. (This
is temporary until `#14480 <http://trac.sagemath.org/14480>`_ is merged
into the ``master`` branch.)

.. note::

    You also have to fill in the "Commit:" field with the 40-digit
    SHA1 hash of your last commit. If you first fill out the "Branch:"
    field on trac and then push to git, then git will automatically
    search for the ticket and fill in the "Commit:" field for you. 

    If, for some reason, you first push to the trac git repository and
    then change the "Branch:" field, then you also have to update the
    "Commit:" field yourself. You can find out the SHA1 hash, for
    example, with::
   
        $ git log -1
        commit 2ee18c5b5c7417e0f8939d9db54d753c468964d8
        Author: Firstname Lastname <user@sagemath.org>
        Date:   Wed Aug 7 21:50:00 2013 +0100
       
            My first commit message!


.. _section-git-pull:

Getting Changes
---------------

A common task during development is to synchronize your local copy of
the branch with the branch on trac. In particular, assume you
downloaded somebody else's branch made some suggestions for
improvements on the trac ticket. Now the original author incorporated
your suggestions into his branch, and you want to get the added
changesets to complete your review. Assuming that you originally got
your local branch as in :ref:`section-git-checkout`, you can just
issue::

    [user@localhost sage]$ git pull -r trac u/user/description
    From ssh://trac.sagemath.org:2222/sage
     * branch            u/user/description -> FETCH_HEAD
    First, rewinding head to replay your work on top of it...
    Fast-forwarded my_branch to 19e832a93094abbf7486b51335e6b0f7dc91478c.

This will download the changes from the originally-used remote branch
and rebase (the ``-r`` command line option) your local branch onto
them. Rebasing is appropriate if you haven't published any changes to
the ticket yourself, see the :ref:`section-git-merge` section if that
is not the case.


.. _section-git-merge:

Merging and Rebasing
====================

Invariably, Sage development continues while you are working on your
local branch. For example, let us assume you started ``my_branch`` at
commit ``B``. After a while, your branch has advanced to commit ``Z``
while the Sage master branch has advanced to ``D`` ::

                     X---Y---Z my_branch
                    /
               A---B---C---D master

How should you deal with upstream changes while you are
still developing your code? In principle, there are two ways of
dealing with it:

* The first solution is to change the commits in your local branch to
  start out at the new master. This is called **rebase**, and it
  rewrites your current branch::
   
      git checkout my_branch
      git rebase master

  In terms of the commit graph, this results in::

                             X'--Y'--Z' my_branch
                            /
               A---B---C---D master

  Since the SHA1 hash includes the hash of the parent, all commits
  change. This means that you should only ever use rebase if nobody
  else has used one of your ``X``, ``Y``, ``Z`` commits to base their
  development on. 

* The other solution is to not change any commits, and instead create
  a new merge commit ``W`` which merges in the changes from the newer
  master. This is called **merge**, and it merges your current branch
  with another branch::

      git checkout my_branch
      git merge master

  The result is the following commit graph::

                     X---Y---Z---W my_branch
                    /           /
               A---B---C-------D master

  The downside is that it introduced an extra merge commit that would
  not be there had you used rebase. But that is also the advantage of
  merging: None of the existing commits is changed, only a new commit
  is made. This additional commit is then easily pushed to the git
  repository and distributed to your collaborators.

As a general rule of thumb, use merge if you are in doubt. The
downsides of rebasing can be really severe for other developers, while
the downside of merging is just minor. Finally, and perhaps the most
important advice, do nothing unless necessary. It is ok for your
branch to be behind the master branch. Just keep developing your
feature. Trac will tell you if it doesn't merge cleanly with the
current master by the color of the "Branch:" field, and the patchbot
(coloured blob on the trac ticket) will test whether your branch still
works on the current master. Unless either a) you really need a
feature that is only available in the current master, or b) there is a
conflict with the current master, there is no need to do anything on
your side.
