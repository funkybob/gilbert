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

{% for value in sequence %}

{% endfor %}

Additionally, an ``else`` clause can be included for when the sequence is empty:

{% for valie in sequence %}

{% else %}

{% endfor %}

if
--

{% if expr %}
{% endif %}

{% if not expr %}
{% endif %}

{% if expr %}
{% else %}
{% endif %}

include
-------

Include another template here.

{% include templatename %}

Additionally, extra context may be overlaid:

{% include templatename foo=bar ... %}

load
----

Load a supplementary template extension library.

extends
-------

Defines this template as extending another template, overriding its {% block %} tags.

{% extends templatename %}

block
-----

Defines or overrides a block.

{% block name %}
{% endblock %}

with
----

Temporarily define some extra context.

{% with foo=bar ... %}
{% endwith %}

case
----

A switch/case flow control.

{% case expr %}
{% when value %}
{% else %}
{% endcase %}
