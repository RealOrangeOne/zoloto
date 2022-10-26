from __future__ import annotations

from unittest import TestCase

import pytest

from zoloto.utils import cached_method, parse_ranges


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


@pytest.mark.parametrize(
    "case",
    [
        ("1", {1}),
        ("1,4", {1, 4}),
        ("1, 4", {1, 4}),
        ("1-4", {1, 2, 3, 4}),
        ("1-4,2-5", {1, 2, 3, 4, 5}),
        ("1-4,6,0", {0, 1, 2, 3, 4, 6}),
    ],
)
def test_parse_ranges(case: tuple) -> None:
    range_str, expected = case
    actual = parse_ranges(range_str)
    assert actual == expected
