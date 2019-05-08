# Gilbert

Another static site generator.

https://en.wikipedia.org/wiki/William_Gilbert_(astronomer)

This README contains a brief introduction to the project. Full documentation [is available here](https://gilbert.readthedocs.io/en/latest/).

# Quick Start

Install gilbert: (** Not currently published **)

    $ pip install gilbert

Or install from GitHub:

    $ pip install git+https://github.com/funkybob/gilbert.git

Create a gilbert project:

    $ gilbert --root mysite init

(You can omit `--root` if it's the current directory.)

Create page files in mysite/pages/

Render your site:

    $ gilbert --root mysite render

Have gilbert watch your files, and re-render on changes:

    $ gilbert --root mysite watch

Finally, list all loaders and plugins:

    $ gilbert --root mysite plugins

# Project contents:

Each project contains 4 directories:

1. templates/

   These are templates available to Content Objects, using the `stencil` template system.

2. pages/

   This is the hierarchy of pages to be rendered on the site.

3. content/

   This contains other content objects to be made available to all pages on the site to include in their templates.

4. docs/

   This is where the site distributable content are rendered into.


# Content Objects

Content objects are basically YAML files, with a single YAML document, optionally followed by additional raw content.

The default Content Object is `Data` which simply provides access to the data in the YAML document.

The `Page` content object is the default type for documents in the `pages/` collection. It will render using the template defined in its data, or the 'default.html' template.


# Plugins

Gilbert supports auto-discovered plugins. They simply need to be packages existing in the namespaced package 'gilbert.plugins'.

By default, the following Plugins are provided:

1. yaml

   Registers a loader for .yml and .yaml files.

2. markdown

   An extension of `Page` which renders its `content` using Markdown

3. scss

   Renders its content using SCSS
