import logging
import warnings

from chainer_addons.models import PrepareType
from chainercv2.models import model_store
from cvmodelz.models import ModelFactory
from functools import partial
from pathlib import Path
from typing import Tuple

from cvfinetune.finetuner.mixins.base import BaseMixin

class _ModelMixin(BaseMixin):
    """
        This mixin is responsible for model selection, model and optimizer creation,
        and model weights loading.
    """

    def __init__(self, *args,
                 model_type: str,
                 model_kwargs: dict = {},
                 pooling: str = "g_avg",

                 prepare_type: str = "model",
                 center_crop_on_val: bool = True,
                 swap_channels: bool = False,

                 load: str = None,
                 weights: str = None,
                 load_path: str = "",
                 load_strict: bool = False,
                 load_headless: bool = False,
                 pretrained_on: str = "imagenet",

                 from_scratch: bool = False,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.model_type = model_type
        self.model_kwargs = model_kwargs

        self._center_crop_on_val = center_crop_on_val
        self._swap_channels = swap_channels

        if model_type.startswith("chainercv2"):
            if prepare_type != "chainercv2":
                msg = f"Using chainercv2 model, but prepare_type was set to \"{prepare_type}\". "
                "Setting it to \"chainercv2\"!"
                warnings.warn(msg)
            prepare_type = "chainercv2"

        self._prepare_type = prepare_type
        self._pooling = pooling

        self._load = load
        self._weights = weights
        self._from_scratch = from_scratch
        self._load_path = load_path
        self._load_strict = load_strict
        self._load_headless = load_headless
        self._pretrained_on = pretrained_on


    def init_model(self):
        """creates backbone CNN model. This model is wrapped around the classifier later"""

        self._check_attr("input_size")

        self.model = self.new_model()

        logging.info(
            f"Created {type(self.model).__name__} model "
            f" with \"{self._prepare_type}\" prepare function."
        )


    def load_weights(self) -> None:

        self._check_attr("clf")
        self._check_attr("n_classes")

        finetune, weights = self._get_loader()

        self.clf.load(weights,
            n_classes=self.n_classes,
            finetune=finetune,

            path=self._load_path,
            strict=self._load_strict,
            headless=self._load_headless
        )

        self.clf.cleargrads()

        feat_size = self.model.meta.feature_size

        if hasattr(self.clf, "output_size"):
            feat_size = self.clf.output_size

        ### TODO: handle feature size!

        logging.info(f"Part features size after encoding: {feat_size}")



    @property
    def prepare_type(self):
        return PrepareType[self._prepare_type]

    @property
    def prepare(self):
        return partial(self.prepare_type(self.model),
            swap_channels=self._swap_channels,
            keep_ratio=self._center_crop_on_val)

    def new_model(self, **kwargs):
        return ModelFactory.new(self.model_type,
            input_size=self.input_size,
            **self.model_kwargs, **kwargs)

    @property
    def model_info(self):
        return self.data_info.MODELS[self.model_type]



    def _get_loader(self) -> Tuple[bool, str]:

        if self._from_scratch:
            logging.info(f"Training a {type(self.model).__name__} model from scratch!")
            return None, None

        if self._load:
            weights = self._load
            logging.info(f"Loading already fine-tuned weights from \"{weights}\"")
            return False, weights

        elif self._weights:
            weights = self._weights
            logging.info(f"Loading custom fine-tuned weights from \"{weights}\"")
            return True, weights

        else:
            weights = self._default_weights
            logging.info(f"Loading default fine-tuned weights from \"{weights}\"")
            return True, weights

    @property
    def _default_weights(self):
        if self.model_type.startswith("chainercv2"):
            model_name = self.model_type.split(".")[-1]
            return model_store.get_model_file(
                model_name=model_name,
                local_model_store_dir_path=str(Path.home() / ".chainer" / "models"))

        else:
            ds_info = self.data_info
            model_info = self.model_info

            base_dir = Path(ds_info.BASE_DIR)
            weights_dir = base_dir / ds_info.MODEL_DIR / model_info.folder

            weights = model_info.weights
            assert self._pretrained_on in weights, \
                f"Weights for \"{self._pretrained_on}\" pre-training were not found!"

            return str(weights_dir / weights[self._pretrained_on])

