Loaders
=======

Content loaders are functions which take a ``pathlib.Path``, and return two
values: `content` and `meta`. `content` is typically a string, where `meta`
must be a dict.

Built in Loaders
----------------

Although ``gilbert`` has only a "raw" loader built in as a fallback, it ships
with several plugins which provide loads for some common cases:

md:

  Loads `.md` files, and provides a dummy meta dict containing only
  ``{content_type: 'MarkdownPage'}``

yaml / yml:

  Loads `.yml` and `.yaml` files. Reads the first document in the file as the
  metadata, and the rest of the file as the content.

scss:

  Loads `.scss` files, and provides a dummy meta dict containing only
  ``{'content_type': 'SCSS'}``
