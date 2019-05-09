from operator import attrgetter

from gilbert.content import Content
from gilbert.utils import oneshot


class Collection(Content):
    '''
    A content type to provide sorted page / content collections by query.
    '''
    filter_by: dict = {}
    sort_by: str = 'name'

    @oneshot
    def pages(self):
        sort_by = self.sort_by
        reverse = sort_by.startswith('-')
        if reverse:
            sort_by = sort_by[1:]
        key = attrgetter(sort_by)
        return sorted(
            self.site.pages.matching(self.filter_by),
            key=key,
            reverse=reverse,
        )

    @oneshot
    def content(self):
        sort_by = self.sort_by
        reverse = sort_by.startswith('-')
        if reverse:
            sort_by = sort_by[1:]
        key = attrgetter(sort_by)
        return sorted(
            self.site.content.matching(self.filter_by),
            key=key,
            reverse=reverse,
        )
