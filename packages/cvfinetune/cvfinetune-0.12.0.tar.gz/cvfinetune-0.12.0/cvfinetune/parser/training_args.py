import abc

from cvargparse import Arg
from cvargparse import ArgFactory
from cvargparse import BaseParser
from cvfinetune.parser.utils import parser_extender

from chainer_addons.training import OptimizerType

@parser_extender
def add_training_args(parser: BaseParser) -> None:

	_args = ArgFactory([

		Arg("--warm_up", type=int, help="warm up epochs"),

		OptimizerType.as_arg("optimizer", "opt",
			help_text="type of the optimizer"),

		Arg("--cosine_schedule", type=int,
			default=-1,
			help="enable cosine annealing LR schedule. This parameter sets the number of schedule stages"),

		Arg("--l1_loss", action="store_true",
			help="(only with \"--only_head\" option!) use L1 Hinge Loss instead of Softmax Cross-Entropy"),

		Arg("--from_scratch", action="store_true",
			help="Do not load any weights. Train the model from scratch"),

		Arg("--label_smoothing", type=float, default=0,
			help="Factor for label smoothing"),

		Arg("--only_head", action="store_true", help="fine-tune only last layer"),

	])\
	.seed()\
	.batch_size()\
	.epochs()\
	.debug()\
	.learning_rate(lr=1e-2, lrs=10, lrt=1e-5, lrd=1e-1)\
	.weight_decay(default=5e-4)

	parser.add_args(_args, group_name="Training arguments")

	_args = [
		Arg("--augmentations",
			choices=[
				"random_crop",
				"random_flip",
				"random_rotation",
				"center_crop",
				"color_jitter"
			],
			default=["random_crop", "random_flip", "color_jitter"],
			nargs="*"),

		Arg("--center_crop_on_val", action="store_true"),
		Arg("--brightness_jitter", type=int, default=0.3),
		Arg("--contrast_jitter", type=int, default=0.3),
		Arg("--saturation_jitter", type=int, default=0.3),

	]
	parser.add_args(_args, group_name="Augmentation arguments")

	_args = [
		Arg("--only_eval", action="store_true", help="evaluate the model only. do not train!"),
		Arg("--init_eval", action="store_true", help="evaluate the model before training"),
	]

	parser.add_args(_args, group_name="Evaluation arguments")

	_args = [
		Arg("--no_progress", action="store_true", help="dont show progress bar"),
		Arg("--no_snapshot", action="store_true", help="do not save trained model"),
		Arg("--output", "-o", type=str, default=".out", help="output folder"),
	]
	parser.add_args(_args, group_name="Output arguments")


class TrainingParserMixin(abc.ABC):
	def __init__(self, *args, **kwargs):
		super(TrainingParserMixin, self).__init__(*args, **kwargs)
		add_training_args(self)


__all__ = [
	"TrainingParserMixin",
	"add_training_args"
]
