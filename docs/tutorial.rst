********************
Quick Start Tutorial
********************

First, we'll create a `virtualenv` and install `gilbert`:

.. code-block:: sh

   $ python3 -m venv venv
   $ . venv/bin/activate
   (venv) $ pip install gilbert

Next, we'll create a project:

.. code-block:: sh

   (venv) $ gilbert --root mysite init

This will create a basic project layout:

.. code-block:: sh

   (venv) $ tree mysite
   mysite/
   ├── content
   ├── dist
   ├── pages
   └── templates

   4 directories, 0 files

Everything from here out will be easier if we're inside the `mysite` directory:

.. code-block:: sh

   (venv) $ cd mysite/

Now, let's create the index page for our new site:

.. code-block:: yaml
   :caption: mysite/pages/index.yaml

   title: Welcome
   ---
   This is my page!

This defines a new ``Content`` object, with config options and content.

If we now try to `render` our site, we'll see the following:

.. code-block:: sh

   (venv) $ gilbert render
   Searching .../gilbert/plugins for plugins...
   Loaded plugin: markdown
   Loaded plugin: yaml
   Loaded plugin: scss
   ValueError: Template for default.html not found: ['default.html']

We need to provide a template to render the page with. Let's do that now:

.. note:: Templates use the stencil_ template engine.

.. code-block:: html
   :caption: mysite/templates/default.html

   <!DOCTYPE html>
   <html>
     <head>
       <title> {{ this:title }} </title>
     </head>
     <body>
     {{ this:content }}
     </body>
   </html>

This time when we render, we'll see:

.. code-block:: sh

   (venv) $ gilbert render
   Searching .../gilbert/plugins for plugins...
   Loaded plugin: markdown
   Loaded plugin: yaml
   Loaded plugin: scss
   Rendering index.yaml ...

We can now look at our new page:

.. code-block:: sh

   (venv) $ $BROWSER dist/index.html


.. _stencil: https://stencil-templates.readthedocs.io/en/latest/
