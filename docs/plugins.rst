*******
Plugins
*******

When a `Site` is instantiated, it will try to load all plugins.

Plugins are any packages in the `gilbert.plugins` namespaced package.


Default plugins
===============

Gilbert comes with some plugins by default.

yaml
----

The ``yaml`` plugin registers a ``loader`` for `.yml` and `.yaml` files.

markdown
--------

The ``markdown`` plugin provides a ``MarkdownPage`` content type, and a loader
for `.md` files.

The `.md` loader reads the files contents, and returns a dict with a single key
of `content_type` as ``MarkdownPage``.

The ``MarkdownPage`` class takes a config dict and contents. It renders the
content using the ``markdown2`` package.

scss
----

The ``scss`` plugin provides a `SCSS` content type, and a loader for `.scss`
files.

The `.scss` loader reads the files contents, and returns a dict with a single
key of `content_type` as ``SCSS``.

The ``SCSS`` class takes a config dict and contents. It renders the contents
using the ``PySCSS`` package.

If the config dict contains a `scss_options` key, it is passed to the
``PySCSS`` Compiler as keyword arguments.

collection
----------

The ``collection`` plugin provides a `Collection` content type for defining
collections of pages or content objects.


Writing your own Plugins
========================

Gilbert leverages Python's "namespaced packages" (as per PEP 420) to implement
plugins.

To provide a plugin in your package, you need to create empty directories for
`gilbert` and `gilbert/plugins`; by "empty" I mean no __init__.py.

Then, inside the plugins directory, create your plugins package directory.

.. code-block:: sh

   + gilbert/
     |
     + plugins/
       |
       + mything/
         |
         + __init__.py

Adding a Content Type
---------------------

New Content Types can be created by sub-classing the `gilbert.content.Content`
class.

This will register the class by its name.

Adding a loader
---------------

New file type loaders can be registered with the `gilbert.site.Site` class
using the `Site.register_loader` classmethod.

The following example will register a handler for files with a `.toml`
extension:

.. code-block:: python

   from gilbert import Site

   def load_toml(path: Path):
       data = toml.load(path.open())

       return '', data

    Site.register_loader('toml', load_toml)


A loader must return two values: `content`, and `meta`.

The first argument is expected to be a dict, possibly including a key
'content_type' indicating which Content class to use.

Extending the Context
---------------------

Plugins can also register a ``Context Provider``. These are called in turn by
the ``Site.get_context`` method to update the ``Context``.

A ``Context Provider`` is a callable that accepts a context dict, and returns
an updated context dict.

The following example will register a ``Context Provider`` that adds the
current time:

.. code-block:: python

    from datetime import datetime

    from gilbert import Site

    def add_datetime(ctx):
        ctx['current_time'] = datetime.now()
        return ctx

    Site.register_context_provider(add_datetime)
