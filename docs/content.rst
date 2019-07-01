*************
Content Types
*************

Content types control how pages and content are interpreted and rendered.

Requirements
============

Gilbert requires Python 3.7 or newer.


Built in Content types
======================

Raw
---

For any content that requires no processing, a ``Raw`` type just copies the
content and name verbatim.


Content
-------

This is the default, generic ``Content`` type for the `content/` directory.

It holds only its name, and any meta-data and/or content passed at its creation.

It can not be rendered as a page.


Page
----

The ``Page`` content type is the default for the `pages/` directory.

When rendered, it will:

1. Find the template to use.

   It will check the `template` key in its data. This can be a single template
   name, or a list of names.  The first found will be used, or it will fall
   back to `default.html`.

2. Build a context

   This is built by the Site, and will include:

   - "site": the site instance
   - "pages": the Pages collection
   - "content": the Content collection
   - "this": this page

3. Generate its output name, which is its own name with the extension replaced
   with '.html'.

   This can be overridden by providing `extension` in the config dict.

4. Render the template, using the context, to the target.

Custom Content Types
====================

You can declare your own content-types easily in your project.  Create a
``plugins.py`` file, and declare them in there.


.. code-block:: python
   :caption: mysite/plugins.py

   import typing
   from datetime import datetime

   from gilbert.content import Templated, Content

   class BlogPost(Templated, Content):
       title: str
       author: str
       posted: typing.Union[None, datetime]
       template: str = "blog/post.html"

Now you can define documents with the content-type of `BlogPost` with these
attributes.

.. code-block:: yaml
   :caption: mysite/content/post.yaml

   content_type: BlogPost
   title: My First Post!
   ---
   Welcome to my blog!


Content Type Mixins
-------------------

In addition, there are provided some mixin classes to help simplify writing
custom plugins.


.. py:class:: Renderable

   .. py:attribute:: extension : Union[str, Sequence[str]]

      The extension to use when writing the output.

   .. py:attribute:: url : str

      The url of this rendered page.

   .. py:attribute:: output_filenamename : str

      The ``Path`` to write output to.

      Default implementation appends the `name` of this object to the
      ``Site.dist_dir`` and replaces its extension with ``extension``.

   .. py:attribute:: content

      Access the objects content.

      Typically implemented as a `oneshot` property.

      Default: ``self.data``.

   .. py:method:: render()

      Called to render this object.

      Writes ``self.content`` to ``self.output_filename``

.. py:class:: Templated(Renderable)

   Base for a class that renders using a template.

   .. py:method:: get_template_names() -> Sequence[str]

      Returns a list of template names.

   .. py:method:: get_template() -> stencil.Template

      Loads the template for this object.

      Default action is to return the first template listed in
      ``get_template_names`` it can load from ``Site.templates``

   .. py:method:: get_context() -> stencil.Context

      Produce the ``stencil.Context`` object to render the template against.

      Default is to return ``Site.get_context(self)``

   .. py:method:: generate_content(target: file)

      Calls ``get_template``
      Calls ``get_contest``
      Renders the template against the context, and write to ``target``.
