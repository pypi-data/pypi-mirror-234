import abc
import logging
from cvdatasets.utils import feature_file_name

class FeaturesMixin(abc.ABC):
	FEATURE_PHONY = dict(train=["train"], test=["test", "val"])

	@classmethod
	def extract_kwargs(cls, opts, *args, **kwargs):
		kwargs = super(FeaturesMixin, cls).extract_kwargs(opts, *args, **kwargs)
		kwargs.update(dict(
			feature_model=getattr(opts, "feature_model", None),
		))
		return kwargs

	def __init__(self, *args, feature_model=None, feature_folder="features", **kwargs):
		super(FeaturesMixin, self).__init__(*args, **kwargs)

		self.feature_model = feature_model
		self.feature_folder = feature_folder

	def check_dataset_kwargs(self, subset, **kwargs):
		kwargs = super(FeaturesMixin, self).check_dataset_kwargs(subset, **kwargs)

		new_kwargs = {}
		if None not in [subset, self.feature_model]:
			tried = []
			model_info = self.info.MODELS[self.feature_model]
			for subset_phony in FeaturesMixin.FEATURE_PHONY[subset]:
				features = feature_file_name(subset_phony, self.dataset_info, model_info)
				feature_path = self.root / self.feature_folder / features
				if feature_path.is_file(): break
				tried.append(feature_path)
			else:
				raise ValueError(
					f"Could not find any features in \"{self.root / self.feature_folder}\" for {subset} subset. Tried features: {tried}")

			logging.info(f"Using features file from \"{feature_path}\"")
			new_kwargs["features"] = feature_path

		new_kwargs.update(kwargs)
		return new_kwargs
