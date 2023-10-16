import chainer
import inspect
import io

from contextlib import contextmanager
from functools import partial

def get_class_that_defined_method(meth):
	if inspect.isfunction(meth):
		cls_name = meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
		return getattr(inspect.getmodule(meth), cls_name, None)

def wrapper(func, key):

	def inner(self):
		return func(self, key)

	return inner

def add_tests(func, model_list) -> None:

	cls = get_class_that_defined_method(func)

	for key in model_list:
		new_func = wrapper(func, key)
		name = f"test_{key.replace('.', '__')}_{func.__name__}"
		new_func.__name__ = name
		setattr(cls, name, new_func)

def is_all_equal(model0: chainer.Chain, model1: chainer.Chain, strict: bool = False, exclude_clf: bool = False) -> bool:
	params0 = dict(model0.namedparams())
	params1 = dict(model1.namedparams())

	for name in params0:
		if exclude_clf and model0.clf_layer_name in name:
			continue
		param0, param1 = params0[name], params1[name]
		if param0.shape != param1.shape:
			if strict:
				return False, f"shape of {name} was not the same: {param0.shape} != {param1.shape}"
			else:
				continue

		if not (param0.array == param1.array).all():
			return False, f"array of {name} was not the same"

	return True, "All equal!"

def is_any_different(model0: chainer.Chain, model1: chainer.Chain, strict: bool = False, exclude_clf: bool = False) -> bool:
	params0 = dict(model0.namedparams())
	params1 = dict(model1.namedparams())

	for name in params0:
		if exclude_clf and model0.clf_layer_name in name:
			continue
		param0, param1 = params0[name], params1[name]
		# print(name)
		if param0.shape != param1.shape:
			if strict:
				return False, f"shape of {name} was not the same: {param0.shape} != {param1.shape}"
			else:
				continue
		if (param0.array != param1.array).any():
			return True, f"Difference in array {name} found."

	return False, "All equal!"


@contextmanager
def memory_file() -> io.BytesIO:
	yield io.BytesIO()

@contextmanager
def clear_print(msg):
	print(msg)
	yield
	print("\033[A{}\033[A".format(" "*len(msg)))
