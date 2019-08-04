***********
Config File
***********

Site-wide config options are stored in the root level `config.yml` file.


Options
=======

plugins::
    A list of python imports to load at start.
    These are expected to define and register plugins.

    See :doc:`plugins/index`.

globals::
    A dict of information to be included in the default template context.

    See :doc:`templates`