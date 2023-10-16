import wandb

from cvfinetune.training.extensions.reporters.base import BaseReport

class WandbReport(BaseReport):

	def reporter_enabled(self) -> bool:
		return True

	def log(self, key: str, value: float, step: int = 0) -> None:
		wandb.log({key: value}, step=step, commit=False)

	def __call__(self, trainer):
		# self.log will be called with commit=False,
		# so we need to call it once with commit=True
		super().__call__(trainer)
		wandb.log({}, commit=True)
