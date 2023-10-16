import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np

from chainercv.transforms import resize
from chainercv.transforms import scale
from collections import OrderedDict
from collections.abc import Iterable


from cvmodelz.models.meta_info import ModelInfo
from cvmodelz.models.pretrained.base import PretrainedModelMixin
from cvmodelz.models.pretrained.inception import blocks
from cvmodelz.models.pretrained.inception import link_mappings
from cvmodelz.utils.links.pooling import PoolingType


def _assign(name, param, data):
	assert data.shape == param.shape, \
		"\"{}\" does not match the shape: {} != {}!".format(
			name, data.shape, param.shape)
	if isinstance(param, chainer.variable.Parameter):
		param.data[:] = data
	else:
		param[:] = data

def _assign_batch_norm(name, link, beta, avg_mean, avg_var):
	_assign(name, link.beta, beta)
	_assign(name, link.avg_mean, avg_mean)
	_assign(name, link.avg_var, avg_var)



"""
We need this to "extract" pretrained_model argument,
otherwise it would be passed to the constructor of the
chainer.Chain class, where it raises an error
"""
class InceptionV3Layers(chainer.Chain):


	def __init__(self, pretrained_model=None, aux_logits=False, *args, **kwargs):
		self.aux_logits = aux_logits
		super().__init__(*args, **kwargs)


class InceptionV3(PretrainedModelMixin, InceptionV3Layers):

	def init_model_info(self):
		self.meta = ModelInfo(
			name="InceptionV3",
			input_size=299,
			feature_size=2048,
			n_conv_maps=2048,

			conv_map_layer="mixed10",
			feature_layer="pool",

			classifier_layers=["fc"],

			prepare_func=self.prepare
		)

	@property
	def functions(self):
		super().functions

	def prepare(self, x, size=None, *, swap_channels=False, keep_ratio=True):
		size = size or self.meta.input_size

		# [0 .. 255] -> [0 .. 1]
		x = x.astype(np.float32) / 255

		# HWC -> CHW channel order
		x = x.transpose(2,0,1)

		if keep_ratio:
			if isinstance(size, Iterable):
				size = min(size)
			# scale the smallest side to <size>
			x = scale(x, size=size)
		else:
			if isinstance(size, int):
				size = (size, size)

			# resize the image to  side to <size>x<size>
			x = resize(x, size)

		if swap_channels:
			x = x[::-1]
		return x


	def forward(self, x, layer_name='fc'):
		aux_logit = None
		for key, funcs in self.functions.items():
			for func in funcs:
				x = func(x)

				if chainer.config.train and self.aux_logits and func == self.mixed07:
					aux_logit = self.aux(x)

			if key == layer_name:
				return x if aux_logit is None else (x, aux_logit)

	@property
	def functions(self):

		names = ["mixed{:02d}".format(i) for i in range(11)]
		body = [(name, [getattr(self, name)]) for name in names]
		links = [
			("head", [self.head]),
		] + body + [
			("pool", [self.pool]),
			("fc", [self.fc]),
		]

		return OrderedDict(links)

	def extract(self, x):
		x = self.head(x)
		x = self.mixed00(x)
		x = self.mixed01(x)
		x = self.mixed02(x)
		x = self.mixed03(x)
		x = self.mixed04(x)
		x = self.mixed05(x)
		x = self.mixed06(x)
		x = self.mixed07(x)
		x = self.mixed08(x)
		x = self.mixed09(x)
		x = self.mixed10(x)

		return self.pool(x)


	def load(self, weights, *args, **kwargs) -> None:
		if isinstance(weights, str) and weights.endswith(".h5"):
			return self._load_from_keras(weights)
		elif isinstance(weights, str) and weights.endswith(".ckpt.npz"):
			return self._load_from_ckpt_weights(weights)

		return super().load(weights, *args, **kwargs)

	def init_extra_layers(self, n_classes) -> None:
		# input 3 x 299 x 299
		self.head = blocks.InceptionHead()
		# output 192 x 35 x 35


		pool_args = dict(pool_type=PoolingType.TF_AVG, ksize=3, stride=1, pad=1)
		# input 192 x 35 x 35
		self.mixed00 = blocks.Inception1(insize=192, sizes=[48, 64, 96], outputs=[64, 64, 96, 32], **pool_args)
		# input 256 x 35 x 35
		self.mixed01 = blocks.Inception1(insize=256, sizes=[48, 64, 96], outputs=[64, 64, 96, 64], **pool_args)
		# input 288 x 35 x 35
		self.mixed02 = blocks.Inception1(insize=288, sizes=[48, 64, 96], outputs=[64, 64, 96, 64], **pool_args)

		pool_args = dict(pool_type=PoolingType.MAX, ksize=3, stride=2, pad=0)
		# input 288 x 35 x 35
		self.mixed03 = blocks.Inception2(288, sizes=[64, 96], outputs=[384, 96], **pool_args)

		# input 768 x 17 x 17
		pool_args = dict(pool_type=PoolingType.TF_AVG, ksize=3, stride=1, pad=1)
		# input 768 x 17 x 17
		self.mixed04 = blocks.Inception3(768, sizes=[128] * 6, outputs=[192] * 4, **pool_args)
		# input 768 x 17 x 17
		self.mixed05 = blocks.Inception3(768, sizes=[160] * 6, outputs=[192] * 4, **pool_args)
		# input 768 x 17 x 17
		self.mixed06 = blocks.Inception3(768, sizes=[160] * 6, outputs=[192] * 4, **pool_args)
		# input 768 x 17 x 17
		self.mixed07 = blocks.Inception3(768, sizes=[192] * 6, outputs=[192] * 4, **pool_args)

		self.aux = blocks.AuxilaryClassifier(n_classes) if self.aux_logits else F.identity

		pool_args = dict(pool_type=PoolingType.MAX, ksize=3, stride=2, pad=0)
		# input 768 x 17 x 17
		self.mixed08 = blocks.Inception4(768, sizes=[192] * 4, outputs=[320, 192], **pool_args)
		# output 1280 x 8 x 8

		# input 1280 x 8 x 8
		pool_args = dict(pool_type=PoolingType.TF_AVG, ksize=3, stride=1, pad=1)
		# input 1280 x 8 x 8
		self.mixed09 = blocks.Inception5(1280, sizes=[384, 448, 384], outputs=[320, 384, 384, 192], **pool_args)
		# input 2048 x 8 x 8
		self.mixed10 = blocks.Inception5(2048, sizes=[384, 448, 384], outputs=[320, 384, 384, 192], **pool_args)

		# input 2048 x 8 x 8
		# global average pooling
		# output 2048 x 1 x 1

		# the final fc layer is initilized by PretrainedModelMixin
		super().init_extra_layers(n_classes)

	def loss(self, pred, gt, *, loss_func=F.softmax_cross_entropy, alpha=0.4, **kwargs):
		if isinstance(pred, tuple):
			pred0, aux_pred = pred
		else:
			pred0, aux_pred = pred, None

		loss = loss_func(pred0, gt, **kwargs)
		if aux_pred is None:
			return loss
		else:
			aux_loss = loss_func(aux_pred, gt, **kwargs)
			return (1-alpha) * loss + alpha * aux_loss

	def accuracy(self, pred, gt):
		if isinstance(pred, tuple):
			pred0, aux_pred = pred
		else:
			pred0, aux_pred = pred, None
		return F.accuracy(pred0, gt)

	def _load_from_ckpt_weights(self, weights):
		content = np.load(weights)
		for name, link in self.namedlinks(skipself=True):
			if name not in link_mappings.chainer_to_tf_ckpt:
				continue

			ckpt_key = link_mappings.chainer_to_tf_ckpt[name]

			if isinstance(link, L.Convolution2D):
				W = content["{}/weights".format(ckpt_key)]
				W = W.transpose(3,2,0,1)
				_assign(name, link.W, W)

			elif isinstance(link, L.BatchNormalization):
				beta = content["{}/beta".format(ckpt_key)]
				avg_mean = content["{}/moving_mean".format(ckpt_key)]
				avg_var = content["{}/moving_variance".format(ckpt_key)]
				_assign_batch_norm(name, link, beta, avg_mean, avg_var)

			elif isinstance(link, L.Linear):
				W = content["{}/weights".format(ckpt_key)]
				W = W.transpose(3,2,0,1).squeeze()
				b = content["{}/biases".format(ckpt_key)]
				_assign(name, link.W, W)
				_assign(name, link.b, b)

			else:
				raise ValueError("Unkown link type: {}!".format(type(link)))

	def _load_from_keras(self, weights):
		import h5py
		with h5py.File(weights, "r") as f:
			if "model_weights" in f:
				f = f["model_weights"]
			for name, link in self.namedlinks(skipself=True):
				if name not in link_mappings.chainer_to_keras: continue
				keras_key = link_mappings.chainer_to_keras[name]

				if isinstance(link, L.Convolution2D):
					W = np.asarray(f[keras_key][keras_key + "/kernel:0"])
					W = W.transpose(3,2,0,1)

					_assign(name, link.W, W)

				elif isinstance(link, L.Linear):
					W = np.asarray(f[keras_key][keras_key + "/kernel:0"])
					b = np.asarray(f[keras_key][keras_key + "/bias:0"])

					_assign(name, link.W, W.transpose(1,0))
					_assign(name, link.b, b)

				elif isinstance(link, L.BatchNormalization):
					beta = np.asarray(f[keras_key][keras_key + "/beta:0"])
					avg_mean = np.asarray(f[keras_key][keras_key + "/moving_mean:0"])
					avg_var = np.asarray(f[keras_key][keras_key + "/moving_variance:0"])

					_assign_batch_norm(name, link, beta, avg_mean, avg_var)
				else:
					raise ValueError("Unkown link type: {}!".format(type(link)))
