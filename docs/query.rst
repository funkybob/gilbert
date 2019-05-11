Object Queries
--------------

The query language is a very basic adatpation of S-expressions. It uses the
following format:

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

    Any page where the "name" is "index.yml" and its "tags" contains a
    "in-menu" value.

Supported operators:

.. code-block:: yaml

   - attr: ["name"]  # obj.name

.. code-block:: yaml

   - all:  # all(...)
     -
     -
     -

.. code-block:: yaml

   - any:  # any(...)
     -
     -
     -

.. code-block:: yaml

   - not:

.. code-block:: yaml

   - lt:  # Also le, eq, ne, ge, gt
     - left
     - right

.. code-block:: yaml

   - startswith:
     - value
     - prefix

.. code-block:: yaml

   - contains:
     - value
     - content
