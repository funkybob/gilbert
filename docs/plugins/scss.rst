SCSS plugin
===========

A plugin for rendering content using `libsass`_

On Init
-------

No ``init_site`` function.

Loaders
-------

A loader for '.scss' files is registered.

It reads the content as UTF-8, and provides a meta of
``{'content_type': 'SCSS'}``.

Content Types
-------------

Defines the ``SCSS`` content type, which renders its content as SCSS or SASS.

Extra configuration options can be provided in the meta as ``scss_options``,
or will be sourced from the global config. These are passed to `sass.compile`_
as keyword arguments.

Context Providers
-----------------

No Context Providers are registered.


.. _libsass: https://sass.github.io/libsass-python/
.. _sass.compile: https://sass.github.io/libsass-python/sass.html#sass.compile
