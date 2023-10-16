import abc
import logging
import numpy as np

from pathlib import Path
from typing import Tuple

from cvdatasets.annotation import mixins
from cvdatasets.annotation.files import AnnotationFiles
from cvdatasets.dataset import Dataset
from cvdatasets.utils import pretty_print_dict
from cvdatasets.utils import read_info_file
from cvdatasets.utils.decorators import only_with_info


class BaseAnnotations(abc.ABC):

	@classmethod
	def extract_kwargs(cls, opts, *args, **kwargs):
		return dict(
			root_or_infofile=opts.data,
			load_strict=getattr(opts, "load_strict", False),
			dataset_key=getattr(opts, "dataset", None)
		)

	@classmethod
	def new(cls, opts,  *, ds_info=None, **_kwargs):
		kwargs = cls.extract_kwargs(opts, ds_info)
		kwargs.update(_kwargs)
		kwargs_str = pretty_print_dict(kwargs)
		try:
			annot = cls(**kwargs)
		except Exception as e:
			logging.error(f"Failed to create \"{cls.__name__}\" annotations " + \
				f"with following kwargs: \"{kwargs_str}\". " + \
				f"Error was: {e}"
			)
			raise
		else:
			logging.info(f"Loaded \"{annot.dataset_key}\" annotations " + \
				f"with following kwargs: \"{kwargs_str}\""
			)
			return annot


	def __init__(self, *, root_or_infofile, dataset_key=None, images_folder="images", load_strict=True, **kwargs):

		self.dataset_key = dataset_key
		self.images_folder = images_folder
		self.load_strict = load_strict

		root_or_infofile = Path(root_or_infofile)
		if root_or_infofile.is_dir():
			self.info = None
			self.root = root_or_infofile

		elif root_or_infofile.is_file():
			self.info = read_info_file(root_or_infofile)
			ds_info = self.dataset_info
			self.root = self.data_root / ds_info.folder / ds_info.annotations

		else:
			msg = f"Root folder or info file does not exist: \"{root_or_infofile}\""
			raise ValueError(msg)

		assert self.root.is_dir(), \
			f"Annotation directory does not exist: \"{self.root}\"!"

		self.files = self.read_annotation_files()
		self.parse_annotations()

	@property
	@only_with_info
	def data_root(self):
		return Path(self.info.BASE_DIR) / self.info.DATA_DIR

	@property
	@only_with_info
	def dataset_key(self):
		if self._dataset_key is not None:
			return self._dataset_key

		else:
			return self.__class__.__name__

	@dataset_key.setter
	def dataset_key(self, value):
		self._dataset_key = value

	@property
	@only_with_info
	def dataset_info(self):
		key = self.dataset_key

		if key not in self.info.DATASETS:
			raise ValueError(f"Cannot find dataset with key \"{key}\"")

		return self.info.DATASETS[key]

	def parse_annotations(self):
		logging.debug("Parsing read annotations (uuids, labels and train-test splits)")
		self._parse_uuids()
		self._parse_labels()
		self._parse_split()

	def __getitem__(self, uuid) -> Tuple[str, int]:
		return self.image(uuid), self.label(uuid)

	@property
	def labels(self):
		return self._labels

	@labels.setter
	def labels(self, labels):
		self._orig_labels, self._labels = np.unique(labels, return_inverse=True)
		self._orig2unq_labels = {lab:i for i, lab in enumerate(self._orig_labels)}
		self._unq2orig_labels = {i:lab for i, lab in enumerate(self._orig_labels)}

	def unq2orig(self, label):
		return self._unq2orig_labels[int(label)]

	def orig2unq(self, label):
		return self._orig2unq_labels[int(label)]

	def image_path(self, image) -> str:
		return str(self.root / self.images_folder / image)

	def image(self, uuid) -> str:
		fname = self.image_names[self.uuid_to_idx[uuid]]
		return self.image_path(fname)

	def label(self, uuid) -> int:
		return self.labels[self.uuid_to_idx[uuid]].copy()

	def bounding_box(self, uuid) -> object:
		return None

	def _uuids(self, split) -> np.ndarray:
		return self.uuids[split]

	@property
	def train_uuids(self):
		return self._uuids(self.train_split)

	@property
	def test_uuids(self):
		return self._uuids(self.test_split)

	def new_train_test_datasets(self, dataset_cls=Dataset, **kwargs):
		return (self.new_dataset(subset, dataset_cls, **kwargs) for subset in ["train", "test"])

	def new_dataset(self, subset=None, dataset_cls=Dataset, **kwargs):
		if subset is not None:
			uuids = getattr(self, "{}_uuids".format(subset))
		else:
			uuids = self.uuids

		kwargs = self.check_dataset_kwargs(subset, **kwargs)
		return dataset_cls(uuids=uuids, annotations=self, **kwargs)

	def check_dataset_kwargs(self, subset, **kwargs):
		dataset_info = self.dataset_info
		if dataset_info is None:
			return kwargs

		logging.debug("Dataset info: {}".format(pretty_print_dict(dataset_info)))

		# TODO: pass all scales
		new_kwargs = {}

		if "scales" in dataset_info and len(dataset_info.scales):
			new_kwargs["ratio"] = dataset_info.scales[0]

		if "is_uniform" in dataset_info:
			new_kwargs["uniform_parts"] = dataset_info.is_uniform

		new_kwargs.update(kwargs)
		logging.debug("Final kwargs: {}".format(pretty_print_dict(new_kwargs)))
		return new_kwargs

	def read_annotation_files(self) -> AnnotationFiles:
		logging.debug("Creating default AnnotationFiles object")
		files = AnnotationFiles(root=self.root, load_strict=self.load_strict)
		return self.load_files(files)

	@abc.abstractmethod
	def load_files(self, files_obj) -> AnnotationFiles:
		return files_obj

	@abc.abstractmethod
	def _parse_uuids(self) -> None:
		pass

	@abc.abstractmethod
	def _parse_labels(self) -> None:
		pass

	@abc.abstractmethod
	def _parse_split(self) -> None:
		pass


class Annotations(
	mixins.BBoxMixin,
	mixins.MultiBoxMixin,
	mixins.PartsMixin,
	mixins.FeaturesMixin,
	mixins.HierarchyMixin,
	BaseAnnotations):
	pass
