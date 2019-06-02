from operator import attrgetter

from gilbert.content import Content
from gilbert.utils import oneshot


class Collection(Content):
    '''
    A content type to provide sorted page / content collections by query.
    '''
    filter_by: dict = {}
    sort_by: str = 'name'
    limit: int = 0

    def select_objects(self, source):
        sort_by = self.sort_by
        reverse = sort_by.startswith('-')
        if reverse:
            sort_by = sort_by[1:]
        key = attrgetter(sort_by)
        items = sorted(
            source.matching(self.filter_by),
            key=key,
            reverse=reverse,
        )
        if self.limit:
            items = items[:self.limit]
        return items

    @oneshot
    def pages(self):
        return self.select_objects(self.site.pages)

    @oneshot
    def content(self):
        return self.select_objets(self.site.content)
