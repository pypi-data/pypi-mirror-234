import numpy as np
import warnings

from abc import ABC
from abc import abstractproperty
from matplotlib import pyplot as plt
from skimage.transform import resize

from cvdatasets import utils
from cvdatasets.dataset.part.surrogate import SurrogateType

class BasePartCollection(ABC):

	def __getitem__(self, i):
		return self._parts[i]

	def __len__(self):
		return len(self._parts)

	def __repr__(self):
		if len(self._parts) == 0:
			return repr(self._parts)
		return repr(np.stack([p.as_annotation for p in self._parts]))

	@property
	def selected(self):
		return np.array([p.is_visible for p in self._parts], dtype=bool)

	@property
	def selected_idxs(self):
		return np.where(self.selected)[0]

	def select(self, idxs):
		if isinstance(idxs, np.ndarray) and idxs.dtype == bool:
			# a mask is present, so convert it to indeces
			idxs = np.where(idxs)[0]

		for p in self._parts:
			p.is_visible = p._id in idxs

	def hide_outside_bb(self, *bounding_box):
		for p in self._parts:
			p.hide_if_outside(*bounding_box)

	def invert_selection(self):
		self.select(np.logical_not(self.selected))

	def offset(self, dx, dy):
		for p in self._parts:
			p.x += dx
			p.y += dy

	def visible_locs(self):
		vis = [(p._id, p.xy) for p in self._parts if p.is_visible]
		idxs, xy = zip(*vis)
		return np.array(idxs), np.array(xy).T

	def visible_crops(self, *args, **kwargs):
		crops = [p.crop(*args, **kwargs) for p in self._parts]
		return crops
		# return np.array(crops)

	def plot(self, cmap=plt.cm.jet, **kwargs):
		for i, p in enumerate(self._parts):
			p.plot(color=cmap(i/len(self._parts)), **kwargs)

	def reveal(self, im, ratio, *args, **kwargs):
		res = np.zeros_like(im)

		for part in self._parts:
			if not part.is_visible: continue
			x, y, crop = part.reveal(im, ratio=ratio, *args, **kwargs)
			h, w, _ = crop.shape
			res[y:y+h, x:x+w] = crop

		return res




class BasePart(ABC):
	_surrogate_type: SurrogateType = SurrogateType.DEFAULT

	def __repr__(self):
		return repr(self.as_annotation)

	@staticmethod
	def new(image, annotation, rescale_size=-1, center_cropped=True, surrogate_type=None):
		from .annotation import BBoxPart, LocationPart
		if len(annotation) == 4:
			return LocationPart(image, annotation, rescale_size, surrogate_type=surrogate_type)
		elif len(annotation) == 5:
			return BBoxPart(image, annotation, rescale_size, center_cropped)
		else:
			raise ValueError("Unknown part annotation format: {}".format(annotation))

	def rescale(self, image, annotation, rescale_size, center_cropped=True):
		if rescale_size is not None and rescale_size > 0:
			xy = annotation[1:3]
			new_xy = utils.rescale(image, xy, rescale_size, center_cropped)
			annotation[1:3] = new_xy
		return annotation

	@property
	def is_visible(self):
		return self._is_visible

	@is_visible.setter
	def is_visible(self, value):
		self._is_visible = bool(value)

	@property
	def xy(self):
		return np.array([self.x, self.y])

	def crop(self, im, w, h, padding_mode="edge", is_location=True):
		if not self.is_visible:
			surrogate = self._surrogate_type
			if surrogate is not None and callable(surrogate):
				return surrogate(im, w, h, dtype=np.uint8)
			else:
				warnings.warn("Part surrogate was not set, but is needed! Returning blank patch as fallback.")
				_, _, c = utils.dimensions(im)
				return np.zeros((h, w, c), dtype=np.uint8)

		x, y = self.xy
		pad_h, pad_w = h // 2, w // 2

		padded_im = np.pad(im, [(pad_h, pad_h), (pad_w, pad_w), [0,0]], mode=padding_mode)
		x0, y0 = x + pad_w, y + pad_h

		if is_location:
			x0, y0 = x0 - w // 2, y0 - h // 2

		return padded_im[y0:y0+h, x0:x0+w]

	@abstractproperty
	def middle(self):
		raise NotImplementedError

	def plot(self, **kwargs):
		return

	def hide_if_outside(self, x, y, w, h):
		mid_x, mid_y = self.middle
		self.is_visible = ((x <= mid_x <= x+w) and (y <= mid_y <= y+h))
