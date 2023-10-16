import chainer.functions as F

from cvargparse.utils.enumerations import BaseChoiceType
from functools import partial

from cvmodelz.utils.functions import tf_average_pooling_2d
from cvmodelz.utils.links.pooling.alpha_pooling import AlphaPooling
from cvmodelz.utils.links.pooling.compact_bilinear import CompactBilinearPooling
from cvmodelz.utils.links.pooling.global_average import GlobalAveragePooling

def pool_creator(func):
	def creator(ksize, stride=None, pad=0, **kwargs):
		return partial(func, ksize=ksize, stride=stride, pad=pad)
	return partial(creator)

class PoolingType(BaseChoiceType):
	MAX = pool_creator(F.max_pooling_2d)
	AVG = pool_creator(F.average_pooling_2d)
	TF_AVG = pool_creator(tf_average_pooling_2d)

	G_AVG = GlobalAveragePooling
	CBIL = CompactBilinearPooling
	ALPHA = AlphaPooling

	Default = G_AVG

	@classmethod
	def new(cls, pool_type, **kwargs):
		pool_cls = cls.get(pool_type).value
		return pool_cls(**kwargs)



__all__ = [
	"PoolingType",
	"AlphaPooling",
	"CompactBilinearPooling",
	"GlobalAveragePooling",
	"tf_average_pooling_2d",
]
