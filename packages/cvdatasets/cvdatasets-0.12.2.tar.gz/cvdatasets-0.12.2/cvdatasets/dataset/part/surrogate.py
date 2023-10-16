import enum
import numpy as np

from cvdatasets import utils
from skimage.transform import resize

class SurrogateType(enum.Enum):

	BLANK = enum.auto()
	MIDDLE = enum.auto()
	IMAGE = enum.auto()

	DEFAULT = MIDDLE

	def __call__(self, im, w, h, dtype=np.uint8):
		im = utils.asarray(im)
		if self is SurrogateType.BLANK:
			return self._blank(im, w, h, dtype=dtype)

		elif self is SurrogateType.IMAGE:
			return self._image(im, w, h, dtype=dtype)

		elif self is SurrogateType.MIDDLE:
			return self._middle(im, w, h, dtype=dtype)

		else:
			raise ValueError("Unknown surrogate method: {}".format(self))

	def _blank(self, im, w, h, dtype):
		_, _, c = utils.dimensions(im)
		return np.zeros((h, w, c), dtype=dtype)

	def _image(self, im, w, h, dtype):
		_part_surrogate = resize(im, (h, w),
			mode="constant",
			anti_aliasing=True,
			preserve_range=True)
		return _part_surrogate.astype(dtype)

	def _middle(self, im, w, h, dtype):
		im_h, im_w, c = utils.dimensions(im)

		middle_x, middle_y = im_w // 2, im_h // 2

		x0 = middle_x - w // 2
		y0 = middle_y - h // 2

		return im[y0: y0+h, x0: x0+w]

