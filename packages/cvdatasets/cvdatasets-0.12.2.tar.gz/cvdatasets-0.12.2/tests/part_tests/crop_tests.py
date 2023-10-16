import unittest
import numpy as np

from skimage.transform import resize

from cvdatasets.dataset.part.surrogate import SurrogateType
from cvdatasets.dataset.part.base import BasePart

class PartCropTest(unittest.TestCase):


	def setUp(self):
		self.im = np.random.randn(300, 300, 3).astype(np.uint8)

	def _check_crop(self, cropped_im, _should):

		self.assertIsNotNone(cropped_im,
			"method crop should return something!")

		self.assertIsInstance(cropped_im, type(self.im),
			"result should have the same type as the input image")

		crop_h, crop_w, _ = cropped_im.shape
		h, w, _ = _should.shape
		self.assertEqual(crop_h, h, "incorrect crop height")
		self.assertEqual(crop_w, w, "incorrect crop width")

		self.assertTrue((cropped_im == _should).all(),
			"crop was incorret")


	def test_bbox_part_crop(self):
		_id, x, y, w, h = annotation = (0, 20, 20, 100, 100)

		part = BasePart.new(self.im, annotation)

		cropped_im = part.crop(self.im)

		_should = self.im[y:y+h, x:x+w]
		self._check_crop(cropped_im, _should)

	def test_location_part_crop(self):
		_id, center_x, center_y, _vis = annotation = (0, 50, 50, 1)

		part = BasePart.new(self.im, annotation)

		h, w, c = self.im.shape
		for ratio in np.linspace(0.1, 0.3, num=9):
			_h, _w = int(h * ratio), int(w * ratio)

			cropped_im = part.crop(self.im, ratio=ratio)

			x, y = center_x - _h // 2, center_y - _w // 2
			_should = self.im[y : y + _h, x : x + _w]

			self._check_crop(cropped_im, _should)

	def test_non_visible_location_crop(self):
		_id, center_x, center_y, _vis = annotation = (0, 50, 50, 0)

		def _blank(im, w, h):
			return np.zeros((h, w, 3), dtype=im.dtype)

		def _middle(im, w, h):
			im_h, im_w, c = im.shape
			middle_x, middle_y = im_w // 2, im_h // 2

			x0 = middle_x - w // 2
			y0 = middle_y - h // 2

			return im[y0: y0+h, x0: x0+w]

		def _image(im, w, h):
			return resize(im, (h, w),
				mode="constant",
				anti_aliasing=True,
				preserve_range=True).astype(np.uint8)

		shoulds = [
			(SurrogateType.BLANK, _blank),
			(SurrogateType.MIDDLE, _middle),
			(SurrogateType.IMAGE, _image),
		]

		for surr_type, should in shoulds:

			bbox = BasePart.new(self.im, annotation, surrogate_type=surr_type)

			h, w, c = self.im.shape
			for ratio in np.linspace(0.1, 0.3, num=9):
				_h, _w = int(h * ratio), int(w * ratio)

				cropped_im = bbox.crop(self.im, ratio=ratio)

				_should = should(self.im, _w, _h)

				self._check_crop(cropped_im, _should)
