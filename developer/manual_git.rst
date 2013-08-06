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

.. warning::

    For now, use the ``build_system`` branch instead of master. This
    will be changed soon.


We assume that you have a copy of the Sage git repository, for example
by running::

    [user@localhost ~]$ git clone git://github.com/sagemath/sage.git -b build_system
    [user@localhost ~]$ cd sage
    [user@localhost sage]$ make



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

    [user@localhost sage]$ git remote add trac ssh://git@trac.sagemath.org:2222/sage.git
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
things that you can get from/to the remote server. Your local branch
can have a different name, for example::

    [user@localhost sage]$ git checkout -b my_branch trac/u/user/description
    Branch my_branch set up to track remote branch u/user/description from trac by rebasing.
    Switched to a new branch 'my_branch'

creates a new branch in your local git repository named ``my_branch``
and switches to it. It is based on the remote ``u/user/description``,
so you start out with the same files as in that ticket. You can then
edit files and commit changes to your local branch.

Your local copy of the repository might not yet know about the remote
branch, as somebody else might have added it only recently. In that
case, git will complain that it can't find a matching commit. The
solution is to fetch updates from the remotes first::

    [user@localhost sage]$ git checkout -b my_branch trac/u/user/description
    fatal: Cannot update paths and switch to branch 'my_branch' at the same time.
    Did you intend to checkout 'trac/u/user/description' which can not be resolved as commit?
    [user@localhost sage]$ git fetch trac u/user/description
    From ssh://trac/sage
    * [new branch]      u/user/description -> FETCH_HEAD
    [user@localhost sage]$ git checkout -b my_branch FETCH_HEAD

Note that the ``u/user/description`` branch is temporarily (until you
fetch something else) available under the alias ``FETCH_HEAD`` so you
do not have to type it twice.



.. _section-git-push:

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
master branch. To push your branch to trac use either::

    [user@localhost sage]$ git push --set-upstream trac my_branch:u/user/description

if you started the branch yourself and do not follow any other branch,
or use::

    [user@localhost sage]$ git push my_branch:u/user/description

if your branch already has an upstream branch. The remaining arguments
are 

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
is temporary until `#14480 <http://trac.sagemath.org/14480>`_ is merged
into the ``master`` branch.)

The above git commands create a new remote branch. If you make any
further local edits, then you need a slight variation of the command
to push your changes (but not create a new remote branch). So assume
that you made some further changes to your local branch and committed
them. Then you just have to push a certain commit, either specified by
its hex number or by the abbreviation ``HEAD`` for the most recent
one::

    [user@localhost sage]$ git push trac HEAD:u/user/description


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

    [user@localhost sage]$ git pull

This will download the changes from the originally-used remote branch
and merge them with your local branch.




.. _section-git-merge:

Merging and Rebasing
====================

.. todo::

    Write something



.. _section-git-recovery:

Reset and Recovery
==================

Git makes it very hard to truly mess up. Here is a short way to get
back onto your feet, no matter what. First, if you just want to go
back to a working Sage installation you can always abandon your
working branch by switching to your local copy of the ``build_system``
branch::

    [user@localhost sage]$ git checkout build_system

As long as you did not make any changes to the ``build_system`` branch
directly, this will give you back a working Sage.

If you want to keep your branch but go back to a previous commit you
can use the *reset* command. For this, look up the commit in the log
which is some 40-digit hexadecimal number (the SHA1 hash). Then use
``git reset --hard`` to revert your files back to the previous state::

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
the useful abbreviation ``HEAD~`` for the previous commit and
``HEAD~n``, with some integer ``n``, for the n-th previous commit.

Finally, perhaps the ultimate human error recovery tool is the
reflog. This is a chronological history of git operations that you can
undo if needed. For example, let us assume we messed up the *git
reset* command and went back too far (say, 5 commits back). And, on
top of that, deleted a file and committed that::

    [user@localhost sage]$ git reset --hard HEAD~5
    [user@localhost sage]$ git rm sage
    [user@localhost sage]$ git commit -m "I shot myself into my foot"

Now we cannot just checkout the repository from before the reset,
because it is no longer in the history. However, here is the reflog::

    [user@localhost sage]$ git reflog
    2eca2a2 HEAD@{0}: commit: I shot myself into my foot
    b4d86b9 HEAD@{1}: reset: moving to HEAD~5
    af353bb HEAD@{2}: checkout: moving from some_branch to master
    1142feb HEAD@{3}: checkout: moving from other_branch to some_branch
    ...

The ``HEAD@{n}`` revisions are shortcuts for the history of git
operations. Since we want to rewind to before the erroneous *git
reset* command, we just have to reset back into the future::

    [user@localhost sage]$ git reset --hard HEAD@{2}
    
