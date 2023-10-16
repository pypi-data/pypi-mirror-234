import numpy as np

from cvdatasets.annotation.base import Annotations
from cvdatasets.annotation.files import AnnotationFiles

class FileListAnnotations(Annotations):

	@classmethod
	def extract_kwargs(cls, opts, ds_info=None, *args, **kwargs):
		kwargs = super(FileListAnnotations, cls).extract_kwargs(opts, ds_info=ds_info, *args, **kwargs)
		kwargs["test_fold_id"] = getattr(opts, "test_fold_id", 0)
		return kwargs

	def __init__(self, *args, test_fold_id=0, **kwargs):
		self._test_fold_id = test_fold_id
		super(FileListAnnotations, self).__init__(*args, **kwargs)

	def load_files(self, file_obj) -> AnnotationFiles:
		file_obj.load_files(
			"images.txt",
			"labels.txt",
			"tr_ID.txt",
			("hierarchy.txt", True),
		)
		return file_obj

	def _parse_uuids(self) -> None:
		assert self.files.images is not None, \
			"Images were not loaded!"

		uuid_fnames = [i.split() for i in self.files.images]
		self.uuids, self.image_names = map(np.array, zip(*uuid_fnames))
		self.uuid_to_idx = {uuid: i for i, uuid in enumerate(self.uuids)}

	def _parse_labels(self) -> None:
		assert self.files.labels is not None, \
			"Labels were not loaded!"

		labs = list(map(int, self.files.labels))
		self.labels = np.array(labs, dtype=np.int32)

	def _parse_split(self) -> None:
		assert self.files.tr_ID is not None, \
			"Train-test split was not loaded!"

		assert hasattr(self, "uuids"), \
			"UUIDs were not parsed yet! Please call _parse_uuids before this method!"
		uuid_to_split = {uuid: int(split) for uuid, split in zip(self.uuids, self.files.tr_ID)}

		split_ids = np.array([uuid_to_split[uuid] for uuid in self.uuids])
		self.test_split = split_ids == self._test_fold_id
		self.train_split = np.logical_not(self.test_split)

if __name__ == '__main__':
	annot = FileListAnnotations(
		root_or_infofile="/home/korsch_data/datasets/birds/cub200/ORIGINAL")

	for i, uuid in enumerate(annot.uuids):
		print(uuid, annot[uuid])

		if i >= 10:
			break

	train, test = annot.new_train_test_datasets()

	print(len(train), len(test))
