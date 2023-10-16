from cvdatasets.dataset.image import ImageWrapper
from cvdatasets.dataset.mixins.base import BaseMixin
from cvdatasets.dataset.mixins.bounding_box.bbox import BoundingBox

class MultiBoxMixin(BaseMixin):
	_all_keys=[
		"x", "x0", "x1",
		"y", "y0", "y1",
		"w", "h",
	]

	def multi_box(self, i, keys=["x0","x1","y0","y1"]):
		assert keys is None or all([key in self._all_keys for key in keys]), \
			f"unknown keys found: {keys}. Possible are: {self._all_keys}"


		im_obj: ImageWrapper = self.image_wrapped(i)
		boxes = [BoundingBox.new(**box, resize=im_obj._im.size)
			for box in self._get("multi_box", i)["objects"]
		]
		del im_obj

		if keys is None:
			return boxes

		return [box.get(*keys) for box in boxes]
