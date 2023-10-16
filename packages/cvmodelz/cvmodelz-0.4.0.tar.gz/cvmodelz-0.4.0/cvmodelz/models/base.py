import abc
import chainer
import io
import numpy as np

from chainer import functions as F
from chainer import links as L
from chainer.initializers import HeNormal
from chainer.serializers import npz
from collections import OrderedDict
from typing import Callable

from cvmodelz import utils
from cvmodelz.models.meta_info import ModelInfo
from cvmodelz.utils.links.pooling import PoolingType

class BaseModel(abc.ABC, chainer.Chain):

	def __init__(self, pooling: Callable = PoolingType.G_AVG,
		input_size=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.init_model_info()

		if isinstance(pooling, (PoolingType, str)):
			pooling = PoolingType.new(pooling)

		with self.init_scope():
			self.pool = pooling

		if input_size is not None:
			self.meta.input_size = input_size


	def init_model_info(self):
		self.meta = ModelInfo()

	@abc.abstractmethod
	def forward(self, *args, **kwargs):
		return super().forward(*args, **kwargs)

	@abc.abstractproperty
	def functions(self) -> OrderedDict:
		return super().functions

	@abc.abstractproperty
	def model_instance(self) -> chainer.Chain:
		raise NotImplementedError()

	@property
	def clf_layer_name(self) -> str:
		return self.meta.classifier_layers[-1]

	@property
	def clf_layer(self) -> chainer.Link:
		return utils.get_attr_from_path(self.model_instance, self.clf_layer_name)

	def loss(self, pred, gt, *, loss_func=F.softmax_cross_entropy, **kwargs):
		return loss_func(pred, gt, **kwargs)

	def accuracy(self, pred, gt):
		return F.accuracy(pred, gt)

	def reinitialize_clf(self, n_classes, feat_size=None, initializer=None):

		if initializer is None or not callable(initializer):
			initializer = HeNormal(scale=1.0)

		clf_layer = self.clf_layer

		assert isinstance(clf_layer, L.Linear)

		w_shape = (n_classes, feat_size or clf_layer.W.shape[1])
		dtype = clf_layer.W.dtype

		clf_layer.out_size, clf_layer.in_size = w_shape
		clf_layer.W.data = np.zeros(w_shape, dtype=dtype)
		clf_layer.b.data = np.zeros(w_shape[0], dtype=dtype)

		initializer(clf_layer.W.data)

	def load_for_finetune(self, weights, n_classes, *, path="", strict=False, headless=False, **kwargs):
		"""
			The weights should be pre-trained on a bigger
			dataset (eg. ImageNet). The classification layer is
			reinitialized after all other weights are loaded
		"""
		self.load(weights, path=path, strict=strict, headless=headless)
		self.reinitialize_clf(n_classes, **kwargs)

	def load_for_inference(self, weights, n_classes, *, path="", strict=False, headless=False, **kwargs):
		"""
			In this use case we are loading already fine-tuned
			weights. This means, we need to reinitialize the
			classification layer first and then load the weights.
		"""
		self.reinitialize_clf(n_classes, **kwargs)
		self.load(weights, path=path, strict=strict, headless=headless)

	def load(self, weights, *, path="", strict=False, headless=False):
		if weights in [None, "auto"]:
			return

		ignore_names = None
		if headless:
			ignore_names = lambda name: name.startswith(path + self.clf_layer_name)

		if isinstance(weights, io.BufferedIOBase):
			assert not weights.closed, "The weights file was already closed!"
			weights.seek(0)

		npz.load_npz(weights, self.model_instance,
			path=path, strict=strict, ignore_names=ignore_names)

	def save(self, path, *args, **kwargs):
		npz.save_npz(path, self, *args, **kwargs)
