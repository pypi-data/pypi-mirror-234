import chainer
import logging
import numpy as np
import typing as T

from cvfinetune.finetuner import mixins

class DefaultFinetuner(
	mixins._ModelMixin,
	mixins._OptimizerMixin,
	mixins._ClassifierMixin,
	mixins._DatasetMixin,
	mixins._IteratorMixin,
	mixins._TrainerMixin):
	""" The default Finetuner gathers together the creations of all needed
	components and call them in the correct order

	"""

	def __init__(self, *args, config: dict = {}, gpu = [-1],
		         seed: T.Optional[int] = None, **kwargs):

		super().__init__(*args, **kwargs)
		self.init_random_state(seed=seed)
		self.init_experiment(config=config)

		self.gpu_config(gpu)
		self.read_annotations()

		self.init_model()
		self.init_datasets()
		self.init_iterators()

		self.init_classifier()
		self.load_weights()

		self.init_optimizer()
		self.init_updater()
		self.init_evaluator()


	def _check_attr(self, attr_name, msg=None):
		msg = msg or f"<{type(self).__name__}> {attr_name} attribute was not initialized!"
		assert hasattr(self, attr_name), msg

	def init_random_state(self, seed: T.Optional[int] = None):
		logging.info(f"Using seed: {seed}")
		self.rnd = np.random.RandomState(seed)

	def init_device(self):
		self.device = chainer.get_device(self.device_id)
		self.device.use()
		return self.device

	def gpu_config(self, devices):
		if -1 in devices:
			self.device_id = -1
		else:
			self.device_id = devices[0]

		device = self.init_device()
		logging.info(f"Using device {device}")
		return device

