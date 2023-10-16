from chainer import link
from chainer import functions as F

class GlobalAveragePooling(link.Link):
	output_dim=None

	# just ignore all Arguments
	def __init__(self, **kw):
		super(GlobalAveragePooling, self).__init__()

	def forward(self, x):
		n, channel, rows, cols = x.shape
		h = F.average_pooling_2d(x, (rows, cols), stride=1)
		h = F.reshape(h, (n, channel))
		return h
