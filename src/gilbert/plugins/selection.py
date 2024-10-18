from functools import cached_property
from operator import attrgetter

from gilbert.collection import Collection
from gilbert.content import Content


class Selection(Content):
    """
    A Content type to provide sorted selections of pages / content.
    """

    filter_by: dict = {}
    sort_by: str = "name"
    limit: int = 0

    def select_objects(self, source: Collection) -> list[Content]:
        sort_by = self.sort_by
        reverse = sort_by.startswith("-")
        if reverse:
            sort_by = sort_by[1:]
        key = attrgetter(sort_by)
        items = sorted(
            source.matching(self.filter_by),
            key=key,
            reverse=reverse,
        )
        if self.limit:
            items = items[: self.limit]
        return items

    @cached_property
    def pages(self):
        """
        Apply filtering and sorting to the Site's pages Collection, and return matching objects.
        """
        return self.select_objects(self.site.pages)

    @cached_property
    def content(self):
        """
        Apply filtering and sorting to the Site's content Collection, and return matching objects.
        """
        return self.select_objects(self.site.content)
