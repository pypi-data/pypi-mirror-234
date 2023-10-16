import logging

from datetime import datetime
from os.path import basename
from os.path import join
from typing import Tuple

import chainer

from chainer.training import Trainer as T
from chainer.training import extensions
from chainer.training import trigger as trigger_module
from chainer_addons.training import lr_shift
from chainer_addons.training.extensions import AlternateTrainable
from chainer_addons.training.extensions import SwitchTrainables
from chainer_addons.training.extensions import WarmUp
from chainer_addons.training.extensions.learning_rate import CosineAnnealingLearningRate
from chainer_addons.training.optimizer import OptimizerType

from cvdatasets.utils import attr_dict

default_intervals = attr_dict(
	print =		(1,  'epoch'),
	log =		(1,  'epoch'),
	eval =		(1,  'epoch'),
	snapshot =	(10, 'epoch'),
)

def debug_hook(trainer):
	pass
	# print(trainer.updater.get_optimizer("main").target.model.fc6.W.data.mean(), file=open("debug.out", "a"))


def _is_adam(opts):
	return opts.optimizer == OptimizerType.ADAM.name.lower()

class Trainer(T):

	def __init__(self, opts,
		updater,
		evaluator: extensions.Evaluator = None,
		intervals: attr_dict = default_intervals,
		no_observe: bool = False,
		**kwargs):

		super(Trainer, self).__init__(
			updater=updater,
			stop_trigger=(opts.epochs, 'epoch'),
			out=opts.output,
			**kwargs
		)
		logging.info("Training outputs are saved under \"{}\"".format(self.out))

		self._only_eval = opts.only_eval
		self.offset = 0

		self.setup_evaluator(evaluator, intervals.eval)

		self.setup_warm_up(epochs=opts.warm_up,
			after_warm_up_lr=opts.learning_rate,
			warm_up_lr=opts.learning_rate
		)

		self.setup_lr_schedule(
			lr=opts.learning_rate,
			lr_target=opts.lr_target,
			lr_shift_trigger=(opts.lr_shift, "epoch"),
			lr_decrease_rate=opts.lr_decrease_rate,

			# needed for cosine annealing
			epochs=opts.epochs,
			cosine_schedule=opts.cosine_schedule,
			attr="alpha" if _is_adam(opts) else "lr",
		)

		### Code below is only for "main" Trainers ###
		if no_observe: return

		### Snapshotting ###
		self.setup_snapshots(
			enabled=not opts.no_snapshot,
			obj=self.clf,
			trigger=intervals.snapshot,
			suffix="clf_epoch",
		)

		self.setup_reporter(opts, intervals.log, intervals.print)
		self.setup_progress_bar(opts)

	def setup_reporter(self, opts, log_trigger, print_trigger):

		self.extend(extensions.observe_lr(), trigger=log_trigger)
		self.extend(extensions.LogReport(trigger=log_trigger))

		### Reports and Plots ###
		print_values, plot_values = self.reportables(opts)

		self.extend(extensions.PrintReport(print_values), trigger=print_trigger)

		for name, values in plot_values.items():
			ext = extensions.PlotReport(values, 'epoch', file_name='{}.png'.format(name))
			self.extend(ext)

	def setup_progress_bar(self, opts):
		if not opts.no_progress:
			self.extend(extensions.ProgressBar(update_interval=1))

		elif self.evaluator is not None:
			self.evaluator._progress_bar = False

	@property
	def optimizer(self):
		return self.updater.get_optimizer("main")

	@property
	def clf(self):
		return self.optimizer.target

	@property
	def model(self):
		return self.clf.model

	def setup_lr_schedule(self,
		lr: float,
		lr_target: float,
		lr_shift_trigger: Tuple[int, str],
		lr_decrease_rate: float,

		epochs: int,
		cosine_schedule: int,
		attr: str):

		if cosine_schedule is not None and cosine_schedule > 0:
			lr_shift_ext = CosineAnnealingLearningRate(
				attr=attr,
				lr=lr,
				target=lr_target,
				epochs=epochs,
				offset=self.offset,
				stages=cosine_schedule
			)
			new_epochs = lr_shift_ext._epochs
			self.stop_trigger = trigger_module.get_trigger((new_epochs, "epoch"))
			logging.info(f"Changed number of training epochs from {epochs} to {new_epochs}")
			lr_shift_trigger = None

		else:
			lr_shift_ext = lr_shift(self.optimizer,
				init=lr, rate=lr_decrease_rate, target=lr_target)

		self.extend(lr_shift_ext, trigger=lr_shift_trigger)

	def setup_warm_up(self, epochs: int, after_warm_up_lr: float, warm_up_lr: float):

		if epochs is None or epochs == 0:
			return

		assert epochs > 0, "Warm-up argument must be positive!"
		self.offset = epochs

		logging.info(f"Warm-up of {epochs} epochs enabled!")

		self.extend(WarmUp(epochs, self.model,
			initial_lr=after_warm_up_lr,
			warm_up_lr=warm_up_lr
			)
		)


	def setup_evaluator(self,
		evaluator: extensions.Evaluator,
		trigger: Tuple[int, str]):

		self.evaluator = evaluator
		if evaluator is None:
			return
		self.extend(evaluator, trigger=trigger)

	def setup_snapshots(self, enabled: bool, obj: object, trigger, suffix: str = "ft_model_epoch"):

		if not enabled:
			logging.warning("Models are not snapshot!")
			return

		dump_fmt = suffix + "{0.updater.epoch:03d}.npz"
		self.extend(extensions.snapshot_object(obj, dump_fmt), trigger=trigger)
		logging.info("Snapshot format: \"{}\"".format(dump_fmt))

	def eval_name(self, name):
		if self.evaluator is None:
			return name

		return f"{self.evaluator.default_name}/{name}"

	def reportables(self, opts):

		print_values = [
			"elapsed_time",
			"epoch",
			# "lr",

			"main/accuracy", self.eval_name("main/accuracy"),
			"main/loss", self.eval_name("main/loss"),

		]

		plot_values = {
			"accuracy": [
				"main/accuracy",  self.eval_name("main/accuracy"),
			],
			"loss": [
				"main/loss", self.eval_name("main/loss"),
			],
		}

		return print_values, plot_values


	def run(self, init_eval=True):
		if init_eval:
			logging.info("Evaluating initial model ...")
			init_perf = self.evaluator(self)
			values = {key: float(value) for key, value in init_perf.items()}

			msg = []

			if "val/main/accuracy" in values:
				msg.append("Initial accuracy: {val/main/accuracy:.3%}".format(**values))

			if "val/main/loss" in values:
				msg.append("Initial loss: {val/main/loss:.3f}".format(**values))

			logging.info(" ".join(msg))

		if self._only_eval:
			return
		return super(Trainer, self).run()

