from operator import attrgetter
from typing import List

from gilbert.collection import Collection
from gilbert.content import Content
from gilbert.utils import oneshot


class Selection(Content):
    """
    A Content type to provide sorted selections of pages / content.
    """

    filter_by: dict = {}
    sort_by: str = "name"
    limit: int = 0

    def select_objects(self, source: Collection) -> List[Content]:
        sort_by = self.sort_by
        reverse = sort_by.startswith("-")
        if reverse:
            sort_by = sort_by[1:]
        key = attrgetter(sort_by)
        items = sorted(source.matching(self.filter_by), key=key, reverse=reverse,)
        if self.limit:
            items = items[: self.limit]
        return items

    @oneshot
    def pages(self):
        """
        Apply filtering and sorting to the Site's pages Collection, and return matching objects.
        """
        return self.select_objects(self.site.pages)

    @oneshot
    def content(self):
        """
        Apply filtering and sorting to the Site's content Collection, and return matching objects.
        """
        return self.select_objects(self.site.content)
