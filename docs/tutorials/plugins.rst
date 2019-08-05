=======
Plugins
=======

In this tutorial we're going to build a Tag Cloud content object. It will
provide a way to inject counts of how many times tags appear on selected
objects.

We start by creating a ``plugins.py`` in our project, and declaring
``TagCloud`` as a sub-class of `gilbert.content.Content`:

.. code-block:: python
   :caption: plugins.py
   :linenos:

   from gilbert.content import Content


   class TagCloud(Content):
       pass

Next, we need to gather all the content objects and aggregate the tags.

.. code-block:: python
   :caption: plugins.py
   :linenos:

   from collections import Counter

   from gilbert.content import Content


   class TagCloud(Content):

       @property
       def tag_counts(self):
           tags = Counter()
           for obj in self.site.content:
               tags.update(obj.tags)
           return tags

And that's it! We can create a content object with `content_type: TagCloud`,
and access it in our templates by looking it up in ``site.content[]``, and
accessing its ``tag_counts`` property.

Oh, but wait - maybe we don't want to count *all* the objects? Let's add a
filter.

.. code-block:: python
   :caption: plugins.py
   :linenos:
   :emphasize-lines: 6,11

   from collections import Counter

   from gilbert.content import Content

   class TagCloud(Content):
       filter_by : dict = {}

       @property
       def tag_counts(self):
           tags = Counter()
           for obj in self.site.content.matches(self.filter_by):
               tags.update(obj.tags)
           return tags

Now our users can declare a filter using :doc:`/query` to limit which objects
will be scanned.

This is nice, but as our site grows, collecting these each time we render will
start to get expensive.

.. code-block:: python
   :caption: plugins.py
   :linenos:
   :emphasize-lines: 4,9

   from collections import Counter

   from gilbert.content import Content
   from gilbert.utils import oneshot

   class TagCloud(Content):
       filter_by : dict = {}

       @oneshot
       def tag_counts(self):
           tags = Counter()
           for obj in self.site.pages.matching(self.filter_by):
               tags.update(obj.tags)
            return tags

So here we introduce the ``oneshot`` utility decorator, which works like
``property`` but caches the result so it only invokes the function once,
saving the result on the instance; future accesses are super fast as they're
handled internally within Python.
