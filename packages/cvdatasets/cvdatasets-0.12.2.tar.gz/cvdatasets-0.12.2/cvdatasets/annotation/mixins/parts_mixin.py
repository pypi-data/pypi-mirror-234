import abc
import copy
import logging
import numpy as np

from collections import OrderedDict
from collections import defaultdict
from typing import Union

from cvdatasets.annotation.files import AnnotationFiles
from cvdatasets.utils.decorators import only_with_info

class PartsMixin(abc.ABC):

	@classmethod
	def extract_kwargs(cls, opts, *args, **kwargs):
		kwargs = super(PartsMixin, cls).extract_kwargs(opts, *args, **kwargs)
		kwargs.update(dict(
			parts=getattr(opts, "parts", None),
		))
		return kwargs


	def __init__(self, *args, parts=None, **kwargs):
		self.part_type = parts
		self.part_names = OrderedDict()
		self.part_name_list = []

		super(PartsMixin, self).__init__(*args, **kwargs)

	def read_annotation_files(self) -> AnnotationFiles:
		files = super(PartsMixin, self).read_annotation_files()
		logging.debug("Adding part annotation files")
		files.load_files(
			part_locs=("parts/part_locs.txt", True),
			part_names=("parts/parts.txt", True),
		)

		return files

	@property
	@only_with_info
	def dataset_info(self) -> dict:
		ds_info = super(PartsMixin, self).dataset_info
		if self.part_type is not None:
			parts_key = f"{self.dataset_key}_{self.part_type}"
			if parts_key in self.info.PARTS:
				parts_info = self.info.PARTS[parts_key]
			else:
				parts_info = self.info.PART_TYPES[self.part_type]

			ds_info = copy.deepcopy(ds_info)
			ds_info.update(parts_info)

		return ds_info

	def check_dataset_kwargs(self, subset, **kwargs) -> dict:
		if self.dataset_info is None:
			return kwargs

		new_kwargs = {}

		if self.part_type is not None:
			new_kwargs["part_rescale_size"] = self.dataset_info.rescale_size

		new_kwargs.update(kwargs)

		return super(PartsMixin, self).check_dataset_kwargs(subset, **new_kwargs)

	@property
	def has_parts(self) -> bool:
		return self.files.part_locs is not None

	@property
	def has_part_names(self) -> bool:
		return self.files.part_names is not None

	def parse_annotations(self) -> None:
		super(PartsMixin, self).parse_annotations()

		if self.has_parts:
			self._parse_parts()

	def _parse_parts(self) -> None:
		logging.debug("Parsing part annotations")
		assert self.has_parts, \
			"Part locations were not loaded!"
		# this part is quite slow... TODO: some runtime improvements?
		uuid_to_parts = defaultdict(list)
		for content in [i.split() for i in self.files.part_locs]:
			uuid = content[0]
			# assert uuid in self.uuids, \
			# 	"Could not find UUID \"\" from part annotations in image annotations!".format(uuid)
			uuid_to_parts[uuid].append([float(c) for c in content[1:]])

		uuid_to_parts = dict(uuid_to_parts)
		self.part_locs = np.stack([
			uuid_to_parts[uuid] for uuid in self.uuids]).astype(np.int32)

		if self.has_part_names:
			self._parse_part_names()

	def _parse_part_names(self) -> None:
		self.part_names.clear()
		self.part_name_list.clear()

		for line in self.files.part_names:
			part_idx, _, name = line.partition(" ")
			self.part_names[int(part_idx)] = name
			self.part_name_list.append(name)

	def parts(self, uuid) -> Union[np.ndarray, None]:
		if self.has_parts:
			return self.part_locs[self.uuid_to_idx[uuid]].copy()

		return None

	def set_parts(self, uuid, parts):
		if not self.has_parts:
			shape = (len(self.uuids),) + parts.shape
			n_parts, _ = parts.shape
			self.part_locs = np.full(shape, -1, dtype=np.int32)

			for locs in self.part_locs:
				locs[:, 0] = np.arange(len(locs))
			self.files.part_locs = True

		self.part_locs[self.uuid_to_idx[uuid]] = parts

