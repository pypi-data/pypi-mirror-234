import abc
import logging

from chainer import functions as F
from cvdatasets.utils import pretty_print_dict
from cvfinetune.training.loss import smoothed_cross_entropy
from functools import partial

from cvfinetune.finetuner.mixins.base import BaseMixin

class _ClassifierCreator:

    def __init__(self, cls, **kwargs):
        super().__init__()
        self.cls = cls
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self.kwargs = dict(self.kwargs, **kwargs)
        return self.cls(*args, **self.kwargs)

class _ClassifierMixin(BaseMixin):
    """
        This mixin implements the wrapping of the backbone model around
        a classifier instance.
    """

    def __init__(self, *args,
                 classifier_cls,
                 classifier_kwargs: dict = {},
                 l1_loss: bool = False,
                 label_smoothing: float = 0.0,
                 **kwargs):

        super().__init__(*args, **kwargs)
        self._clf_creator = _ClassifierCreator(classifier_cls, **classifier_kwargs)

        self._l1_loss = l1_loss
        self._label_smoothing = label_smoothing


    def init_classifier(self, **kwargs):
        self._check_attr("model")
        self._check_attr("n_classes")

        self.clf = self._clf_creator(self.model,
                                     loss_func=self.loss_func,
                                     **kwargs)

        kwargs = self._clf_creator.kwargs
        logging.info(
            f"Wrapped the model around {type(self.clf).__name__}"
            f" with kwargs: {pretty_print_dict(kwargs)}"
        )

    @property
    def loss_func(self):
        if self._l1_loss:
            return F.hinge

        if self._label_smoothing > 0:
            assert self._label_smoothing < 1, "Label smoothing factor must be less than 1!"

            return smoothed_cross_entropy(self.n_classes, eps=self._label_smoothing)

        return F.softmax_cross_entropy
