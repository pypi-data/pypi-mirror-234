import abc
import logging
import numpy as np

from cvdatasets.annotation.files import AnnotationFiles


class MultiBoxMixin(abc.ABC):

	def read_annotation_files(self) -> AnnotationFiles:
		files = super(MultiBoxMixin, self).read_annotation_files()

		files.load_files(
			multi_boxes=("multi_boxes.json", True),
		)
		return files

	@property
	def has_multi_boxes(self) -> bool:
		return self.files.multi_boxes is not None

	def parse_annotations(self) -> None:
		super(MultiBoxMixin, self).parse_annotations()
		if self.has_multi_boxes:
			self._parse_multi_boxes()

	def _parse_multi_boxes(self) -> None:
		logging.debug("Parsing multi-box annotations")

		assert self.has_multi_boxes, \
			"Multi-boxes were not loaded!"

		self.multi_boxes = {}

		for uuid in self.uuids:
			idx = self.uuid_to_idx[uuid]
			im_name = self.image_names[idx]
			multi_box = self.files.multi_boxes[idx]
			assert im_name == multi_box["image"], \
				f"{im_name} != {multi_box['image']}"

			self.multi_boxes[uuid] = multi_box

	def multi_box(self, uuid) -> np.ndarray:
		if self.has_multi_boxes:
			return self.multi_boxes[uuid]

		fname = self.image_names[self.uuid_to_idx[uuid]]
		return dict(image=fname, objects=[dict(x0=0, x1=0, y0=1, y1=1)])
