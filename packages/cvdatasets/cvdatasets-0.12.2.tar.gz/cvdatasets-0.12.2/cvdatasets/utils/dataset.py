import logging
import numpy as np
import warnings

def _format_kwargs(kwargs):
	return " ".join([f"{key}={value}" for key, value in kwargs.items()])

def _uuid_check(uuids):
	""" Checks whether the ids are unique """

	assert len(np.unique(uuids)) == len(uuids), \
		"UUIDs are not unique!"

def new_iterator(data, n_jobs, batch_size, repeat=True, shuffle=True, n_prefetch=2, *,
	use_threads: bool = False):
	from chainer.iterators import SerialIterator, MultiprocessIterator, MultithreadIterator

	it_kwargs = dict(batch_size=batch_size, repeat=repeat, shuffle=shuffle)
	if n_jobs > 0:
		try:
			import cv2
			cv2.setNumThreads(0)
		except ImportError:
			pass

		if use_threads:
			raise RuntimeError("MultithreadIterator seems to have some issues concerning configs")
			it_cls = MultithreadIterator
			it_kwargs["n_threads"] = n_jobs

		else:
			it_cls = MultiprocessIterator

			input_shape = getattr(data, "size", (512, 512))
			n_parts = getattr(data, "n_parts", 1)

			if isinstance(input_shape, int):
				input_shape = (input_shape, input_shape)
			elif not isinstance(input_shape, tuple):
				try:
					input_shape = tuple(input_shape)
				except TypeError as e:
					warnings.warn(f"Could not parse input_shape: \"{input_shape}\". Falling back to a default value of (512, 512)")
					input_shape = (512, 512)

			shared_mem_shape = (3,) + input_shape
			shared_mem = (n_parts+1) * np.zeros(shared_mem_shape, dtype=np.float32).nbytes
			logging.info(f"Using {batch_size * shared_mem / 1024**2: .3f} MiB of shared memory")

			it_kwargs.update(
				n_processes=n_jobs,
				n_prefetch=n_prefetch,
				shared_mem=shared_mem,
			)
	else:
		it_cls = SerialIterator

	it = it_cls(data, **it_kwargs)
	n_batches = int(np.ceil(len(data) / it.batch_size))
	logging.info(f"Using {it_cls.__name__} with {n_batches:,d} batches per epoch and kwargs: {_format_kwargs(it_kwargs)}")

	return it, n_batches
