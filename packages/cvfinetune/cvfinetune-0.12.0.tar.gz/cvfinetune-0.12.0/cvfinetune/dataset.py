import abc
import numpy as np

from cvdatasets.dataset import AnnotationsReadMixin
from cvdatasets.dataset import IteratorMixin
from cvdatasets.dataset import TransformMixin
from cvdatasets.dataset import UniformPartMixin

class BaseDataset(TransformMixin, UniformPartMixin, AnnotationsReadMixin):
	"""Commonly used dataset constellation"""

	def __init__(self, *args, prepare, center_crop_on_val: bool = True, **kwargs):
		super().__init__(*args, **kwargs)
		raise NotImplementedError("YOU SHOULD NOT USE ME!")
		self.prepare = prepare

	def augment(self, im):
		if isinstance(im, list):
			im = np.array(im)

		if np.logical_and(0 <= im, im <= 1).all():
			im = im * 2 -1

		return im

	def transform(self, im_obj):
		im, parts, lab = im_obj.as_tuple()
		return self.prepare(im), lab + self.label_shift
