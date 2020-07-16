from unittest import TestCase

from zoloto.utils import cached_method, encode_as_json


class CachedMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.counter = 0

    @cached_method
    def increment(self) -> None:
        self.counter += 1

    def test_caches(self) -> None:
        self.assertEqual(self.counter, 0)
        self.increment()
        self.assertEqual(self.counter, 1)
        self.increment()
        self.assertEqual(self.counter, 1)


def test_encode_as_json() -> None:
    assert encode_as_json([1, 2, 3]) == "[1,2,3]"
