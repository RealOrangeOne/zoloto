from functools import partial

from hypothesis import strategies

reasonable_image_size = partial(strategies.integers, 10, 2 ** 10)
