
class only_with_info(object):

	def __init__(self, method):
		self.method = method

	def __call__(self, obj, *args, **kwargs):
		if obj.info is None: return None
		return self.method(obj, *args, **kwargs)
