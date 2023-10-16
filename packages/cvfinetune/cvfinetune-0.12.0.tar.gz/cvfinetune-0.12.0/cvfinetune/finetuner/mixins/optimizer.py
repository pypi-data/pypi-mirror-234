import abc
import chainer
import logging

from chainer.optimizer_hooks import Lasso
from chainer.optimizer_hooks import WeightDecay
from chainer_addons.training import optimizer as new_optimizer
from chainer_addons.training.optimizer_hooks import SelectiveWeightDecay
from cvdatasets.utils import pretty_print_dict

from cvfinetune.finetuner.mixins.base import BaseMixin

def check_param_for_decay(param):
    return param.name != "alpha"

def enable_only_head(chain: chainer.Chain):
    if hasattr(chain, "enable_only_head") and callable(chain.enable_only_head):
        chain.enable_only_head()

    else:
        chain.disable_update()
        chain.fc.enable_update()

class _OptimizerCreator:

    def __init__(self, opt, **kwargs):
        super().__init__()

        self.opt = opt
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        if self.opt is None:
            return None

        kwargs = dict(self.kwargs, **kwargs)
        return new_optimizer(self.opt, *args, **kwargs)

class _OptimizerMixin(BaseMixin):

    def __init__(self, *args,
                 optimizer: str,
                 learning_rate: float = 1e-3,
                 weight_decay: float = 5e-4,
                 eps: float = 1e-2,
                 only_head: bool = False,
                 **kwargs):

        super().__init__(*args, **kwargs)

        optimizer_kwargs = dict(decay=0, gradient_clipping=False)

        if optimizer in ["rmsprop", "adam"]:
            optimizer_kwargs["eps"] = eps

        self._opt_creator = _OptimizerCreator(optimizer, **optimizer_kwargs)
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self._only_head = only_head


    def init_optimizer(self):
        """Creates an optimizer for the classifier """

        self._check_attr("clf")
        self._check_attr("_pooling")
        self._check_attr("_l1_loss")

        self.opt = self._opt_creator(self.clf, self.learning_rate)

        if self.opt is None:
            logging.warning("========= No optimizer was initialized! =========")
            return

        kwargs = self._opt_creator.kwargs
        logging.info(
            f"Initialized {type(self.opt).__name__} optimizer"
            f" with initial LR {self.learning_rate} and kwargs: {pretty_print_dict(kwargs)}"
        )

        self.init_regularizer()

        if self._only_head:
            logging.warning("========= Fine-tuning only classifier layer! =========")
            enable_only_head(self.clf)

    def init_regularizer(self, **kwargs):

        if self.weight_decay <= 0:
            return

        if self._l1_loss:
            cls = Lasso

        elif self._pooling == "alpha":
            cls = SelectiveWeightDecay
            kwargs["selection"] = check_param_for_decay

        else:
            cls = WeightDecay

        logging.info(f"Adding {cls.__name__} ({self.weight_decay:e})")
        self.opt.add_hook(cls(self.weight_decay, **kwargs))
