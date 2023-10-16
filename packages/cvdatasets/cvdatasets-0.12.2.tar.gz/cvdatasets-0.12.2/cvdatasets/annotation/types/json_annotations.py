import copy
import hashlib
import logging
import numpy as np

from cvdatasets import utils
from cvdatasets.annotation.base import Annotations
from cvdatasets.annotation.files import AnnotationFiles

def _uuid_entry(im_info):
	return hashlib.md5(im_info["file_name"].encode()).hexdigest()

class JSONAnnotations(Annotations):

	def load_files(self, file_obj) -> AnnotationFiles:
		file_obj.load_files(
			"trainval.json", "val.json",
			("unlabeled_train.json", True),
		)
		return file_obj

	@property
	def has_unlabeled_data(self) -> bool:
		return self.files.unlabeled_train is not None

	def _parse_uuids(self) -> None:

		uuid_fnames = [(str(im["id"]), im["file_name"]) for im in self.files.trainval["images"]]
		self.uuids, self.image_names = map(np.array, zip(*uuid_fnames))

		utils.dataset._uuid_check(self.uuids)

		self.uuid_to_idx = {uuid: i for i, uuid in enumerate(self.uuids)}

		if self.has_unlabeled_data:
			logging.info("Loading unlabeled data...")
			self._parse_unlabeled()
		else:
			logging.info("No unlabeled data was provided!")

	def _parse_unlabeled(self) -> None:

		uuid_fnames = [(_uuid_entry(im), im["file_name"]) for im in self.files.unlabeled_train["images"]]

		self.unlabeled = unlabeled = copy.copy(self)

		unlabeled.uuids, unlabeled.image_names = map(np.array, zip(*uuid_fnames))
		unlabeled.labels = np.full(unlabeled.image_names.shape, -1, dtype=np.int32)
		unlabeled.train_split = np.full(unlabeled.image_names.shape, 1, dtype=bool)
		unlabeled.test_split = np.full(unlabeled.image_names.shape, 0, dtype=bool)

		assert len(np.unique(unlabeled.uuids)) == len(unlabeled.uuids), \
			"Unlabeled UUIDs are not unique!"

		overlap = set(self.uuids) & set(unlabeled.uuids)
		assert len(overlap) == 0, \
			f"Unlabeled and labeled UUIDs overlap: {overlap}"

		unlabeled.uuid_to_idx = {uuid: i for i, uuid in enumerate(unlabeled.uuids)}


	def _parse_labels(self) -> None:
		self.labels = np.zeros(len(self.uuids), dtype=np.int32)
		labs = {str(annot["image_id"]): annot["category_id"]
			for annot in self.files.trainval["annotations"]}

		for uuid in self.uuids:
			self.labels[self.uuid_to_idx[uuid]] = labs[uuid]


	def _parse_split(self) -> None:
		self.train_split = np.ones(len(self.uuids), dtype=bool)
		val_uuids = [str(im["id"]) for im in self.files.val["images"]]
		for v_uuid in val_uuids:
			self.train_split[self.uuid_to_idx[v_uuid]] = False

		self.test_split = np.logical_not(self.train_split)



if __name__ == '__main__':
	annot = JSONAnnotations(
		root_or_infofile="/home/korsch_data/datasets/inat/2020/IN_CLASS")

	for i, uuid in enumerate(annot.uuids):
		print(uuid, annot[uuid])

		if i >= 4:
			break

	train, test = annot.new_train_test_datasets()

	print(len(train), len(test))

