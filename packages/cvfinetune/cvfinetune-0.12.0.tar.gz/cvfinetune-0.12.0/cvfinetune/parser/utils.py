import logging
import numpy as np
import os
import typing as T
import warnings
import yaml

from cvargparse import BaseParser
from cvdatasets.utils import read_info_file
from functools import wraps

from pathlib import Path


WARNING = """Could not find default info file \"{}\". """ + \
"""Some arguments (dataset, parts etc.) are not restraint to certain choices! """ + \
"""You can set <DATA> environment variable to change the default info file location."""

DEFAULT_INFO_FILE = os.environ.get("DATA")
def get_info_file():

	if DEFAULT_INFO_FILE is not None and os.path.isfile(DEFAULT_INFO_FILE):
		return read_info_file(DEFAULT_INFO_FILE)
	else:
		warnings.warn(WARNING.format(DEFAULT_INFO_FILE))
		return None


def parser_extender(extender):

	@wraps(extender)
	def inner(parser, *args, **kwargs):
		assert isinstance(parser, BaseParser), \
			"Parser should be an BaseParser instance!"

		extender(parser, *args, **kwargs)

		return parser

	return inner


def populate_args(args, ignore = None, replace = {}, fc_params = []):

	args.debug = False

	assert args.load is not None, "--load argument missing!"

	model_path = Path(args.load)

	args_path = model_path.parent / "meta" / "args.yml"

	assert args_path.exists(), f"Couldn't find args file \"{args_path}\""

	logging.info(f"Reading arguments from \"{args_path}\"")

	with open(args_path) as f:
		dumped_args = yaml.safe_load(f)

	for key, value in dumped_args.items():
		if (ignore is not None and key in ignore) or getattr(args, key, None) == value:
			continue

		if key in ["logfile", "loglevel"]:
			continue

		old_value = getattr(args, key, None)
		if key in replace:
			value = replace[key].get(value, value)

		logging.debug(f"Setting \"{key}\" to {value} (originally was {'missing' if old_value is None else old_value})")

		setattr(args, key, value)

	# get the correct number of classes
	args.n_classes = get_n_classes(args.load, args.load_path,
		fc_params=fc_params)

	if args.n_classes <= 0:
		raise KeyError("Could not find number of classes!")

def get_n_classes(weights_file: str, load_path: str = "",
	*, fc_params: T.Tuple[str] = ()) -> int:
	"""
		Searches for the classification layer identified by
		names in fc_params.
	"""

	weights = np.load(weights_file)
	prefixes = [""]

	if load_path != "":
		prefixes.append(load_path)

	for prefix in prefixes:
		for name in fc_params:
			key = f"{prefix}{name}"
			if key not in weights:
				continue
			return weights[key].shape[0]

	return -1


def parse_input_size(args, default: int = 224, attr: str = "input_size"):
	model_type = args.model_type.lower()
	value = getattr(args, attr)
	if value == "infer":
		if "resnet" in model_type:
			size = 224
		elif "inception" in model_type:
			size = 299
		else:
			size = default

	elif value == "infer_big":
		if "resnet" in model_type:
			size = 448
		elif "inception" in model_type:
			# alternatives: 453, 552, 585
			size = 427
		else:
			size = default * 2
	else:
		size = int(value)
	setattr(args, attr, size)
	return (size, size)
