import logging
import munch
import os
import re
import sys
import typing as T

from sacred import Experiment as BaseExperiment
from sacred.observers import MongoObserver
from sacred.utils import apply_backspaces_and_linefeeds

from pathlib import Path
from urllib.parse import quote_plus

def progress_bar_filter(text,
	escape=re.compile(r"\x1B\[([0-?]*[ -/]*[@-~])"),
	line_contents=re.compile(r".*(total|validation|this epoch|Estimated time|\d+ iter, \d+ epoch|\d+ \/ \d+ iteration).+\n"),
	tqdm_progress = re.compile(r"\n? *\d+\%\|.+\n?")):

	""" Filters out the progress bar of chainer """

	_text = apply_backspaces_and_linefeeds(text)

	_text = escape.sub("", _text)
	_text = line_contents.sub("", _text)
	_text = tqdm_progress.sub("", _text)
	_text = re.sub(r"\n *\n*", "\n", _text)

	return _text


class Experiment(BaseExperiment):

	ENV_KEYS: munch.Munch = munch.munchify(dict(
		USER_NAME="MONGODB_USER_NAME",
		PASSWORD="MONGODB_PASSWORD",
		DB_NAME="MONGODB_DB_NAME",

		HOST="MONGODB_HOST",
		PORT="MONGODB_PORT",
	))

	def __init__(self, *args,
		config: dict = {},
		host: T.Optional[str] = None,
		port: T.Optional[int] = None,
		no_observe: bool = False,
		output_filter: T.Callable = progress_bar_filter,
		**kwargs):

		if kwargs.get("base_dir") is None:
			base_dir = Path(sys.argv[0]).resolve().parent
			logging.info(f"Base experiment directory: {base_dir}")
			kwargs["base_dir"] = str(base_dir)

		super(Experiment, self).__init__(*args, **kwargs)

		if no_observe:
			return

		self.logger = logging.getLogger()
		self.captured_out_filter = output_filter

		creds = Experiment.get_creds()
		_mongo_observer = MongoObserver.create(
			url=Experiment.auth_url(creds, host=host, port=port),
			db_name=creds["db_name"],
		)

		self.observers.append(_mongo_observer)

		self.add_config(**config)

	def __call__(self, *args, **kwargs):
		return self._create_run()(*args, **kwargs)

	@classmethod
	def get_creds(cls):
		return dict(
			user=cls._get_env_key(cls.ENV_KEYS.USER_NAME),
			password=cls._get_env_key(cls.ENV_KEYS.PASSWORD),
			db_name=cls._get_env_key(cls.ENV_KEYS.DB_NAME),
		)

	@classmethod
	def auth_url(cls, creds, host="localhost", port=27017):
		host = host or cls.get_host()
		port = port or cls.get_port()
		logging.info(f"MongoDB host: {host}:{port}")

		url = "mongodb://{user}:{password}@{host}:{port}/{db_name}?authSource=admin".format(
			host=host, port=port, **creds)
		return url

	@classmethod
	def get_host(cls):
		return cls._get_env_key(cls.ENV_KEYS.HOST, default="localhost")

	@classmethod
	def get_port(cls):
		return cls._get_env_key(cls.ENV_KEYS.PORT, default=27017)

	@classmethod
	def _get_env_key(cls, key, default=None):
		return quote_plus(str(os.environ.get(key, default)))



__all__ = [
	"Experiment",
	"progress_bar_filter"
]
