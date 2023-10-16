from cvdatasets.dataset.mixins.base import BaseMixin
from cvdatasets.dataset.mixins.bounding_box.bbox import BoundingBox

class BBoxMixin(BaseMixin):

	def bounding_box(self, i):
		bbox = self._get("bounding_box", i)
		if bbox is None or not len(bbox):
			return None
		return BoundingBox(*bbox)


class BBCropMixin(BBoxMixin):

	def __init__(self, *, crop_to_bb=False, crop_uniform=False, **kwargs):
		super(BBCropMixin, self).__init__(**kwargs)
		self.crop_to_bb = crop_to_bb
		self.crop_uniform = crop_uniform

	def bounding_box(self, i):
		bbox = super(BBCropMixin, self).bounding_box(i)

		if self.crop_uniform:
			return bbox.squared()

		return bbox

	def get_example(self, i):
		im_obj = super(BBCropMixin, self).get_example(i)
		if self.crop_to_bb:
			bb = self.bounding_box(i)
			return im_obj.crop(*bb)
		return im_obj
