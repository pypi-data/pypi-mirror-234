import numpy as np

from pathlib import Path

from cvdatasets import utils
from cvdatasets.annotation.base import Annotations
from cvdatasets.annotation.files import AnnotationFiles

class FolderAnnotations(Annotations):
	_default_folders = dict(
		train_images="train",
		val_images="val",
		test_images=("test", True)
	)

	@classmethod
	def extract_kwargs(cls, opts, ds_info=None, *args, **kwargs):
		kwargs = super(FolderAnnotations, cls).extract_kwargs(opts, ds_info=ds_info, *args, **kwargs)
		if ds_info is None:
			return kwargs

		folders = dict(cls._default_folders)

		for key in ["train", "val", "test"]:
			key = f"{key}_images"

			value = ds_info.get(key)
			if value is None:
				continue

			folders[key] = value

		kwargs["folders"] = folders
		return kwargs

	def __init__(self, *args, folders=_default_folders, **kwargs):
		self._folders = folders
		super(FolderAnnotations, self).__init__(*args, **kwargs)

	def load_files(self, file_obj) -> AnnotationFiles:
		file_obj.load_files(**self._folders)
		return file_obj

	@property
	def _has_test_set(self) -> bool:
		return self.files.test_images is not None

	def _uuid_from_path(self, fpath):
		return "_".join(Path(fpath).relative_to(self.root).parts)
		# return "_".join(Path(fpath).parts[-3:])

	def _parse_uuids(self) -> None:
		self.images_folder = ""

		train_uuid_fnames = [(self._uuid_from_path(fpath), str(fpath.relative_to(self.root))) for
			fpath in self.files.train_images]

		val_uuid_fnames = [(self._uuid_from_path(fpath), str(fpath.relative_to(self.root))) for
			fpath in self.files.val_images]

		if self._has_test_set:
			test_uuid_fnames = [(self._uuid_from_path(fpath), str(fpath.relative_to(self.root))) for
				fpath in self.files.test_images]

		uuid_fnames = train_uuid_fnames + val_uuid_fnames
		self.uuids, self.image_names = map(np.array, zip(*uuid_fnames))

		utils.dataset._uuid_check(self.uuids)
		self.uuid_to_idx = {uuid: i for i, uuid in enumerate(self.uuids)}


	def _parse_labels(self) -> None:
		train_labs = [fpath.parent.name for fpath in self.files.train_images]
		val_labs = [fpath.parent.name for fpath in self.files.val_images]
		labs = train_labs + val_labs

		if self._has_test_set:
			self.test_labels = [fpath.parent.name for fpath in self.files.test_images]

		self._classes, self.labels = np.unique(labs, return_inverse=True)


	def _parse_split(self) -> None:
		self.train_split = np.ones(len(self.uuids), dtype=bool)
		self.train_split[len(self.files.train_images):] = False

		self.test_split = np.logical_not(self.train_split)


if __name__ == '__main__':
	annot = FolderAnnotations(
		root_or_infofile="/home/korsch_data/datasets/ImageNet/TOP_INAT20")

	for i, uuid in enumerate(annot.uuids):
		print(uuid, annot[uuid])

		if i >= 10:
			break

	train, test = annot.new_train_test_datasets()

	print(len(train), len(test))
