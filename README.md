# Gilbert

Another static site generator.

https://en.wikipedia.org/wiki/William_Gilbert_(astronomer)

This README contains a brief introduction to the project. Full documentation
[is available here](https://gilbert.readthedocs.io/en/latest/).

# Quick Start

Install gilbert:

    $ pip install gilbert

Create a gilbert project:

    $ gilbert --root mysite init

(You can omit `--root` if it's the current directory.)

Create page files in mysite/pages/

Render your site:

    $ gilbert --root mysite render

Have gilbert serve your site:

    $ gilbert --root mysite serve

Serve your site and re-render on changes:

    $ gilbert --root mysite serve --watch

Finally, list all loaders and plugins:

    $ gilbert --root mysite plugins


## Installation requirements

Gilbert current requires Python 3.7 or greater.
