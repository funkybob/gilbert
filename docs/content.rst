*************
Content Types
*************

Content types control how pages and content are interpreted and rendered.


Built in Content types
======================

Raw
---

For any content that requires no processing, a ``Raw`` type just copies the
content and name verbatim.


Content
-------

This is the default, generic ``Content`` type for the `content/` directory.

It holds only its name, and any data and/or content passed at its creation.

It can not be rendered.


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

   .. py:method:: get_output_name() -> str

      Returns the ``Path`` to write output to.

      Default implementation appends the `name` of this object to the
      ``Site.dist_dir`` and replaces its extension with ``extension``.

   .. py:method:: generate_content(site : Site)

      Called to generate the objects output.

      Default: returns ``self.content``.

   .. py:method:: render(site: Site)

      Called to render this object.
      Opens the Path returned by ``get_output_name`` and passes it to
      ``generate_content``

.. py:class:: Templated(Renderable)

   Base for a class that renders using a template.

   .. py:method:: get_template_names() -> Sequence[str]

      Returns a list of template names.

   .. py:method:: get_template(site: Site) -> stencil.Template

      Loads the template for this object.

      Default action is to return the first template listed in
      ``get_template_names`` it can load from ``Site.templates``

   .. py:method:: get_context(site: Site) -> stencil.Context

      Produce the ``stencil.Context`` object to render the template against.

      Default is to return ``Site.get_context(self)``

   .. py:method:: generate_content(site: Site, target: file)

      Calls ``get_template``
      Calls ``get_contest``
      Renders the template against the context, and write to ``target``.
