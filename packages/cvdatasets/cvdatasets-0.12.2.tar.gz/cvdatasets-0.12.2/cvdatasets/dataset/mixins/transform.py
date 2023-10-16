import abc

try:
	import chainer
	def is_train() -> bool:
		return chainer.config.train
except ImportError as e:
	""" other frameworks (e.g., PyTorch) do not have this global flag """
	def is_train() -> bool:
		return False



from cvdatasets.dataset.image.size import Size
from cvdatasets.dataset.mixins.base import BaseMixin

class TransformMixin(BaseMixin):

	def __init__(self, size, part_size=None, *args, **kwargs):
		super(TransformMixin, self).__init__(*args, **kwargs)

		self.size = size
		self.part_size = size if part_size is None else part_size

	@abc.abstractmethod
	def transform(self, im_obj):
		pass

	def get_example(self, i):
		im_obj = super(TransformMixin, self).get_example(i)
		return self.transform(im_obj)

	@property
	def size(self):
		if is_train():
			return self._size // 0.875
		else:
			return self._size

	@size.setter
	def size(self, value):
		self._size = Size(value)

	@property
	def part_size(self):
		if is_train():
			return self._part_size // 0.875
		else:
			return self._part_size

	@part_size.setter
	def part_size(self, value):
		self._part_size = Size(value)
