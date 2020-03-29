Menu
====

A ``Selection`` is an easy solution to building a navigation menu.

Steps
-----

1. Add an 'in_nav' attribute to pages you want to appear in the menu.
2. Create a ``Selection`` in your ``content`` directory.
3. Add it to your template.

1. Add attributes
-----------------

.. code-block:: yaml

   in_menu: True
   ---
   Some page!

2. Create a ``Selection``
--------------------------

Add the ``selection`` plugin to ``config.yml``:

.. code-block:: yaml

   plugins:
     - gilbert.plugins.selection


Next, add a menu object to your ``content`` directory:

.. code-block:: yaml
   :caption: content/menu.yml

   content_type: Selection
   filter_by:
     - attr: ['in_menu']

This filter will select any object with the ``in_menu`` attribute having a
"truthy" value.

3. Add it to your template
--------------------------

Finally you can add something like the following to render your menu in your
page:

.. code-block:: html

   <ul>
   {% for page in site.content['menu.yml'].pages %}
     <li><a href="{{ page.url }}">{{ page.title }}</a></li>
   {% endfor %}
   </ul>


Added features
--------------

Instead of setting ``in_menu`` to `True`, you could assign a value and order
by it to ensure consistent ordering.

.. code-block:: yaml
   :caption: content/menu.yml

   content_type: Selection
   filter_by:
     - attr: ['in_menu']
   sort_by: in_menu