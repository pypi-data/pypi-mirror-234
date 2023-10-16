import numpy as np

try:
	from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
	from yaml import Loader, Dumper

import yaml

from os.path import isfile

def pretty_print_dict(dictionary):
	return ", ".join(["{key}={value}".format(key=key, value=value)
		for key, value in dictionary.items()])

def feature_file_name(subset, part_info, model_info):

	return "{subset}{suffix}.{model}.npz".format(
			subset=subset,
			suffix=part_info.feature_suffix,
			model=model_info.class_key)

def read_info_file(fpath):
	with open(fpath) as f:
		return attr_dict(yaml.load(f, Loader=Loader))

def random_idxs(idxs, rnd=None, n_parts=None):

	if rnd is None or isinstance(rnd, int):
		rnd = np.random.RandomState(rnd)
	else:
		assert isinstance(rnd, np.random.RandomState), \
			"'rnd' should be either a random seed or a RandomState instance!"

	n_parts = n_parts or rnd.randint(1, len(idxs))
	res = rnd.choice(idxs, n_parts, replace=False)
	res.sort()
	return res

class attr_dict(dict):
	def __getattr__(self, name):
		if name in self:
			return self[name]
		else:
			return super(attr_dict, self).get(name)

	def __getitem__(self, key):
		res = super(attr_dict, self).__getitem__(key)

		if isinstance(res, dict):
			return attr_dict(res)
		return res

	def __getstate__(self): return self.__dict__

	def __setstate__(self, d): self.__dict__.update(d)


class _MetaInfo(object):
	def __init__(self, **kwargs):
		for name, value in kwargs.items():
			setattr(self, name, value)
		self.structure = []

def retry_operation(n_retries, func, *args, **kwargs):

	if n_retries <= 0:
		return func(*args, **kwargs)

	error = None
	for i in range(n_retries):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			error = e

	raise RuntimeError(f"Operation {func.__name__} failed after {n_retries} n_retries! ({error})")


from cvdatasets.utils.dataset import new_iterator
from cvdatasets.utils.image import asarray
from cvdatasets.utils.image import read_image
from cvdatasets.utils.transforms import color_jitter
from cvdatasets.utils.transforms import dimensions
from cvdatasets.utils.transforms import rescale
