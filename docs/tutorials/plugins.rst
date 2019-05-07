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

Since this will be rendered using a template, we also need to include the
``Templated`` mixin, and specify a default ``template`` attribute.

.. code-block:: python
   :caption: plugins.py
   :linenos:

   from gilbert.content import Content, Templated


   class TagCloud(Templated, Content):
       template = 'tag_cloud.html'

Next, we need to gather all the content objects and aggregate the tags.

.. code-block:: python
   :caption: plugins.py
   :linenos:

   from collections import Counter

   from gilbert.content import Content, Templated


   class TagCloud(Templated, Content):
       template = 'tag_cloud.html'

       def get_context(self):
           tags = Counter()
           for obj in site.content:
               tags.update(obj.tags)
           return site.get_context(self, tag_cloud=tags)

And that's it!

Oh, but wait - maybe we don't want to count _all_ the objects? Let's add a
filter.

.. code-block:: python
   :caption: plugins.py
   :linenos:
   :emphasize-lines: 8,12

   from collections import Counter

   from gilbert.content import Content, Templated

   class TagCloud(Templated, Content):
       template = 'tag_cloud.html'

       filter_by : dict = {}

       def get_context(self):
           tags = Counter()
           for obj in self.site.content.matches(self.filter_by):
               tags.update(obj.tags)
           return self.site.get_context(self, tag_cloud=tags)

Now our users can declare a filter using :doc:`/query` to limit which objects
will be scanned.

This is nice, but as our site grows, collecting these each time we render will
start to get expensive.

.. code-block:: python
   :caption: plugins.py
   :linenos:
   :emphasize-lines: 4,5,12-14

   from collections import Counter

   from gilbert.content import Content, Templated
   from gilbert.query import Query
   from gilbert.utils import oneshot

   class TagCloud(Templated, Content):
       template = 'tag_cloud.html'

       filter_by : dict = {}

       @oneshot
       def tag_counts(self):
           tags = Counter()
           for obj in self.site.pages.matching(self.filter_by):
               tags.update(obj.tags)
            return tags

       def get_context(self):
           return self.site.get_context(self, tag_cloud=self.tag_counts)

So here we introduce the ``oneshot`` utility decorator, which works like
``property`` but caches the result so it only invokes the function once.
