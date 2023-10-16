import abc
import pyaml


from chainer import links as L
from chainercv2.models import inceptionv3 as cv2inceptionv3
from chainercv2.models import inceptionresnetv1 as cv2inceptionresnetv1
from chainercv2.models import resnext as cv2resnext
from chainercv2.models import resnet as cv2resnet
from chainercv.links.model import ssd
from chainercv.links.model import faster_rcnn
from collections import OrderedDict

from cvmodelz.models import pretrained
from cvmodelz.models.wrapper import ModelWrapper

class ModelFactory(abc.ABC):

	supported = OrderedDict(
		chainer=(
			L.ResNet50Layers,
			L.ResNet101Layers,
			L.ResNet152Layers,
			# L.VGG16Layers,
			# L.VGG19Layers,
		),

		chainercv=(
			ssd.SSD300,
			faster_rcnn.FasterRCNNVGG16,
		),

		chainercv2=(
			cv2resnet.resnet50,
			cv2resnet.resnet18,

			cv2inceptionv3.inceptionv3,
			cv2inceptionresnetv1.inceptionresnetv1,
			cv2resnext.resnext50_32x4d,
		),

		cvmodelz=(
			pretrained.VGG16,
			pretrained.VGG19,

			pretrained.ResNet35,
			pretrained.ResNet35HD,
			pretrained.ResNet50,
			pretrained.ResNet50HD,
			pretrained.ResNet101,
			pretrained.ResNet152,

			pretrained.InceptionV3,
			pretrained.InceptionV3HD,
		),
	)

	@abc.abstractmethod
	def __init__(self):
		raise NotImplementedError("instance creation is not supported!")

	@classmethod
	def new(cls, model_type, **kwargs):

		key, cls_name = model_type.split(".")

		for model_cls in cls.supported[key]:
			if model_cls.__name__ == cls_name:
				break
		else:
			raise ValueError(f"Could not find {model_type}!")

		if model_cls in cls.supported["chainercv2"]:
			n_classes = kwargs.pop("n_classes", 1000)
			pretrained = kwargs.pop("pretrained_model", None) == "auto"
			model = model_cls(classes=n_classes, pretrained=pretrained)
			kwargs["model"] = model
			model_cls = ModelWrapper

		return model_cls(**kwargs)


	@classmethod
	def _check(cls, model, key):
		return isinstance(model, cls.supported[key])

	@classmethod
	def is_chainer_model(cls, model):
		return cls._check(model, "chainer")

	@classmethod
	def is_cv_model(cls, model):
		return cls._check(model, "chainercv")

	@classmethod
	def is_cv2_model(cls, model):
		return cls._check(model, "chainercv2")

	@classmethod
	def is_cvmodelz_model(cls, model):
		return cls._check(model, "cvmodelz")

	@classmethod
	def get_all_models(cls, key=None):
		if key is not None:
			return [f"{key}.{model_cls.__name__}" for model_cls in cls.supported[key]]

		return cls.get_models(cls.supported.keys())

	@classmethod
	def get_models(cls, keys=None):
		if keys is None:
			keys = cls.supported.keys()

		res = []
		for key in keys:
			res += cls.get_all_models(key)

		return res


if __name__ == '__main__':
	print(pyaml.dump(dict(Models=ModelFactory.get_all_models()), indent=2))
