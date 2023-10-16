import logging
import pyaml
import typing as T

from bdb import BdbQuit
from chainer.serializers import save_npz
from chainer.training import extensions
from chainer.training import updaters
from cvdatasets.utils import pretty_print_dict
from pathlib import Path


from cvfinetune.finetuner.mixins.base import BaseMixin
from cvfinetune.training.extensions import SacredReport
from cvfinetune.training.extensions import ManualGCCollect
from cvfinetune.utils.sacred import Experiment


class _TrainerMixin(BaseMixin):
    """This mixin is responsible for updater, evaluator and trainer creation.
    Furthermore, it implements the run method
    """

    def __init__(self, *args,
                 updater_cls=updaters.StandardUpdater,
                 updater_kwargs: dict = {},

                 only_eval: bool = False,
                 init_eval: bool = False,

                 experiment_name: T.Optional[str] = None,
                 no_snapshot: bool = False,
                 no_sacred: bool = False,

                 manual_gc: bool = True,
                 **kwargs):
        super(_TrainerMixin, self).__init__(*args, **kwargs)
        self.updater_cls = updater_cls
        self.updater_kwargs = updater_kwargs

        self.only_eval = only_eval
        self.init_eval = init_eval
        self.no_snapshot = no_snapshot
        self.no_sacred = no_sacred
        self.experiment_name = experiment_name
        self.manual_gc = manual_gc

        self.ex = None

    @property
    def no_observe(self):
        return self.no_sacred

    def init_experiment(self, *, config: dict):
        """ creates a sacred experiment that is later used
            by the trainer's sacred extension
        """

        self.config = config

        if self.no_sacred:
            logging.warning("Default sacred workflow is disabled "\
                "by the --no_sacred option!")
            return

        self.ex = Experiment(
            name=self.experiment_name,
            config=self.config,
            no_observe=self.no_observe)

        # self.trainer will be initialized later
        def run(*args, **kwargs):
            self._check_attr("trainer")
            return self.trainer.run(*args, **kwargs)

        self.ex.main(run)

    def run_experiment(self, *args, **kwargs):

        if self.ex is None:
            return self.trainer.run(*args, **kwargs)

        sacred_reporter = SacredReport(ex=self.ex, trigger=(1, "epoch"))
        self.trainer.extend(sacred_reporter)
        return self.ex(*args, **kwargs)


    def init_updater(self):
        """Creates an updater from training iterator and the optimizer."""

        self._check_attr("opt")
        self._check_attr("device")
        self._check_attr("train_iter")

        if self.opt is None:
            self.updater = None
            return

        self.updater = self.updater_cls(
            iterator=self.train_iter,
            optimizer=self.opt,
            device=self.device,
            **self.updater_kwargs,
        )
        logging.info(" ".join([
            f"Using single GPU: {self.device}.",
            f"{self.updater_cls.__name__} is initialized",
            f"with following kwargs: {pretty_print_dict(self.updater_kwargs)}"
            ])
        )

    def init_evaluator(self, default_name="val"):
        """Creates evaluation extension from validation iterator and the classifier."""

        self._check_attr("device")
        self._check_attr("val_iter")

        self.evaluator = extensions.Evaluator(
            iterator=self.val_iter,
            target=self.clf,
            device=self.device,
            progress_bar=True
        )

        self.evaluator.default_name = default_name

    def _new_trainer(self, trainer_cls, opts, *args, **kwargs):
        return trainer_cls(
            opts=opts,
            updater=self.updater,
            evaluator=self.evaluator,
            *args, **kwargs
        )

    def run(self, trainer_cls, opts, *args, **kwargs):

        self.trainer = self._new_trainer(trainer_cls, opts, *args, **kwargs)

        if self.manual_gc:
            manual_gc = ManualGCCollect(trigger=(1, "iteration"))
            self.trainer.extend(manual_gc)

        self.save_meta_info()

        logging.info("Snapshotting is {}abled".format(
            "dis" if self.no_snapshot else "en"))

        try:
            self.run_experiment(self.init_eval or self.only_eval)
        except (KeyboardInterrupt, BdbQuit) as e:
            raise e
        except Exception as e:
            self.dump("exception")
            raise e
        else:
            self.dump("final")

    def evaluate(self,
        eval_fpath: T.Optional[T.Union[Path, str]] = None,
        *,
        force: bool = False):

        eval_fpath = Path(eval_fpath)

        if eval_fpath.exists() and not force:
            logging.warning(f"Evaluation file (\"{eval_fpath}\") "\
                "exists already, skipping evaluation")
            return

        records = self.evaluator()

        records = {key: float(value) for key, value in records.items()}
        with open(eval_fpath, "w") as f:
            pyaml.dump(records, f, sort_keys=False)


    def _trainer_output(self, name: str = ""):
        return Path(self.trainer.out, name)

    def dump(self, suffix):
        self._check_attr("only_eval")
        if self.only_eval:
            return

        clf_file = self._trainer_output(f"clf_{suffix}.npz")
        logging.info(f"Storing classifier weights to {clf_file}")
        save_npz(clf_file, self.clf)

    def save_meta_info(self, meta_folder: str = "meta"):
        self._check_attr("config")

        folder = self._trainer_output(meta_folder)
        folder.mkdir(parents=True, exist_ok=True)

        with open(folder / "args.yml", "w") as f:
            pyaml.dump(self.config, f, sort_keys=True)

