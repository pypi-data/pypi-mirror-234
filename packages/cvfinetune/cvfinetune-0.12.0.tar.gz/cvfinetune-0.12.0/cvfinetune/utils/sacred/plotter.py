import pymongo as pym
import numpy as np
import matplotlib.pyplot as plt
import warnings
from datetime import datetime

from matplotlib.gridspec import GridSpec
from chainer_addons.utils.sacred import MPIExperiment

def parse_date(date, fmt="{:d}-{:02d}-{:02d} 00:00:00"):
	if isinstance(date, str):
		return datetime.fromisoformat(date)

	elif isinstance(date, (tuple, list)):
		return datetime.fromisoformat(fmt.format(*date))

	elif date is None:
		return None

	else:
		warnings.warn("Unsupported date format: {date}. Date parsing skipped".format(date))

def query_to_str(query):
	query_list = [f"{key}={value}" for key, value in query.items()]
	return "{{{}}}".format(", ".join(query_list))

class SacredPlotter(object):

	def __init__(self, creds, host=None, port=None):
		super(SacredPlotter, self).__init__()
		auth_url = MPIExperiment.auth_url(creds, host=host, port=port)
		self.client = pym.MongoClient(auth_url)

		self.db = self.client[creds["db_name"]]
		self.metrics = self.db["metrics"]
		self.runs = self.db["runs"]

	def get_values(self, metric, query):

		values = []
		runs = list(self.runs.find(query))

		for run in runs:

			accuracies = self.metrics.find_one(dict(
				name=metric,
				run_id=run["_id"],
			))
			if accuracies is None or accuracies["values"] is None:
				continue

			values.append(accuracies["values"][-1])

		return values

	def plot(self,
		metrics,
		setups,
		query_factory,
		setup_to_label,
		include_running=False,
		start_time=None,
		metrics_key="val/main/",
		**plot_kwargs):

		"""
			Arguments:
				- metrics: defines which metrics to plot

				- setups: defines different setups, that
					will be compared

				- query_factory: callable; creates from the setup
					specification the pymongo query

				- setup_to_label: callable; converts a setup
					specification into a readable label

				- include_running: whether running experiments should
					be included or not

				- start_time: time (starting of an experiment) from which
					the experiments should be considered

				- metrics_key: prefix that will be appended to each
					metric name

		"""

		n_metrics = len(metrics)
		n_cols = int(np.ceil(np.sqrt(n_metrics)))
		n_rows = int(np.ceil(n_metrics / n_cols))

		grid = GridSpec(n_rows, n_cols)
		axs = []
		for i, metric in enumerate(metrics):

			res = []

			for setup in setups:
				query = query_factory(setup)

				if not include_running:
					query["status"] = {"$ne": "RUNNING"}

				if start_time is not None:
					query["start_time"] = {"$gte": parse_date(start_time)}

				values = self.get_values(f"{metrics_key}{metric}", query)
				if len(values) == 0:
					warnings.warn(f"No values found for query { query_to_str(query) }")
				else:
					res.append((setup, values))

			row, col = np.unravel_index(i, (n_rows, n_cols))

			if len(res) == 0:
				warnings.warn(f"No setups for metric \"{metric}\" collected!")

			else:

				ax = plt.subplot(grid[row, col])
				labels, values = zip(*[(setup_to_label(setup, vals), vals) for setup, vals in res if vals])
				ax.boxplot(values, labels=labels, **plot_kwargs)
				ax.set_title(f"Metric: {metric}")

				axs.append(ax)

		return axs


