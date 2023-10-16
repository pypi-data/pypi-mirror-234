from cvmodelz.models.pretrained.inception.inception_v3 import InceptionV3

class InceptionV3HD(InceptionV3):
	def init_model_info(self):
		super().init_model_info()
		self.meta.name +=  "HD"

	def init_extra_layers(self, n_classes) -> None:
		super().init_extra_layers(n_classes)

		self.mixed03.conv3x3.conv.stride = (1, 1)
		self.mixed03.conv3x3.conv.pad = (1, 1)
		self.mixed03.conv3x3_3.conv.stride = (1, 1)
		self.mixed03.conv3x3_3.conv.pad = (1, 1)
		self.mixed03.pool.keywords["stride"] = 1
		self.mixed03.pool.keywords["pad"] = 1

		self.mixed08.conv3x3_2.conv.stride = (1, 1)
		self.mixed08.conv3x3_2.conv.pad = (1, 1)
		self.mixed08.conv7x7_4.conv.stride = (1, 1)
		self.mixed08.conv7x7_4.conv.pad = (1, 1)
		self.mixed08.pool.keywords["stride"] = 1
		self.mixed08.pool.keywords["pad"] = 1
