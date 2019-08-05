Markdown plugin
===============

``gilbert.plugins.markdown``

A plugin for rendering content using `markdown2`_.

On Init
-------

No ``init_site`` function.

Loaders
-------

A loader for '.md' files is registered. It returns the files content, with
meta data as ``{'content_type': 'MarkdownPage}``.

Content Types
-------------

Registers a ``MarkdownPage`` which interprets its content as markdown.

If an ``extras`` option is provided, it is passwd to ``markdown2`` as the
`extensions <markdown2-extra>`_ argument.

Context Providers
-----------------

No Context Providers are registered.


.. _markdown2: https://github.com/trentm/python-markdown2

.. _markdown2-extra: https://github.com/trentm/python-markdown2#extra-syntax-aka-extensions
