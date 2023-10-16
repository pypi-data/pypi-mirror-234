import abc

from chainer import reporter
from chainer.training import trigger as trigger_module
from chainer.training.extension import Extension

class BaseReport(abc.ABC, Extension):
	def __init__(self, *, keys=None, trigger=(1, "epoch")):
		super().__init__()
		self._keys = keys
		self._trigger = trigger_module.get_trigger(trigger)

		self._init_summary()

	def __call__(self, trainer):
		if not self.reporter_enabled():
			return

		obs = trainer.observation
		keys = self._keys

		if keys is None:
			self._summary.add(obs)
		else:
			self._summary.add({k: obs[k] for k in keys if k in obs})

		if not self._trigger(trainer):
			return

		stats = self._summary.compute_mean()

		step = None
		if self._trigger.unit == "epoch":
			step = trainer.updater.epoch

		elif self._trigger.unit == "iteration":
			step = trainer.updater.iteration

		for name in stats:
			self.log(name, float(stats[name]), step=step)

		self._init_summary()

	def _init_summary(self):
		self._summary = reporter.DictSummary()

	@abc.abstractmethod
	def reporter_enabled(self) -> bool:
		pass

	@abc.abstractmethod
	def log(self, key: str, value: float, step: int = 0) -> None:
		pass


