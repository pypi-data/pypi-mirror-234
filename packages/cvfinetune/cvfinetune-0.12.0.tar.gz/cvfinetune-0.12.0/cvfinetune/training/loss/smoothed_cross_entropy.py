from chainer import functions as F


class SmoothedCrossEntropy:

	def __init__(self, n_classes: int, eps: float = 0.1):
		super(SmoothedCrossEntropy, self).__init__()
		self.n_classes = n_classes
		self.eps = eps

	def __call__(self, pred, gt, **kwargs):
		loss = F.softmax_cross_entropy(pred, gt, **kwargs)

		# -sum[ log( P(k) ) * U ]
		reg_loss = F.mean(F.sum(F.log_softmax(pred) / self.n_classes, axis=1))

		return (1-self.eps) * loss - self.eps * reg_loss


def smoothed_cross_entropy(N: int, eps: float = 0.1):
	return SmoothedCrossEntropy(n_classes=N, eps=eps)
