import enum
import logging
import numpy as np
import typing as T

from cvdatasets.dataset.mixins.chainer_mixins.iterator_mixin import IteratorMixin


class SamplingType(enum.Enum):

	undersample = enum.auto()
	oversample = enum.auto()

	def __call__(self, dataset,
				 random_state=None,
				 count: int = -1,
				 ):
		if random_state is None:
			rnd = np.random.RandomState()

		elif isinstance(random_state, int):
			rnd = np.random.RandomState(random_state)

		else:
			rnd = random_state

		labs = dataset.labels
		cls_count = np.bincount(labs)

		def sampler(current_order, current_position):

			labs_now = dataset.labels

			idxs = []
			if self == SamplingType.undersample:
				# logging.debug("UNDERSAMPLING")
				_count = max(count, cls_count.min())

				for cls in np.unique(labs):
					mask = cls == labs
					cls_idxs = np.where(mask)[0]
					if len(cls_idxs) > _count:
						cls_idxs = rnd.choice(cls_idxs, _count, replace=False)

					idxs.extend(cls_idxs)

			elif self == SamplingType.oversample:
				# logging.debug("OVERSAMPLING")
				_count = min(count, cls_count.max())

				for cls in np.unique(labs):
					mask = cls == labs
					cls_idxs = np.where(mask)[0]
					if len(cls_idxs) < _count:
						cls_idxs = rnd.choice(cls_idxs, _count, replace=True)

					idxs.extend(cls_idxs)

			return rnd.permutation(idxs)

		return sampler

class SamplingMixin(IteratorMixin):

	def __init__(self, sampling_type: T.Optional[SamplingType] = None,
		         sampling_count: int = -1,
		         *args, **kwargs):
		self._sampling_type = sampling_type
		self._sampling_count = sampling_count
		super().__init__(*args, **kwargs)

	def new_iterator(self, **kwargs):
		it, n_batches = super().new_iterator(**kwargs)

		if None not in (it.order_sampler, self._sampling_type):
			it.order_sampler = self._sampling_type(self,
				count=self._sampling_count,
				random_state=it.order_sampler._random)

			logging.info(f"Initialized new sampler: {self._sampling_type}")

			if hasattr(it, "_initialize_loop"):
				it._initialize_loop()
			else:
				it.reset()

		return it, n_batches
