from functools import reduce
import chainer
import numpy as np
import sys
import logging

from functools import partial
from tabulate import tabulate

from chainer.function_hooks import TimerHook
from chainer.function_hooks import CupyMemoryProfileHook


def get_attr_from_path(obj, path, *, sep="/"):
	def getter(o, attr):
		return
	getter = lambda o, attr: (getattr(o, attr) if attr else o)
	return reduce(getter, path.split(sep), obj)

def _get_activation_shapes(model, input_size, input_var, batch_size=2, n_channels=3):
	assert hasattr(model, "functions"), \
		"Model should have functions defined!"

	if input_var is None:
		input_shape = (batch_size, n_channels, input_size, input_size)
		x = model.xp.zeros(input_shape, dtype=model.xp.float32)
	else:
		x = input_var

	res = [("Input", x.shape)]
	with chainer.no_backprop_mode(), chainer.using_config("train", False):
		for name, link in model.functions.items():
			in_shape = str(x.shape)
			out_shapes = []
			for func in link:
				x = func(x)
				out_shapes.append(str(x.shape))
			logging.debug("\t".join(map(str, (name, in_shape, out_shapes))))
			res.append((name, in_shape, " -> ".join(out_shapes)))
	return res

def print_model_info(model, file=sys.stdout, input_size=None, input_var=None):
	_print = partial(print, file=file)
	name = getattr(model, "name", None)
	if name is None:
		name = model.__class__.__name__

	rows = []
	default_size = 224
	if hasattr(model, "meta"):
		_print(model.meta)
		default_size = model.meta.input_size
		rows.append(("Default input size", f"{default_size}"))

		feature_size = model.meta.feature_size
		rows.append(("Feature size", f"{feature_size}"))

		n_conv_maps = model.meta.n_conv_maps
		rows.append(("# of conv maps (last layer)", f"{n_conv_maps}"))

	n_weights = model.count_params()
	rows.append(("# of parameters", f"{n_weights:,d}"))

	n_params = len(list(model.params()))
	rows.append(("# of trainables", f"{n_params:,d}"))

	n_layers = len(list(model.links()))
	rows.append(("# of layers", f"{n_layers:,d}"))

	_print(f"Printing some information about \"{name}\" model")
	_print(tabulate(rows, tablefmt="fancy_grid"))

	timer_hook = TimerHook()
	memory_hook = CupyMemoryProfileHook()

	with timer_hook, memory_hook:
		shapes = _get_activation_shapes(model, input_size or default_size, input_var)

	timer_hook.print_report()
	memory_hook.print_report()

	_print("In/Out activation shapes:")
	_print(tabulate(shapes,
		headers=["Link name", "Input", "Output"],
		tablefmt="fancy_grid"))

