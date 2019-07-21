***********
Collections
***********

There are two content ``Collections`` used in gilbert: pages, and content.

The only difference is the pages ``Collection`` uses the ``Page`` as a default
content type.

Primarily, a ``Collection`` is a dict, with content objects keyed by their
filenames. Unlike a dict, iterating a ``Collection`` will iterate its values.

You can also query a ``Collection`` for objects of a certain type using the
``Collection.matching`` method.  See :doc:`query` for more details on the
query syntax.
