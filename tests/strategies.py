from functools import partial

from hypothesis import strategies

from zoloto.marker_type import MAX_ALL_ALLOWED_ID, MarkerType

reasonable_image_size = partial(strategies.integers, 100, 2**12)
marker_types = partial(strategies.sampled_from, MarkerType)
marker_ids = partial(strategies.integers, 0, MAX_ALL_ALLOWED_ID)
