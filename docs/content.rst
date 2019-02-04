*************
Content Types
*************

Content types control how pages and content are interepreted and rendered.


Built in Content types
======================

Raw
---

For any content that requires no processing, a ``Raw`` type just copies the
content and name verbatim.


Content
-------

This is the default, generic ``Content`` type for the `content/` directory.

It holds only its name, and any data and/or content passed at its creation.

It can not be rendered.


Page
----

The ``Page`` content type is the default for the `pages/` directory.

When rendered, it will:

1. Find the template to use.

   It will check the `template` key in its data. This can be a single template
   name, or a list of names.  The first found will be used, or it will fall
   back to `default.html`.

2. Build a context

   This is built by the Site, and will include:

   - "site": the site instance
   - "pages": the Pages collection
   - "content": the Content collection
   - "this": this page

3. Generate its output name, which is its own name with the extension replaced
   with '.html'.

   This can be overridden by providing `extension` in the config dict.

4. Render the template, using the context, to the target.
