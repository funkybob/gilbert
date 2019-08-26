Selection plugin
================

``gilbert.plugins.selection``

On Init
-------

No ``init_site`` function.

Loaders
-------

No loader is registered.

Content Types
-------------

Defines a ``Selection`` content type.

This type is not renderable.

.. py:class:: Selection(Content)

    .. py:attribute:: filter_by: dict = {}

        Uses the :doc:`/query` syntax to define a filter for which objects
        should be in this selection.

    .. py:attribute:: sort_by: str = 'name'

        The field to order matching objects by.

    .. py:attribute:: limit: int = 0

        Maximum number of objects to return.

        Use 0 for unlimited.

    .. py:attribute:: pages

        Yields a list of content objets from ``Site.pages`` matching the query.

    .. py:attribute:: content

        Yields a list of content objets from ``Site.content`` matching the
        query.

Context Providers
-----------------

No Context Providers are registered.
