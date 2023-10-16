import chainer

from chainer import functions as F
from chainer import links as L
from chainer.links.model.vision.resnet import BuildingBlock
from chainer.links.model.vision.resnet import prepare
from collections import OrderedDict
from functools import partial


from cvmodelz.models.meta_info import ModelInfo
from cvmodelz.models.pretrained.base import PretrainedModelMixin

class BaseResNet(PretrainedModelMixin):
	n_layers = ""

	def init_model_info(self):
		self.meta = ModelInfo(
			name=f"ResNet{self.n_layers}",
			input_size=224,
			feature_size=2048,
			n_conv_maps=2048,

			conv_map_layer="res5",
			feature_layer="pool5",

			classifier_layers=["fc6"],

			prepare_func=self.prepare,
		)

	def prepare(self, x, size=None, *, swap_channels=True, keep_ratio=True):
		size = size or self.meta.input_size

		if isinstance(size, int):
			size = (size, size)

		x = prepare(x, size)

		# if not desired, we need to undo it
		if not swap_channels:
			x = x[:, :, ::-1]

		return x

	@property
	def functions(self):
		return super().functions

class ResNetHDMixin:

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.res4.a.conv1.stride = (1, 1)
		self.res4.a.conv4.stride = (1, 1)

		self.res5.a.conv1.stride = (1, 1)
		self.res5.a.conv4.stride = (1, 1)

"""
We need this to "extract" pretrained_model argument,
otherwise it would be passed to the constructor of the
chainer.Chain class, where it raises an error
"""
class ResNet35Layers(chainer.Chain):

	def __init__(self, *args, pretrained_model=None, **kwargs):
		super().__init__(*args, **kwargs)


class ResNet35(BaseResNet, ResNet35Layers):
	n_layers = 35

	def init_extra_layers(self, *args, **kwargs):
		self.conv1 = L.Convolution2D(3, 64, 7, 2, 3, **kwargs)
		self.bn1 = L.BatchNormalization(64)
		self.res2 = BuildingBlock(2, 64, 64, 256, 1, **kwargs)
		self.res3 = BuildingBlock(3, 256, 128, 512, 2, **kwargs)
		self.res4 = BuildingBlock(3, 512, 256, 1024, 2, **kwargs)
		self.res5 = BuildingBlock(3, 1024, 512, 2048, 2, **kwargs)

		# the final fc layer is initilized by PretrainedModelMixin
		super().init_extra_layers(*args, **kwargs)

	@property
	def functions(self):
		links = [
			("conv1", [self.conv1, self.bn1, F.relu]),
			("pool1", [partial(F.max_pooling_2d, ksize=3, stride=2)]),
			("res2", [self.res2]),
			("res3", [self.res3]),
			("res4", [self.res4]),
			("res5", [self.res5]),
			("pool5", [self.pool]),
			("fc6", [self.fc6]),
			("prob", [F.softmax]),
		]
		return OrderedDict(links)

	def forward(self, x, layer_name=None):
		for key, funcs in self.functions.items():
			for func in funcs:
				x = func(x)
			if key == layer_name:
				return x


class ResNet35HD(ResNetHDMixin, ResNet35):
	pass

class ResNet50(BaseResNet, L.ResNet50Layers):
	n_layers = 50

class ResNet50HD(ResNetHDMixin, ResNet50):
	pass

class ResNet101(BaseResNet, L.ResNet101Layers):
	n_layers = 101


class ResNet152(BaseResNet, L.ResNet152Layers):
	n_layers = 152

