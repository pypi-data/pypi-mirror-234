from cvmodelz.models.prepare import functions as F

from cvargparse.utils.enumerations import BaseChoiceType


class PrepareType(BaseChoiceType):
	MODEL = 0
	CUSTOM = 1
	TF = 2
	CHAINERCV2 = 3

	Default = MODEL

	def __call__(self, model):
		"""
			Initializes image preprocessing function
		"""

		if self == PrepareType.MODEL:
			return model.meta.prepare_func

		elif self == PrepareType.CUSTOM:
			return F.GenericPrepare(
				size=model.meta.input_size)

		elif self == PrepareType.TF:
			return F.GenericTFPrepare(
				size=model.meta.input_size,
				from_path=False)

		elif self == PrepareType.CHAINERCV2:
			return F.ChainerCV2Prepare(
				size=model.meta.input_size)
