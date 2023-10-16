import unittest
import numpy as np

from skimage.transform import resize

from cvdatasets.dataset.part.surrogate import SurrogateType


class SurrogateTest(unittest.TestCase):

	def setUp(self):
		self.im = np.random.randn(300, 300, 3).astype(np.uint8)

	def test_middle_surrogate(self):

		w = h = 100
		should = self.im[100:200, 100:200]
		computed = SurrogateType.MIDDLE(self.im, w, h)

		self.assertEqual(should.shape, computed.shape)
		self.assertTrue(np.all(should == computed))


	def test_blank_surrogate(self):

		w = h = 100
		should = np.zeros((h,w,3), dtype=np.uint8)
		computed = SurrogateType.BLANK(self.im, w, h)

		self.assertEqual(should.shape, computed.shape)
		self.assertTrue(np.all(should == computed))

	def test_image_surrogate(self):

		w = h = 100
		should = resize(self.im, (h, w),
			mode="constant",
			anti_aliasing=True,
			preserve_range=True).astype(np.uint8)
		computed = SurrogateType.IMAGE(self.im, w, h)

		self.assertEqual(should.shape, computed.shape)
		self.assertTrue(np.all(should == computed))


