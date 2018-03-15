#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : wangmengyu
# @File    : paginator.py
# @Software: PyCharm

from math import ceil


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator(object):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        self.object_list = object_list
        self.per_page = int(per_page)
        self.orphans = int(orphans)
        self.allow_empty_first_page = allow_empty_first_page
        self._num_pages = self._count = None

    def validate_number(self, number):
        """Validates the given 1-based page number."""
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def page(self, number):
        """Returns a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return Page(self.object_list[bottom:top], number, self)

    def _get_count(self):
        """Returns the total number of objects, across all pages."""
        if self._count is None:
            try:
                self._count = self.object_list.count()
            except (AttributeError, TypeError):
                # AttributeError if object_list has no count() method.
                # TypeError if object_list.count() requires arguments
                # (i.e. is of type list).
                self._count = len(self.object_list)
        return self._count
    count = property(_get_count)

    def _get_num_pages(self):
        """Returns the total number of pages."""
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(1, self.count - self.orphans)
                self._num_pages = int(ceil(hits / float(self.per_page)))
        return self._num_pages
    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        return range(1, self.num_pages + 1)
    page_range = property(_get_page_range)


class Page(object):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        return list(self.object_list)[index]

    # The following four methods are only necessary for Python <2.6
    # compatibility (this class could just extend 2.6's collections.Sequence).

    def __iter__(self):
        i = 0
        try:
            while True:
                v = self[i]
                yield v
                i += 1
        except IndexError:
            return

    def __contains__(self, value):
        for v in self:
            if v == value:
                return True
        return False

    def index(self, value):
        for i, v in enumerate(self):
            if v == value:
                return i
        raise ValueError

    def count(self, value):
        return sum([1 for v in self if v == value])

    # End of compatibility methods.

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.number + 1

    def previous_page_number(self):
        return self.number - 1

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.per_page * (self.number - 1)) + 1

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page

    def iter_pages(self, left_edge=2, left_current=1,
                   right_current=3, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in xrange(1, self.paginator.num_pages + 1):
            if num <= left_edge or\
                (num > self.number - left_current - 1 and num < self.number + right_current) or\
                num > self.paginator.num_pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


class SQLAlchemyPaginator(Paginator):
    """
    modified by SL at 2014-3-21
    """

    def __init__(self, query, per_page, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, [], per_page, orphans, allow_empty_first_page)
        self.query = query

    def page(self, number):
        """Returns a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        offset = (number - 1) * self.per_page
        # return SQLAlchemyPage(self.query.limit(self.per_page).offset(offset), number, self)
        return Page(self.query.limit(self.per_page).offset(offset).all(), number, self)

    def _get_count(self):
        """Returns the total number of objects, across all pages."""
        if self._count is None:
            self._count = self.query.count()
        return self._count
    count = property(_get_count)


# class SQLAlchemyPage(Page):
#
#     def __init__(self, query, number, paginator):
#         self.query = query
#         self.number = number
#         self.paginator = paginator
#
#     def __len__(self):
#         return self.query.count()
#
#     def __getitem__(self, index):
#         return self.query.get(index)

class ListPaginator(Paginator):
    """
        不使用sql的offset， limit进行分页
    """

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, [], per_page, orphans, allow_empty_first_page)
        self.object_list = object_list

    def page(self, number):
        """Returns a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        offset = (number - 1) * self.per_page

        all_num = self._get_count()
        start = self.per_page * (number - 1)
        # end = start + self.per_page - 1
        # end = end if end < (all_num - 1) else all_num - 1
        end = start + self.per_page
        end = end if end < (all_num - 1) else all_num

        if start == (all_num - 1):
            page_date = [self.object_list[start]]
        elif start >= all_num:
            page_date = []
        else:
            page_date = self.object_list[start:end]

        return Page(page_date, number, self)

    def _get_count(self):
        """Returns the total number of objects, across all pages."""
        if self._count is None:
            self._count = len(self.object_list)
        return self._count
    count = property(_get_count)


def pagination_or_not(query, page=None, per_page=None, default_per_page=None, sql=True):
    """
    如果 page 为 None 表示不使用分页，返回所有查询记录
    如果 page 不为 None 表示使用分页，返回 pagination
    使用模板宏：render_pagination 展示分页组件
    :author SL
    """
    if page:
        per_page = per_page or default_per_page
        if sql:
            paginator = SQLAlchemyPaginator(query, per_page)
        else:
            paginator = ListPaginator(query, per_page)
        page = int(page)
        page = 0 < page <= paginator.num_pages and page or paginator.num_pages
        return paginator.page(page)
    else:
        # return query.all()
        return query


