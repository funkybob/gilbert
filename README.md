# Gilbert

Another static site generator.

https://en.wikipedia.org/wiki/William_Gilbert_(astronomer)


# Quick Start

Install gilbert:

    $ pip install gilbert

Create a gilbert project:

    $ gilbert --root mysite init

Create page files in mysite/pages/

Render your site:

    $ gilbert --root mysite render


# Project contents:

Each project contains 4 directories:

1. templates/

   These are templates available to Content Objects, using the `stencil` template system.

2. pages/

   This is the hierarchy of pages to be rendered on the site.

3. content/

   This contains other content objects to be made available to all pages on the site to include in their templates.

4. dist/

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
