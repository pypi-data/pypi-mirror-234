from cvfinetune.training.extensions.reporters.base import BaseReport

class SacredReport(BaseReport):
	def __init__(self, *args, ex, **kwargs):
		self.ex = ex
		super().__init__(*args, **kwargs)

	def reporter_enabled(self) -> bool:
		return None not in [self.ex, self.ex.current_run]

	def log(self, key: str, value: float, step: int = 0) -> None:
		self.ex.log_scalar(key, value, step=step)
