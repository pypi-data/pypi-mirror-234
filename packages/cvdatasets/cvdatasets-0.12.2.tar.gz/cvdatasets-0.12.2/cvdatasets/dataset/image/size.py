import numpy as np

from collections.abc import Iterable

class Size(object):
	dtype=np.int32

	def __init__(self, value):
		self._size = np.zeros(2, dtype=self.dtype)
		if isinstance(value, int):
			self._size[:] = value

		elif isinstance(value, Size):
			self._size[:] = value._size

		elif isinstance(value, Iterable):
			assert len(value) <= 2, \
				"only iterables of maximum size 2 are supported, but was {}!".format(len(value))
			self._size[:] = np.round(value)


		else:
			raise ValueError("Unsupported data type: {}!".format(type(value)))

	def __str__(self):
		return "<Size {}x{}>".format(*self._size)

	def __repr__(self):
		return str(self)

	def __add__(self, other):
		return self.__class__(self._size + other)

	def __sub__(self, other):
		return self.__class__(self._size - other)

	def __mul__(self, other):
		return self.__class__(self._size * other)

	def __truediv__(self, other):
		return self.__class__(self._size / other)

	def __floordiv__(self, other):
		return self.__class__(self._size // other)

	def __iter__(self):
		return iter(self._size)

	def __len__(self):
		return len(self._size)
