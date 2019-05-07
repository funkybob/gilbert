Object Queries
--------------

The query language uses the following format:

.. code-block:: yaml

   filter_by:
     - and:
       - eq:
         - attr: ["name"]
         - "index.yml"
       - contains:
         - attr: ["tags"]
         - "in-menu"

This would translate to:

    Any page where the "name" is "index.yml" and its "tags" contains a "in-menu" value.

Supported operators:

- attr: look up an attribute

.. code-block:: yaml

   - attr: ["name"]  # obj.name

   - all:  # all(...)
     -
     -
     -

   - any:  # any(...)
     -
     -
     -

   - not:

   - lt:  # Also le, eq, ne, ge, gt
     - left
     - right

   - startswith:
     - value
     - prefix

   - contains:
     - value
     - content
