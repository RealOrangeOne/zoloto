from functools import partial

from hypothesis import strategies

reasonable_image_size = partial(strategies.integers, 100, 2 ** 12)
