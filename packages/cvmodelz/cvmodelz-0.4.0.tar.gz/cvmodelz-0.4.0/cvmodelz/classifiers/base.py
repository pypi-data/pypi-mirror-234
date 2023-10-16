import abc
import chainer
import io

from chainer import functions as F
from chainer.serializers import npz
from typing import Callable
from typing import Dict

from cvmodelz.models.base import BaseModel

class Classifier(chainer.Chain):

	def __init__(self, model: BaseModel, *,
		layer_name: str = None,
		loss_func: Callable = F.softmax_cross_entropy,
		only_head: bool = False,
		):
		super().__init__()
		self._only_head = only_head
		self.layer_name = layer_name or model.clf_layer_name
		self.loss_func = loss_func

		with self.init_scope():
			self.setup(model)

		if only_head:
			self.enable_only_head()

	def setup(self, model: BaseModel) -> None:
		self.model = model

	def report(self, **values) -> None:

		chainer.report({key: chainer.as_array(val) for key, val in values.items()}, self)

	def enable_only_head(self) -> None:
		self.model.disable_update()
		self.model.clf_layer.enable_update()

	@property
	def n_classes(self) -> int:
		return self.model.clf_layer.W.shape[0]

	def save(self, weights_file):
		npz.save_npz(weights_file, self)

	def load(self, weights_file: str, n_classes: int, *, finetune: bool = False, **kwargs) -> None:
		""" Loading a classifier has following use cases:

			(0) No loading.
				- All weights are initilized randomly.

			(1) Loading from default pre-trained weights
				- The weights are loaded directly to
				the model.
				- Any additional not model-related
				layer will be initialized randomly.

			(2) Loading from a saved classifier.
				- All weights are loaded as-it-is from
				the given file.
		"""

		try:
			# Case (2)
			return self.load_classifier(weights_file)

		except KeyError as e:
			pass

		# Case (1)
		self.load_model(weights_file, n_classes=n_classes, finetune=finetune, **kwargs)

		# else:
		# 	# Case (0)
		# 	pass

	def load_classifier(self, weights_file: str):

		if weights_file is None:
			return

		if isinstance(weights_file, io.BufferedIOBase):
			assert not weights_file.closed, "The weights file was already closed!"
			weights_file.seek(0)

		npz.load_npz(weights_file, self, strict=True)

	def get_model_loader(self, finetune: bool = False, model: BaseModel = None):
		model = model or self.model
		if finetune:
			return model.load_for_finetune
		else:
			return model.load_for_inference


	def load_model(self, weights_file: str, n_classes: int, *, finetune: bool = False, **kwargs):
		model_loader = self.get_model_loader(finetune=finetune, model=self.model)
		kwargs["strict"] = kwargs.get("strict", True)
		model_loader(weights=weights_file, n_classes=n_classes, **kwargs)

	@property
	def feat_size(self) -> int:
		return self.model.meta.feature_size

	@property
	def output_size(self) -> int:
		return self.feat_size

	def loss(self, pred: chainer.Variable, y: chainer.Variable, **kwargs) -> chainer.Variable:
		return self.model.loss(pred, y, loss_func=self.loss_func, **kwargs)

	def evaluations(self, pred: chainer.Variable, y: chainer.Variable) -> Dict[str, chainer.Variable]:
		return dict(accuracy=self.model.accuracy(pred, y))

	def forward(self, X: chainer.Variable, y: chainer.Variable) -> chainer.Variable:
		pred = self.model(X, layer_name=self.layer_name)

		loss = self.loss(pred, y)
		evaluations = self.evaluations(pred, y)

		self.report(loss=loss, **evaluations)
		return loss


