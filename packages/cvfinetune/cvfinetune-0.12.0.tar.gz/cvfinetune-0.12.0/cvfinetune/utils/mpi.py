import mpi4py.MPI as MPI

try:
	import chainermn
except Exception as e: #pragma: no cover
	_CHAINERMN_AVAILABLE = False #pragma: no cover
else:
	_CHAINERMN_AVAILABLE = True



def chainermn_available(strict: bool = True) -> bool:
	if strict:
		assert _CHAINERMN_AVAILABLE, "Distributed training is not possible!"

	return _CHAINERMN_AVAILABLE

def enabled() -> bool:
	return MPI.COMM_WORLD.Get_size() > 1

def new_comm(comm_type: str = "pure_nccl"):
	return chainermn.create_communicator("pure_nccl")
