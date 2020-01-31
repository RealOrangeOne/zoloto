from unittest import TestCase

from zoloto.utils import cached_method


class CachedMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.counter = 0

    @cached_method
    def increment(self, by: int = 1) -> None:
        self.counter += by

    def test_caches(self) -> None:
        self.assertEqual(self.counter, 0)
        self.increment()
        self.assertEqual(self.counter, 1)
        self.increment()
        self.assertEqual(self.counter, 1)

    def test_passes_args(self) -> None:
        self.assertEqual(self.counter, 0)
        self.increment(2)
        self.assertEqual(self.counter, 2)
        self.increment(2)
        self.assertEqual(self.counter, 2)
