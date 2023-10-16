import gc
import logging
import threading


from chainer.training import extension
from chainer.training import trigger as trigger_module

class ManualGCCollect(extension.Extension):

	SLEEP = 3

	def __init__(self, trigger=(1, "iteration")):
		super().__init__()

		self._trigger = trigger_module.get_trigger(trigger)

		self.thread = threading.Thread(target=self.work)

		self.stop = threading.Event()
		self.trigger_gc = threading.Event()

	def work(self):
		logging.info("GC Thread working ...")

		while True:
			if self.stop.is_set():
				break

			if not self.trigger_gc.wait(self.SLEEP):
				continue

			self.trigger_gc.clear()
			gc.collect()

		logging.info("GC Thread finished")

	def initialize(self, trainer):
		logging.info("Starting GC Thread ...")
		self.thread.start()

	def __call__(self, trainer):
		if not self._trigger(trainer):
			return
		self.trigger_gc.set()


	def finalize(self):
		logging.info("Finilizing GC Thread")
		self.stop.set()
		self.thread.join()

	def on_error(self, trainer, exc, tb):
		logging.info("Error occured, stopping GC Thread")
		self.stop.set()
		self.thread.join()
