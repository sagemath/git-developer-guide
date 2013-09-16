.. _chapter-walk-through:

========================
Sage Development Process
========================

This section is a concise overview of the Sage development process. In
it, we will see how to make changes to the Sage source code and
communicate these changes back to the Sage project. If you are a
beginner to Sage development, this introductory guide is here to help
you become familiar with the Sage development process.

Sage comes with a set of developer scripts, which help you with common
interactions with the bug tracker (see :ref:`chapter-sage-trac`) and
with handling revisions of your code. The developer scripts use the
git distributed revison control system under the hood which you'll
have to install (see :ref:`chapter-git-setup`), but you do not need to
know anything about it (see :ref:`chapter-manual-git` only if you want
to).

Most of the commands in the following section will not work unless you have an
account on the bug tracker. If you want to contribute to Sage, it is a good
idea to get an account now (see :ref:`section-trac-account`).

We assume here that the ``sage`` executable of your development installation of
Sage is in your ``PATH``. If this is not the case, you might have to replace
``sage`` by ``./sage`` in the following (assuming you are in the sage root
directory). You can also use the developer scripts from the Sage prompt. All
commands to ``sage -dev`` are available as methods on the global ``dev``
object, e.g., the equivalent of ``sage -dev switch-ticket 12345`` would be
``dev.switch_ticket(12345)``.

.. warning::

	In the transitional period it can happen that you end up on a branch where
	the developer scripts are not available or outdated. If this is the case,
	i.e., if ``sage -dev`` does not work properly anymore:

	* Go to http://trac.sagemath.org/14482
	* Note the branch field on the ticket, e.g., ``u/saraedum/ticket/14482``
	* Run ``git pull git://trac.sagemath.org/sage.git u/saraedum/ticket/14482``
	  to add the latest version of the developer scripts to your branch

.. _section-walkthrough-add:

Adding to the Sage Sources
==========================

Suppose you have written an algorithm for calculating the last twin prime, and
want to add it to Sage. You would first open a ticket for that::

    sage -dev create-ticket

This will give you an editor in which you can give a summary and a description
of what you want to do. If you are not sure which values to put for the other
fields, you can leave the defaults or have a look at
:ref:`section-trac-fields`. After you close the editor, a new ticket will be
opened on the trac server. From that point on, everyone can see what you intend
to do, which is very useful for avoiding double work.

If you want to cancel the creation of a ticket, then you can just save an empty
file. This will abort the operation.

After saving your ticket on the trac server, a branch will be created for you.
A branch is essentially a named container to store your modifications to the
Sage source code. Your new branch is now called ``ticket/<TICKETNUM>``. Unless
you upload it (see below), it will only be on your local system and not visible
to anyone else.

At this point, you will start editing the source code, trying it out, running
doctests, et cetera. At some point, you may wish to share your changes with the
rest of us: maybe it is ready for review, or maybe you are collaborating with
someone and want to share your changes "up until now".

The first step is to record your changes into your branch::

    sage -dev commit

You will be asked to write a message describing your changes. It is common to
write a one line summary, then a blank line, and then a 1 - 2 paragraph
explanation of your changes. (Of course, if your changes are minor, then just
the one-line summary can be enough.)

The next step is to upload your changes to Trac::

    sage -dev upload

On trac, your branch will be called ``u/<USERNAME>/ticket/<TICKETNUM>``.
Additionally, this will set the Branch field on the ticket to point to this
branch. This way, other people know where to find your work.

It is common to go through some iterations of ``sage -dev commit`` before you
upload, and you will probably also have uploaded a few times before your
changes are ready for review.

If you are happy with the changes you uploaded, you want somebody else to
review them, so they can be included into the next version of Sage. If your
ticket is ready for review, run::

	sage -dev edit-ticket

This will give you an editor in which you can edit the ticket. Change the
status to::

	Status: needs_review

And add yourself as an author for that ticket by inserting the following as the
first line::

	Authors: Your Real Name

If you want to add an additional comment for potential reviewers, run::

	sage -dev add-comment

.. _section-walkthrough-review:

Reviewing
=========

Now suppose you want to review the existing work on a ticket, such as the one
you created in the last section.  For definiteness, suppose you want to review
#12270. You would do that as follows::

    sage -dev switch-ticket 12270

This command will download the branch on Trac in case you do not have any local
work on ticket 12270. (If you do, you may have to merge your changes; see
below). You can now test the ticket; you'll probably want to call ``make`` or
``sage -b``.

Your will want to add a comment to the ticket as part of your review::

    sage -dev add-comment

This will open a text editor in which you can type, and upload the result to Trac.
    
It is also possible that you make some changes to the code as part of your review. After
you've done that, you can upload your changes back to trac::

    sage -dev commit
    sage -dev upload

This will update the ticket to now point to your branch, including your changes. Your branch
is based on the original author's branch, so s/he can easily incorporate your changes into his/her
own branch (see below).


.. _section-walkthrough-collaborate:

Collaboration
=============

It is very easy to collaborate by just going through the above steps any number of times::

    # developer 1
    <EDIT EDIT>
    sage -dev commit
    sage -dev upload
    # developer 2
    sage -dev download
    <EDIT EDIT>
    sage -dev commit
    sage -dev upload
    # developer 1
    sage -dev download
    <EDIT EDIT>
    sage -dev commit
    sage -dev upload
    (etc)

The obvious problem is when you both work on the same ticket simultaneously::

    # developer 1
    <EDIT EDIT>
    sage -dev commit
    sage -dev upload
    # developer 2
    <EDIT EDIT>
    sage -dev commit
    sage -dev upload
    Changes not compatible with remote branch u/<developer1>/ticket/12270; consider downloading first. Are you sure you want to continue?

Developer 2 should probably select ``No``, and do as suggested::

    sage -dev download

This will try to merge the changes developer 1 made into the ones that developer 2 made. The latter should check whether
all seems okay, and if so, upload the changes::

    sage -dev upload   # works now

It is possible that the changes cannot be automatically merged. In
that case, developer 2 will have to do some manual fixup after
downloading and before uploading::

    <EDIT EDIT FOR FIXUP>
    sage -dev commit
    sage -dev upload


