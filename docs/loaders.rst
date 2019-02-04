Loaders
=======

Content loaders are functions which take a ``pathlib.Path``, and return a list of arguments for a ``Content`` class.

The first returned argument must be a ``dict``, which may include a `content_type` key naming the ``Content`` class to use for this object.

The base ``Content`` class takes 2 arguments: data, and content.

Built in Loaders
----------------

By default, there is a `yaml` load available.

It reads the first document in a YAML file as the configuration ``dict``, and reads any remaining part of the file as the `content`.
