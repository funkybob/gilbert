*******
Plugins
*******

When a `Site` is instantiated, it will try to load all plugins.

Plugins are any packages in the `gilbert.plugins` namespaced package.


Default plugins
===============

Gilbert comes with some plugins by default.

markdown
--------

The ``markdown`` plugin provides a ``MarkdownPage`` content type, and a loader for `.md` files.

The `.md` loader reads the files contents, and returns a dict with a single key of `content_type` as ``MarkdownPage``.

The ``MarkdownPage`` class takes a config dict and contents. It renderse the content using the ``markdown2`` package.

scss
----

The ``scss`` plugin provides a `SCSS` content type, and a loader for `.scss` files.

The `.scss` loader reads the files contents, and returns a dict with a single key of `content_type` as ``SCSS``.

The ``SCSS`` class takes a config dict and contents. It renders the contents using the ``PySCSS`` package.

If the config dict contains a `scss_options` key, it is passed to the ``PySCSS`` Compiler as keyword arguments.

Writing your own Plugins
========================

Gilbert leverages Python's "namespaced packages" (as per PEP 420) to implement plugins.

To provide a plugin in your package, you need to create empty directories for `gilbert` and `gilbert/plugins`; by "empty" I mean no __init__.py.

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

New Content Types can be created by sub-classing the `gilbert.content.Content` class.

This will register the class by its name.

Adding a loader
---------------

New file type loaders can be registered with the `gilbert.collection.Collection` class using the `Collection.register` classmethod.

The following example will register a handler for files with a `.toml` extension:

.. code-block:: python

   from gilbert.collection import Collection

   def load_toml(path: Path):
       data = toml.load(path.open())

       return data

    Collection.register('toml')


A loader should return a list of arguments to be passed to a Content object.

The first argument is expected to be a dict, possibly including a key 'content_type' indicating which Content class to use.
