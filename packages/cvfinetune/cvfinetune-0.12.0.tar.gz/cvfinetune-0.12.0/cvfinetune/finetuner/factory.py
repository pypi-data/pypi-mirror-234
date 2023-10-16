import logging
import warnings

from cvfinetune import utils
from cvfinetune.finetuner.base import DefaultFinetuner
from cvfinetune.finetuner.mpi import MPIFinetuner
from cvfinetune.utils import mpi

from cvdatasets.utils import pretty_print_dict

class FinetunerFactory:

	@classmethod
	def new(cls, *args, **kwargs):
		raise NotImplementedError(f"Use simple instance creation instead of {cls.__name__}.new()!")

	def __init__(self, *, default=DefaultFinetuner, mpi_tuner=MPIFinetuner, **kwargs):
		super().__init__()

		if "mpi" in kwargs:
			kwargs.pop("mpi")
			warnings.warn("\"mpi\" is no longer supported. MPI checks are performed automatically.", category=DeprecationWarning)

		self.kwargs = kwargs
		self.tuner_cls = default

		if mpi.enabled() and mpi.chainermn_available():
			comm = mpi.new_comm("pure_nccl")
			msg1 = "MPI enabled. Creating NCCL communicator!"
			msg2 = f"Rank: {comm.rank}, IntraRank: {comm.intra_rank}, InterRank: {comm.inter_rank}"
			utils.log_messages(msg1, msg2)

			self["comm"] = comm
			self.tuner_cls = mpi_tuner

		logging.info(f"Using {self.tuner_cls.__name__} with arguments: {pretty_print_dict(self.kwargs)}")

	def __call__(self, opts, **kwargs):
		opt_kwargs = self.tuner_cls.extract_kwargs(opts)
		_kwargs = dict(self.kwargs, **kwargs, **opt_kwargs)
		return self.tuner_cls(config=opts.__dict__, **_kwargs)

	def get(self, key, default=None):
		return self.kwargs.get(key, default)

	def __getitem__(self, key):
		return self.kwargs[key]

	def __setitem__(self, key, value):
		self.kwargs[key] = value
