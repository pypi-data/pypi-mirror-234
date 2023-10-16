import abc
import logging
import numpy as np

from cvdatasets.annotation.files import AnnotationFiles

class BBoxMixin(abc.ABC):

	dtype = np.dtype([
		("x", np.int32),
		("y", np.int32),
		("w", np.int32),
		("h", np.int32),
	])

	def read_annotation_files(self) -> AnnotationFiles:
		files = super(BBoxMixin, self).read_annotation_files()
		logging.debug("Adding bounding box annotation files")
		files.load_files(
			bounding_boxes=("bounding_boxes.txt", True),
		)
		return files

	@property
	def has_bounding_boxes(self) -> bool:
		return self.files.bounding_boxes is not None

	def parse_annotations(self) -> None:
		super(BBoxMixin, self).parse_annotations()

		if self.has_bounding_boxes:
			self._parse_bounding_boxes()

	def _parse_bounding_boxes(self) -> None:
		logging.debug("Parsing bounding box annotations")
		assert self.has_bounding_boxes, \
			"Bounding boxes were not loaded!"

		uuid_to_bbox = {}
		for content in [i.split() for i in self.files.bounding_boxes]:
			uuid, bbox = content[0], content[1:]
			uuid_to_bbox[uuid] = [float(i) for i in bbox]

		self.bounding_boxes = np.array(
			[tuple(uuid_to_bbox[uuid]) for uuid in self.uuids],
			dtype=self.dtype)

	def bounding_box(self, uuid) -> np.ndarray:
		if self.has_bounding_boxes:
			return self.bounding_boxes[self.uuid_to_idx[uuid]].copy()

		return None
