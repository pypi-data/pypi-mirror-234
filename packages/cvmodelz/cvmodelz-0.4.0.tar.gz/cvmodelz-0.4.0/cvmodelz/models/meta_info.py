import pyaml
import types

from dataclasses import dataclass
from typing import Tuple
from typing import Callable

pyaml.add_representer(types.FunctionType, lambda cls, func: cls.represent_data(str(func)))
pyaml.add_representer(types.MethodType, lambda cls, func: cls.represent_data(str(func)))

@dataclass
class ModelInfo(object):

	name:                       str         = "GenericModel"
	input_size:                 int         = 224
	feature_size:               int         = 2048
	n_conv_maps:                int         = 2048

	conv_map_layer:             str         = "conv"
	feature_layer:              str         = "fc"

	classifier_layers:          Tuple[str]  = ("fc",)

	prepare_func:               Callable    = lambda x: x  # noqa: E731

	def prepare(self, foo):
		pass

	def __str__(self):
		obj = dict(ModelInfo=self.__dict__)
		return pyaml.dump(obj, sort_dicts=False, )


if __name__ == '__main__':
	info = ModelInfo()
	print(info)

	info = ModelInfo(prepare_func=info.prepare)
	print(info)
