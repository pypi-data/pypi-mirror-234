import abc
import chainer

from chainer import functions as F
from typing import Callable
from typing import Dict

from cvmodelz.classifiers.base import Classifier
from cvmodelz.models.base import BaseModel



class SeparateModelClassifier(Classifier):
	"""
		Abstract Classifier, that holds two separate models.
		The user has to define, how these models operate on the
		input data. Hence, the forward method is abstract!
	"""

	def __init__(self, *args, copy_mode="copy", **kwargs):
		self.copy_mode = copy_mode
		super().__init__(*args, **kwargs)

	@abc.abstractmethod
	def forward(self, *args, **kwargs) -> chainer.Variable:
		super().forward(*args, **kwargs)

	def setup(self, model: BaseModel) -> None:
		super().setup(model)

		self.separate_model = self.model.copy(mode=self.copy_mode)

	def load_model(self, weights_file: str, n_classes: int, *, finetune: bool = False, **kwargs) -> None:
		for model in [self.model, self.separate_model]:
			model_loader = self.get_model_loader(finetune=finetune, model=model)
			kwargs["strict"] = kwargs.get("strict", True)
			model_loader(weights=weights_file, n_classes=n_classes, **kwargs)

	def enable_only_head(self) -> None:
		super().enable_only_head()
		self.separate_model.disable_update()
		self.separate_model.fc.enable_update()


class MeanModelClassifier(SeparateModelClassifier):

	def evaluations(self, pred0: chainer.Variable, pred1: chainer.Variable, y: chainer.Variable) -> Dict[str, chainer.Variable]:
		accu0 = self.model.accuracy(pred0, y)
		accu1 = self.separate_model.accuracy(pred1, y)

		mean_pred = (F.softmax(pred0) + F.softmax(pred1)) / 2

		accu = self.model.accuracy(mean_pred, y)

		return dict(
			accu0=accu0,
			accu1=accu1,
			accuracy=accu,
		)

	def forward(self, X: chainer.Variable, y: chainer.Variable) -> chainer.Variable:

		pred0 = self.model(X, layer_name=self.layer_name)
		pred1 = self.separate_model(X, layer_name=self.layer_name)

		loss0, loss1 = self.loss(pred0, y), self.loss(pred1, y)
		loss = (loss0 + loss1) / 2

		evaluations = self.evaluations(pred0, pred1, y)

		self.report(
			loss0=loss0,
			loss1=loss1,
			loss=loss,
			**evaluations
		)
		return loss



