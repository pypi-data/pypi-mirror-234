import abc
import typing as T

from chainer_addons.links import PoolingType
from cvargparse import Arg
from cvargparse import BaseParser

from cvfinetune.parser.utils import parser_extender
from cvmodelz.models import ModelFactory
from cvmodelz.models import PrepareType

@parser_extender
def add_model_args(parser: BaseParser, *,
	model_modules: T.Optional[T.List[str]] = None) -> None:

	if model_modules is None:
		model_modules = ["chainercv2", "cvmodelz"]

	choices = ModelFactory.get_models(model_modules)
	_args = [
		Arg("--model_type", "-mt",
			required=True,
			choices=choices,
			help="type of the model"),

		Arg("--pretrained_on", "-pt",
			default="imagenet",
			choices=["imagenet", "inat"],
			help="type of model pre-training"),

		Arg("--input_size", default="infer",
			help="overrides default input size of the model, if greater than 0. " \
			"Set to \"infer\" to guess the input size from the model type."),

		Arg("--part_input_size", default="infer",
			help="overrides default input part size of the model, if greater than 0. " \
			"Set to \"infer\" to guess the input size from the model type."),

		PrepareType.as_arg("prepare_type",
			help_text="type of image preprocessing"),

		PoolingType.as_arg("pooling",
			help_text="type of pre-classification pooling"),

		Arg("--load",
			help="ignore weights and load already fine-tuned model (classifier will NOT be re-initialized and number of classes will be unchanged)"),

		Arg("--weights",
			help="ignore default weights and load already pre-trained model (classifier will be re-initialized and number of classes will be changed)"),

		Arg("--headless", action="store_true",
			help="ignores classifier layer during loading"),

		Arg("--load_strict", action="store_true",
			help="load weights in a strict mode"),

		Arg("--load_path", default="",
			help="load path within the weights archive"),
	]

	parser.add_args(_args, group_name="Model arguments")


class ModelParserMixin(abc.ABC):
	def __init__(self, *args, **kwargs):
		super(ModelParserMixin, self).__init__(*args, **kwargs)
		add_model_args(self)


__all__ = [
	"ModelParserMixin",
	"add_model_args"
]
