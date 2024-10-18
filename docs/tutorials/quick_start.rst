********************
Quick Start Tutorial
********************

.. caution:: Remember, ``gilbert`` requires Python 3.12

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
   ├── config.yml
   ├── content
   ├── docs
   ├── pages
   └── templates

   4 directories, 1 file

Everything from here out will be easier if we're inside the `mysite` directory:

.. code-block:: sh

   (venv) $ cd mysite/

Now, let's create the index page for our new site:

.. code-block:: yaml
  :caption: mysite/pages/index.yaml

   title: Welcome
   ---
   This is my page!

This defines a new ``Content`` object, with information _about_ the page (the
meta-data) before the `---` line, and content after.

If we now try to `render` our site, we'll see the following:

.. code-block:: sh

   (venv) $ gilbert render
   Found 0 content objects.
   Found 1 pages.
   Rendering index.yaml ...
   -- Done.

And in our `docs/` folder we'll find `index.yaml`. Not what we wanted. This is
becaues we haven't enabled the YAML plugin. Without it, Gilbert will treat the
file as raw data, and just copy it across.

First, let's clean up our mistake. You can clear the `docs` directory using
the `clean` command:

    (venv) $ gilbert clean

Now, let's configure that plugin. If you open the `config.yml` file in your
editor you will see something like:

.. code-block:: yaml
   :caption: mysite/config.yml

   global: {}
   plugins: []

We can add the YAML plugin as follows:

.. code-block:: yaml
   :caption: mysite/config.yml
   :emphasize-lines: 2,3

   global: {}
   plugins:
     - gilbert.plugins.yaml

Let's try rendering again:

.. code-block:: sh

   (venv) $ gilbert render
   Loaded plugin: gilbert.plugins.yaml
   Found 0 content objects.
   Found 1 pages.
   Rendering index.yaml ...
   Template for default.html not found: ['default.html']

We need to provide a template to render the page with. Let's do that now:

.. note:: Templates use the stencil_ template engine.

.. code-block:: html
  :caption: mysite/templates/default.html

   <!DOCTYPE html>
   <html>
     <head>
       <title> {{ this.title }} </title>
     </head>
     <body>
       {{ this.content }}
     </body>
   </html>

This time when we render, we'll see:

.. code-block:: sh

  (venv) $ gilbert render
  $ gilbert render
  Loaded plugin: gilbert.plugins.yaml
  Found 0 content objects.
  Found 1 pages.
  Rendering index.yaml ...
  -- Done.

We can now look at our new page:

.. code-block:: sh

   (venv) $ gilbert serve

And point your browser at http://localhost:8000/

Helpfully, ``gilbert`` will rebuild automatically as you change files.

.. _stencil: https://stencil-templates.readthedocs.io/en/latest/
