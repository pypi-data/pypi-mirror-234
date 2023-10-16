from chainer import links as L

from cvmodelz.models.base import BaseModel

class PretrainedModelMixin(BaseModel):
	"""
		This mixin is designed to be a superclass besides one of
		chainer's built in models (VGG, ResNet, GoogLeNet).

		Example:

			import chainer.links as L
			class OurResNet(PretrainedModelMixin, L.ResNet50layers):
				...
	"""

	def __init__(self, *args, n_classes: int = 1000, pretrained_model: str = None, **kwargs):
		super().__init__(*args, pretrained_model=pretrained_model, **kwargs)

		with self.init_scope():
			self.init_extra_layers(n_classes)

		self.load(pretrained_model, strict=True)

	def forward(self, X, layer_name=None):
		assert hasattr(self, "meta"), "Did you forgot to initialize the meta attribute?"

		layer_name = layer_name or self.meta.classifier_layers[-1]
		caller = super().forward
		activations = caller(X, layers=[layer_name])

		if isinstance(activations, dict):
			activations = activations[layer_name]

		return activations

	def init_extra_layers(self, n_classes, **kwargs) -> None:
		if hasattr(self, self.clf_layer_name):
			delattr(self, self.clf_layer_name)

		clf_layer = L.Linear(self.meta.feature_size, n_classes)
		setattr(self, self.clf_layer_name, clf_layer)

	@property
	def model_instance(self) -> BaseModel:
		""" since it is a mixin, we are the model """

		return self

