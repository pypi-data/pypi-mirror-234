from chainer import links as L
from chainer.links.model.vision.vgg import prepare as vgg_prepare
from chainer.links.model.vision.vgg import _max_pooling_2d

from cvmodelz.models.meta_info import ModelInfo
from cvmodelz.models.pretrained.base import PretrainedModelMixin


class BaseVGG(PretrainedModelMixin):

	def __init__(self, *args, **kwargs):
		kwargs["pooling"] = kwargs.get("pooling", _max_pooling_2d)
		super().__init__(*args, **kwargs)

	@property
	def functions(self):
		return super().functions

	def init_model_info(self):
		self.meta = ModelInfo(
			name="VGG",
			input_size=224,
			feature_size=4096,
			n_conv_maps=512,

			conv_map_layer=self.final_conv_layer,
			feature_layer="fc7",

			classifier_layers=["fc6", "fc7", "fc8"],

			prepare_func=self.prepare,
		)

	def prepare(self, x, size=None, *, swap_channels=True, keep_ratio=True):
		x = vgg_prepare(x, size=size)

		# if not desired, we need to undo it
		if not swap_channels:
			x = x[:, :, ::-1]

		return x

class VGG19(BaseVGG, L.VGG19Layers):
	final_conv_layer = "conv5_4"


class VGG16(BaseVGG, L.VGG16Layers):
	final_conv_layer = "conv5_3"

