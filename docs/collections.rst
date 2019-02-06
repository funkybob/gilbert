***********
Collections
***********

There are two content ``Collections`` used in gilbert: pages, and content.

The only difference is the pages ``Collection`` use the ``Page`` as a default
content type.

Primarily, a ``Collection`` is a dict, with content objects keyed by their
filenames.

You can also query a ``Collection`` for objects of a certain type.

Additionally, a ``Collection`` can build indices of objects according to values
on particular attributes.
