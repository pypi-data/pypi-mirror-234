import numpy as np
import random
import typing as T
import warnings

try:
	import cv2
except ImportError as e:
	warnings.warn("OpencCV was not installed! Some of the image operations won't use the 'use_cv' flag")
	cv2_available = False
else:
	cv2_available = True

from PIL import Image
from functools import partial

def dimensions(im: T.Union[Image.Image, np.ndarray]) -> T.Tuple[int, int, int]:
	""" Generic method that return the height, width and number of
		channels for a given input. The input can be a numpy array
		or a PIL.Image instance.
	"""
	if isinstance(im, np.ndarray):
		if im.ndim != 3:
			import pdb; pdb.set_trace()
		assert im.ndim == 3, "Only RGB images are currently supported!"
		return im.shape

	elif isinstance(im, Image.Image):
		w, h = im.size
		c = len(im.getbands())
		# assert c == 3, "Only RGB images are currently supported!"
		return h, w, c

	else:
		raise ValueError("Unknown image instance ({})!".format(type(im)))

def rescale(im, coords, rescale_size, center_cropped=True, no_offset=False):
	""" Rescales coordinates for a given image.
		The assumption is that the (pixel) coordinates were estimated
		based on a different image resolution (rescale_size). This is
		typically the input size of the CNN that was used for the
		estimation of the coordinates (e.g. 224 or 448 for ResNets,
		299 or 427 for InceptionV3, or 227 for AlexNet).

		The parameter "center_cropped" indicates whether the input image
		was center cropped before resize or resized without preserving
		the original aspect ratio.

		If you want to rescale the width and height (e.g. of a bounding
		box) then you should set "no_offset=True"!
	"""

	h, w, c = dimensions(im)

	if np.all(coords == -1):
		return coords

	offset = 0
	if center_cropped:
		_min_val = min(w, h)
		wh = np.array([_min_val, _min_val])
		if not no_offset:
			offset = (np.array([w, h]) - wh) / 2

	else:
		wh = np.array([w, h])

	scale = wh / rescale_size
	return coords * scale + offset

####################
### Source: https://github.com/chainer/chainercv/blob/b52c71d9cd11dc9efdd5aaf327fed1a99df94d10/chainercv/transforms/image/color_jitter.py
####################
# from https://scikit-image.org/docs/dev/api/skimage.color.html#skimage.color.rgb2gray:
#	Y = 0.2125 R + 0.7154 G + 0.0721 B
GRAY_WEIGHTS = (0.2125, 0.7154, 0.0721)

#	from https://docs.opencv.org/4.7.0/de/d25/imgproc_color_conversions.html:
#	Y = 0.299 R + 0.587 G + 0.114 B
GRAY_WEIGHTS = (0.299, 0.587, 0.114)

def _grayscale(img, *, channel_order="RGB", use_cv=True, axis_order="CHW"):
	"""
		channel_order can be either 'RGB' or 'BGR'
		axis_order can be either 'CHW' or 'HWC'
	"""
	global GRAY_WEIGHTS

	assert channel_order in ["RGB", "BGR"], f"Unknown channel order: {channel_order}"
	assert axis_order in ["CHW", "HWC"], f"Unknown axis order: {axis_order}"

	w = GRAY_WEIGHTS if channel_order == "RGB" else reversed(GRAY_WEIGHTS)

	if use_cv and cv2_available and axis_order == "HWC":
		mode = cv2.COLOR_RGB2GRAY if channel_order == "RGB" else cv2.COLOR_BGR2GRAY
		return cv2.cvtColor(img, mode)

	if axis_order == "HWC":
		R, G, B = img[..., 0], img[..., 1], img[..., 2]

	elif axis_order == "CHW":
		R, G, B = img[0], img[1], img[2]

	if use_cv and cv2_available:
		return cv2.addWeighted(cv2.addWeighted(R, w[0], G, w[1], 0), 1, B, w[2], 0)

	return w[0] * R + w[1] * G + w[2] * B

def _blend(img_a, img_b, alpha, *, use_cv=True):
	if use_cv and cv2_available:
		if img_a.shape == img_b.shape:
			return cv2.addWeighted(img_a,alpha, img_b,1-alpha,0)
		# else:
		# 	import pdb; pdb.set_trace()
	return alpha * img_a + (1 - alpha) * img_b


def _brightness(img, var):
	alpha = 1 + np.random.uniform(-var, var)
	return _blend(img, np.zeros_like(img), alpha), alpha


def _contrast(img, var, **kwargs):
	gray = _grayscale(img, **kwargs)[0].mean()

	alpha = 1 + np.random.uniform(-var, var)
	return _blend(img, gray, alpha), alpha


def _saturation(img, var, **kwargs):
	gray = _grayscale(img, **kwargs)

	alpha = 1 + np.random.uniform(-var, var)
	return _blend(img, gray, alpha), alpha


def color_jitter(img, brightness=0.4, contrast=0.4,
				 saturation=0.4, return_param=False,
				 min_value=0,
				 max_value=255,
				 channel_order="RGB"):
	"""Data augmentation on brightness, contrast and saturation.
	Args:
		img (~numpy.ndarray): An image array to be augmented. This is in
			CHW and RGB format.
		brightness (float): Alpha for brightness is sampled from
			:obj:`unif(-brightness, brightness)`. The default
			value is 0.4.
		contrast (float): Alpha for contrast is sampled from
			:obj:`unif(-contrast, contrast)`. The default
			value is 0.4.
		saturation (float): Alpha for contrast is sampled from
			:obj:`unif(-saturation, saturation)`. The default
			value is 0.4.
		return_param (bool): Returns parameters if :obj:`True`.
	Returns:
		~numpy.ndarray or (~numpy.ndarray, dict):
		If :obj:`return_param = False`,
		returns an color jittered image.
		If :obj:`return_param = True`, returns a tuple of an array and a
		dictionary :obj:`param`.
		:obj:`param` is a dictionary of intermediate parameters whose
		contents are listed below with key, value-type and the description
		of the value.
		* **order** (*list of strings*): List containing three strings: \
			:obj:`'brightness'`, :obj:`'contrast'` and :obj:`'saturation'`. \
			They are ordered according to the order in which the data \
			augmentation functions are applied.
		* **brightness_alpha** (*float*): Alpha used for brightness \
			data augmentation.
		* **contrast_alpha** (*float*): Alpha used for contrast \
			data augmentation.
		* **saturation_alpha** (*float*): Alpha used for saturation \
			data augmentation.
	"""
	funcs = list()
	if brightness > 0:
		funcs.append(('brightness', partial(_brightness, var=brightness)))
	if contrast > 0:
		funcs.append(('contrast', partial(_contrast, var=contrast, channel_order=channel_order)))
	if saturation > 0:
		funcs.append(('saturation', partial(_saturation, var=saturation, channel_order=channel_order)))
	random.shuffle(funcs)

	params = {'order': [key for key, val in funcs],
			  'brightness_alpha': 1,
			  'contrast_alpha': 1,
			  'saturation_alpha': 1}
	for key, func in funcs:
		img, alpha = func(img)
		params[key + '_alpha'] = alpha

	if min_value is not None:
		img = np.maximum(img, min_value)

	if max_value is not None:
		img = np.minimum(img, max_value)

	if return_param:
		return img, params
	else:
		return img



if __name__ == '__main__':
	import time
	from tqdm.auto import tqdm
	from functools import partial

	shape, order = (3, 600, 600), "CHW"
	# shape, order = (600, 600, 3), "HWC"
	small_shape = (max(shape), max(shape))
	iterations = 6_000

	im = np.random.randint(0, 255, size=shape, dtype=np.uint8)
	im2 = np.random.randint(0, 255, size=shape, dtype=np.uint8)
	im3 = np.random.randint(0, 255, size=small_shape, dtype=np.uint8)

	res0 = _blend(im, im2, alpha=0.5, use_cv=True).astype(np.int32)
	res1 = _blend(im, im2, alpha=0.5, use_cv=False).astype(np.int32)
	diff = np.abs(res0-res1)
	assert np.all(diff <= 2)


	res0 = _grayscale(im, use_cv=True).astype(np.int32)
	res1 = _grayscale(im, use_cv=False).astype(np.int32)
	diff = np.abs(res0-res1)
	assert np.all(diff <= 2)

	funcs = [
		(partial(_grayscale, axis_order=order), f"Grayscale on {order}"),
		(partial(_blend, img_b=im2, alpha=0.5), "Blending with same size"),
		(partial(_blend, img_b=im3, alpha=0.5), "Blending with smaller size"),
	]

	for func, func_name in funcs:
		for use_cv in [True, False]:
			desc = f"{func_name} with{'' if use_cv else 'out'} OpenCV"
			t0 = time.time()
			for n in tqdm(range(iterations), desc=desc):
				res = func(im, use_cv=use_cv)
			t = time.time() - t0

			print(f"{iterations} iterations took {t:.3f}sec ({t/iterations * 1000:.3f} ms/iter)")
