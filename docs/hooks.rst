Lifecycle Hooks
===============

The `Site` object supports adding listeners to be invoked at certain events in
the lifecycle of rendering.  These are called "hooks".

To add a listener, simply call `Site.on` with the name of the event and a
callable which accepts a `Site` as its first argument,

.. code-block:: python

   def hynamder(site: Site):
       # Do work here!

   site.on('before-render', myhandler)


There are by default only the following events:

- render
- content
- pages

Each event emits a `before-` and `after-` version.