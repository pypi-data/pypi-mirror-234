import typing

from cvdatasets.annotation.types.file_list import FileListAnnotations
from cvdatasets.annotation.types.folder_annotations import FolderAnnotations
from cvdatasets.annotation.types.json_annotations import JSONAnnotations

from cvargparse.utils import BaseChoiceType
from cvdatasets.utils import read_info_file


class AnnotationArgs(typing.NamedTuple):
	data: str
	dataset: str
	parts: str
	feature_model: str

	test_fold_id: int = 0

class AnnotationType(BaseChoiceType):
	FOLDER = FolderAnnotations
	FILE_LIST = FileListAnnotations
	JSON = JSONAnnotations

	Default = FILE_LIST

	@classmethod
	def new_annotation(cls, args: AnnotationArgs, **kwargs):
		info_file = read_info_file(args.data)
		ds_info = info_file.DATASETS[args.dataset]

		if args.dataset in cls:
			annot = cls[args.dataset].value

		else:
			assert args.dataset in info_file.DATASETS, \
				f"No information was found about the dataset \"{args.dataset}\" in the info file \"{args.data}\""
			annot = cls[ds_info.annotation_type.lower()].value

		return annot.new(args, ds_info=ds_info, **kwargs)

	@classmethod
	def as_choices(cls, add_phony=True):
		choices = super(AnnotationType, cls).as_choices()
		if not add_phony:
			return choices

		for key in cls:
			for phony in cls.phony(key):
				choices[phony.lower()] = choices[key.name.lower()]

		return choices

	@classmethod
	def phony(cls, key):
		""" returns for a key a list of datasets,
			that use the same annotation class """

		return {
			cls.FOLDER : [
				"IMAGENET", "IMAGENET_TOP_INAT20"
			],

			cls.FILE_LIST : [
				"CUB200", "CUB200_2FOLD", "CUB200_GOOGLE", "CUB200_GOOGLE_SEM",
				"NAB", "BIRDSNAP",
				"CARS", "DOGS", "FLOWERS",
				"HED", "TIGERS", "TIGERS_TEST",

			],

			cls.JSON : [
				"INAT18",
				"INAT19", "INAT19_TEST", "INAT19_MINI",
				"INAT20", "INAT20_TEST",
				"INAT20_IN_CLASS",
				"INAT20_OUT_CLASS",
				"INAT20_NOISY_IN_CLASS",
				"INAT20_NOISY_OUT_CLASS",
				"INAT20_U_IN_CLASS",
				"INAT20_U_OUT_CLASS",
			],

		}.get(key, [])

if __name__ == '__main__':
	print(AnnotationType.as_choices().keys())
