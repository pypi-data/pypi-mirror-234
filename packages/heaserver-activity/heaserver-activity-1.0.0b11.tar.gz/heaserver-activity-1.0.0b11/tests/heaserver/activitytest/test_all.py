from .testcase import TestCase, RecentlyAccessedViewsByTypeTestCase
from heaserver.service.testcase.mixin import GetOneMixin, GetAllMixin


class TestGet(TestCase, GetOneMixin):
    pass


class TestGetAll(TestCase, GetAllMixin):
    pass

class TestRecentlyAccessedGetAll(RecentlyAccessedViewsByTypeTestCase, GetAllMixin):
    pass
