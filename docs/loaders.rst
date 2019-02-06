Loaders
=======

Content loaders are functions which take a ``pathlib.Path``, and return two
values: `content` and `meta`. `content` is typically a string, where `meta`
must be a dict.

Built in Loaders
----------------

By default, there is a `yaml` load available.

It reads the first document in a YAML file as the configuration ``dict``, and
reads any remaining part of the file as the `content`.
