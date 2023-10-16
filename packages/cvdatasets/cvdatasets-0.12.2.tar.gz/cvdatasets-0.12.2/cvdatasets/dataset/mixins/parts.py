import numpy as np

from cvdatasets.dataset.mixins.base import BaseMixin
from cvdatasets.dataset.mixins.bounding_box import BBoxMixin
from cvdatasets.dataset.mixins.bounding_box import BBCropMixin

class BasePartMixin(BaseMixin):

	def __init__(self, ratio=None, *args, **kwargs):
		super(BasePartMixin, self).__init__(*args, **kwargs)
		self.ratio = ratio

class PartsInBBMixin(BasePartMixin, BBoxMixin):

	def __init__(self, parts_in_bb=False, *args, **kwargs):
		super(PartsInBBMixin, self).__init__(*args, **kwargs)
		self.parts_in_bb = parts_in_bb

	def get_example(self, i):
		im_obj = super(PartsInBBMixin, self).get_example(i)

		if self.parts_in_bb:
			bb = self.bounding_box(i)
			return im_obj.hide_parts_outside_bb(*bb)
		return im_obj

class PartCropMixin(BasePartMixin):

	def __init__(self, return_part_crops=False, *args, **kwargs):
		super(PartCropMixin, self).__init__(*args, **kwargs)
		self.return_part_crops = return_part_crops

	def get_example(self, i):
		im_obj = super(PartCropMixin, self).get_example(i)
		if self.return_part_crops:
			return im_obj.part_crops(self.ratio)
		return im_obj


class PartRevealMixin(BasePartMixin):

	def __init__(self, reveal_visible=False, *args, **kwargs):
		super(PartRevealMixin, self).__init__(*args, **kwargs)
		self.reveal_visible = reveal_visible

	def get_example(self, i):
		im_obj = super(PartRevealMixin, self).get_example(i)
		if self.reveal_visible:
			return im_obj.reveal_visible(self.ratio)
		return im_obj


class UniformPartMixin(BasePartMixin):

	def __init__(self, uniform_parts=False, *args, **kwargs):
		super(UniformPartMixin, self).__init__(*args, **kwargs)
		self.uniform_parts = uniform_parts

	def get_example(self, i):
		im_obj = super(UniformPartMixin, self).get_example(i)
		if self.uniform_parts:
			return im_obj.uniform_parts(self.ratio)
		return im_obj

class RandomBlackOutMixin(BasePartMixin):

	def __init__(self, seed=None, rnd_select=False, blackout_parts=None, *args, **kwargs):
		super(RandomBlackOutMixin, self).__init__(*args, **kwargs)
		self.rnd = np.random.RandomState(seed)
		self.rnd_select = rnd_select
		self.blackout_parts = blackout_parts

	def get_example(self, i):
		im_obj = super(RandomBlackOutMixin, self).get_example(i)
		if self.rnd_select:
			return im_obj.select_random_parts(rnd=self.rnd, n_parts=self.blackout_parts)
		return im_obj


# some shortcuts

class _PartMixin(RandomBlackOutMixin, PartsInBBMixin, UniformPartMixin, BBCropMixin):
	"""
		TODO!
	"""

class RevealedPartMixin(PartRevealMixin, _PartMixin):
	"""
		TODO!
	"""


class CroppedPartMixin(PartCropMixin, _PartMixin):
	"""
		TODO!
	"""
