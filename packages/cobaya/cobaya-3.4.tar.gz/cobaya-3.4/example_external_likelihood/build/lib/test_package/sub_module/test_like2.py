from test_package import TestLike


class TestLike2(TestLike):
    pass


class test_like2(TestLike2):
    # this one inherits yaml from TestLike2 since no explicit .yaml provided
    pass
