Template Helpers
================

The ``Stencil`` template engine can access any functions inside its context to apply when generating content.

This recipe will show how to add an "excerpt" filter to let you show a short introduction to blog posts in your list pages.

Steps
-----

1. Write helper function
------------------------

First, we write a function in our ``plugins.py`` to preform the needed work:

.. code-block:: python

    from lxml import html

    from stencil import SafeStr

    def excerpt(content, length):
        '''
        HTML-Safe trimming of content to a fixed number of blocks.

        Ensures all tags are properly closed.
        '''
        fragments = html.fromstring(content)
        return SafeStr(''.join(html.tostring(x, encoding='unicode') for x in fragments[:length]))

2. Register it on site load
---------------------------

Next, we need to register an event callback to add our function to the context when a render creates a template context:

.. code-block:: python

    from gilbert import Site

    @Site.register_context_provider
    def global_context(ctx):

        ctx['excerpt'] = excerpt

        return ctx

3. Use it in a template!
------------------------

Finally, we can call the function in our templates:

.. code-block:: html

    <article>
      <header>
        <h1><a href="{{ post.url }}">{{ post.title }}</a></h1>
      </header>
      <p>{{ excerpt(post.content, 3) }}</p>
    </article>

