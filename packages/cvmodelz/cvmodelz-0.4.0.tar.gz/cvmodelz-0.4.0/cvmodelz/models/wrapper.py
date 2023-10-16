import chainer

from collections import OrderedDict

from cvmodelz.models.base import BaseModel
from cvmodelz.models.meta_info import ModelInfo


class ModelWrapper(BaseModel):
	"""
		This class is designed to wrap around chainercv2 models
		and provide the loading API of the BaseModel class.
		The wrapped model is stored under self.wrapped
	"""

	def __init__(self, model: chainer.Chain, *args, **kwargs):
		name = model.__class__.__name__
		self.__class__.__name__ = name
		self.model_name = name
		super().__init__(*args, **kwargs)


		if hasattr(model, "meta"):
			self.meta = model.meta

		with self.init_scope():
			self.wrapped = model
			delattr(self.wrapped.features, "final_pool")


	def init_model_info(self):
		info = dict(
			name=self.model_name,
			feature_size=2048,
			n_conv_maps=2048,
			classifier_layers=["output/fc"],
			conv_map_layer="features",
			feature_layer="pool",
		)

		if self.model_name == "InceptionResNetV1":
			info.update(dict(
				input_size=299,
				feature_size=1792,
				n_conv_maps=1792,
				classifier_layers=[
					"output/fc1",
					"output/fc2"
				],
			))

		elif self.model_name == "InceptionV3":
			info.update(dict(
				input_size=299,
			))

		elif self.model_name in ["ResNet", "ResNeXt"]:
			info.update(dict(
				input_size=224,
			))

		self.meta = ModelInfo(**info)

	@property
	def model_instance(self) -> chainer.Chain:
		return self.wrapped

	@property
	def functions(self) -> OrderedDict:

		links = [
			(self.meta.conv_map_layer, [self.wrapped.features]),
			(self.meta.feature_layer, [self.pool]),
			(self.clf_layer_name, [self.wrapped.output]),
		]

		return OrderedDict(links)

	def load(self, *args, path="", **kwargs):
		paths = [path, f"{path}wrapped/"]
		for _path in paths:
			try:
				return super().load(*args, path=_path, **kwargs)
			except KeyError as e:
				pass

		raise RuntimeError(f"tried to load weights with paths {paths}, but did not succeeed")

	def forward(self, X, layer_name=None):
		if layer_name is None:
			res = self.wrapped(X)

		elif layer_name == self.meta.conv_map_layer:
			res = self.wrapped.features(X)

		elif layer_name == self.meta.feature_layer:
			conv = self.wrapped.features(X)
			res = self.pool(conv)

		elif layer_name == self.clf_layer_name:
			conv = self.wrapped.features(X)
			feat = self.pool(conv)
			res = self.wrapped.output(feat)

		else:
			raise ValueError(f"Dont know how to compute \"{layer_name}\"!")

		return res

