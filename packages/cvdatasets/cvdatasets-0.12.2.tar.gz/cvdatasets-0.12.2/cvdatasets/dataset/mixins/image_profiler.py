import numpy as np
import logging

from contextlib import contextmanager

from cvdatasets.dataset.mixins.base import BaseMixin


class ImageProfilerMixin(BaseMixin):
	def __init__(self, *args, **kwargs):
		super(ImageProfilerMixin, self).__init__(*args, **kwargs)
		self._profile_img_enabled = False

	@contextmanager
	def enable_img_profiler(self):
		_dmp = self._profile_img_enabled
		self._profile_img_enabled = True
		yield
		self._profile_img_enabled = _dmp

	def _profile_img(self, img, tag):
		if len(img) == 0: return
		if self._profile_img_enabled:
			logging.info(f"[{tag:^30s}]" + \
				" | ".join([
					f"size: {str(img.shape):>20s}",
					f"pixel values: ({img.min():+8.2f}, {img.max():+8.2f})"
					])
				)
