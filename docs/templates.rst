=========
Templates
=========


Expressions
===========

In block and var tags, a subset of Python syntax is supported.

Literals:

.. code-block:: python

   {{ "foo" }}
   {{ 1 }}
   {{ 24.96 }}

Attribute lookup:

.. code-block:: python

   {{ foo.bar }}

Subscript lookup:

.. code-block:: python

   {{ foo[bar] }}
   {{ foo["bar"] }}
   {{ foo[1] }}

Function calls:

.. code-block:: python

   {{ foo() }}
   {{ foo(bar, 1.4, "test") }}


And these actions can be chained:

.. code-block:: python

   {{ foo['test'].bar(1).baz }}


Block tags
==========

for
---

Allows for repeating a portion of the template over a sequence:

.. code-block:: html

   {% for value in sequence %}
   ...
   {% endfor %}

Additionally, an ``else`` clause can be included for when the sequence is empty:

.. code-block:: html

   {% for value in sequence %}
   ...
   {% else %}
   ...
   {% endfor %}

if
--

.. code-block:: html

   {% if expr %}
   ...
   {% endif %}

   {% if not expr %}
   ...
   {% endif %}

   {% if expr %}
   ...
   {% else %}
   ...
   {% endif %}

include
-------

Include another template here.

.. code-block:: html

   {% include templatename %}

Additionally, extra context may be overlaid:

.. code-block:: html

   {% include templatename foo=bar ... %}

extends
-------

Defines this template as extending another template, overriding its {% block %} tags.

.. code-block:: html

   {% extends templatename %}

block
-----

Defines or overrides a block.

.. code-block:: html

   {% block name %}
   ...
   {% endblock %}

with
----

Temporarily define some extra context.

.. code-block:: html

   {% with foo=bar ... %}
   ...
   {% endwith %}

case
----

A switch/case flow control.

.. code-block:: html

   {% case expr %}
   {% when value %}
   ...
   {% when value %}
   ...
   {% else %}
   ...
   {% endcase %}
