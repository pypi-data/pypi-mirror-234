try:
	import chainer
except ImportError:
	has_chainer = False
else:
	has_chainer = True

import abc

class BaseChainerMixin(abc.ABC):

	def chainer_check(self):
		global has_chainer
		assert has_chainer, "Please install chainer!"
