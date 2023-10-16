from sacred import SETTINGS

SETTINGS.DISCOVER_SOURCES = "dir"

from cvfinetune.utils.sacred.experiment import Experiment
from cvfinetune.utils.sacred.plotter import SacredPlotter
