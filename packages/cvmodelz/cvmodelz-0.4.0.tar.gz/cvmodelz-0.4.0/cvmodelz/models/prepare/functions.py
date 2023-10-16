import numpy as np

from chainercv import transforms as tr
from collections.abc import Iterable

class GenericPrepare:

	def __init__(self, size,
		crop_fraction=0.875,
		swap_channels=True,
		zero_mean=False,
		keep_ratio=True):
		super().__init__()

		self.crop_fraction = crop_fraction
		self.swap_channels = swap_channels
		self.zero_mean = zero_mean
		self.keep_ratio = keep_ratio

	def __call__(self, im, size=None, *args, swap_channels=None, keep_ratio=None, zero_mean=None, **kwargs):
		size = self.size if size is None else size
		swap_channels = self.swap_channels if swap_channels is None else swap_channels
		keep_ratio = self.keep_ratio if keep_ratio is None else keep_ratio
		zero_mean = self.zero_mean if zero_mean is None else zero_mean

		crop_size = None
		h, w, c = im.shape

		_im = im.transpose(2, 0, 1)

		if self.swap_channels:
			# RGB -> BGR
			_im = _im[::-1]

		if self.crop_fraction:
			crop_size = (np.array([h, w]) * self.crop_fraction).astype(np.int32)
			_im = tr.center_crop(_im, crop_size)

		# bilinear interpolation
		if self.keep_ratio:
			if isinstance(size, tuple):
				size = size[0]
			_im = tr.scale(_im, size, interpolation=2)
		else:
			if isinstance(size, int):
				size = (size, size)
			_im = tr.resize(_im, size, interpolation=2)

		if _im.dtype == np.uint8:
			# rescale [0 .. 255] -> [0 .. 1]
			_im = (_im / 255).astype(np.float32)


		if self.zero_mean:
			# rescale [0 .. 1] -> [-1 .. 1]
			_im = _im * 2 - 1

		return _im



class GenericTFPrepare:

	def __init__(self, size, crop_fraction, from_path):
		super().__init__()

		import tensorflow as tf
		config_sess = tf.ConfigProto(allow_soft_placement=True)
		config_sess.gpu_options.allow_growth = True
		self.sess = tf.Session(config=config_sess)

		self.from_path = from_path
		if from_path:
			self.im_input = im_input = tf.placeholder(tf.string)
			image = tf.image.decode_jpeg(tf.read_file(im_input), channels=3)
			image = tf.image.convert_image_dtype(image, tf.float32)
		else:
			self.im_input = image = im_input = tf.placeholder(tf.float32, shape=(None, None, 3))


		raise NotImplementedError("REFACTOR ME!")
		image = tf.image.central_crop(image, central_fraction=crop_fraction)
		image = tf.expand_dims(image, 0)
		image = tf.image.resize_bilinear(image, [size, size], align_corners=False)
		image = tf.squeeze(image, [0])
		image = tf.subtract(image, 0.5)
		self.output = tf.multiply(image, 2)


	def __call__(self, im, *args, **kwargs):
		if not self.from_path and im.dtype == np.uint8:
			im = im / 255

		res = self.sess.run(self.output, feed_dict={self.im_input: im})
		return res.transpose(2, 0, 1)

class ChainerCV2Prepare:


	def __init__(self, size, *, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)):
		super().__init__()
		self.size = size
		self.mean = np.array(mean, dtype=np.float32).reshape(-1, 1, 1)
		self.std = np.array(std, dtype=np.float32).reshape(-1, 1, 1)


	def _size(self, size):
		size = self.size if size is None else size
		if isinstance(size, Iterable):
			size = min(size)
		return size

	def __call__(self, im, size=None, *args, **kwargs):

		_im = im.transpose(2, 0, 1)
		_im = _im.astype(np.float32) / 255.0
		_im = tr.scale(_im, self._size(size), interpolation=2)

		_im -= self.mean
		_im /= self.std

		return _im
