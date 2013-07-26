.. _chapter-workflows:

=======================
Distributed Development
=======================

Git is a tool to exchange commits (organized into branches) with other
developers. As a distributed revision control system, it does not have
the notion of a central server; The Sage trac server is just one of
many possible remote repositories from your point of view. This lets
you use and experiment with different ways to interact with other
developers. In this chapter, we describe some common ways to develop
for Sage.

For simplicity, let us assume two developers (Alice and Bob) are
collaborating on a ticket. The first step of opening the ticket is
always the same, and could be performed by either Alice or Bob or a
third person.





Simple Workflow
===============

.. image:: static/flowchart.svg

1. Alice creates a :ref:`new local branch <section-git-branch>` and
   :ref:`commits <section-git-commit>` changes to the Sage sources.

2. Alice :ref:`uploads her branch <section-git-push>` to the trac
   server and fills in the "Branch:" field with her remote branch name
   ``u/alice/description``.

3. Bob :ref:`downloads Alice's branch <section-git-checkout>`, looks
   through the source, and leaves a comment on the ticket about a
   mistake in Alice's code.

4. Alice fixes the bug on top of her current branch, and uploads the
   updated branch.

5. Bob :ref:`retrieves Alice's updates <section-git-pull>` and reviews
   the changes.

6. Once Bob is satisfied, he sets the ticket to positive review. The
   "Author:" field is set to Alice's full name, and the "Reviewer:"
   field is set to Bob's full name.

Alternatively, Bob might want to make some changes himself. Then,
instead, we would have

3. Bob :ref:`downloads Alice's branch <section-git-checkout>`, makes
   changes, and :ref:`commits <section-git-commit>` them to his local
   branch.

4. Bob :ref:`uploads his branch <section-git-push>` to the trac server
   and fills in the "Branch:" field with his remote branch name
   ``u/bob/description``.

5. Alice :ref:`downloads Bob's branch <section-git-checkout>` and
   reviews his changes.

6. Once Alice is satisfied, she sets the ticket to positive review. If
   both contributions are of comparable size, then the "Author:" and
   "Reviewer:" fields are set to both Alice's and Bob's full name.




Public Repository
=================







GitHub
======

