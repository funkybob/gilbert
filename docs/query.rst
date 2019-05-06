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
